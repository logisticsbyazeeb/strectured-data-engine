from __future__ import annotations

import re
from io import BytesIO
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
import pdfplumber

COUNTRY_CODES = {
    "uae": "AE",
    "united arab emirates": "AE",
    "dubai": "AE",
    "saudi arabia": "SA",
    "india": "IN",
    "china": "CN",
    "united states": "US",
    "united kingdom": "GB",
    "european union": "EU",
    "japan": "JP",
    "singapore": "SG",
    "germany": "DE",
    "france": "FR",
}


def normalize_country_name(country_name: str | None) -> str:
    value = (country_name or "").strip()
    if not value:
        return ""

    normalized = " ".join(value.lower().split())
    return COUNTRY_CODES.get(normalized, value.upper()[:3])


def _clean_cell(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return " ".join(text.split())


def _matches_invoice_row(candidate: Sequence[str]) -> bool:
    cleaned = [_clean_cell(cell) for cell in candidate]
    if not cleaned or not any(cleaned):
        return False
    if len(cleaned) < 2:
        return False

    header_text = " ".join(cleaned).lower()
    if (
        ("invoice" in header_text and "date" in header_text)
        or ("supplier" in header_text and "currency" in header_text)
        or ("invoice no" in header_text and "amount" in header_text)
    ):
        return False

    invoice_no = cleaned[0]
    amount = cleaned[-1]
    return bool(invoice_no) or bool(amount)


def _build_invoice_record(cells: Sequence[str]) -> dict[str, str] | None:
    cleaned = [_clean_cell(cell) for cell in cells]
    if not cleaned or not _matches_invoice_row(cleaned):
        return None

    invoice_record = {
        "Invoice No": cleaned[0],
        "Date": cleaned[1] if len(cleaned) > 1 else "",
        "Supplier": cleaned[2] if len(cleaned) > 2 else "",
        "Country": normalize_country_name(cleaned[3] if len(cleaned) > 3 else ""),
        "Currency": cleaned[4] if len(cleaned) > 4 else "",
        "Amount": cleaned[5] if len(cleaned) > 5 else "",
        "Description": " ".join(cleaned[6:]) if len(cleaned) > 6 else "",
    }

    if not invoice_record["Invoice No"] and not invoice_record["Amount"]:
        return None

    if not invoice_record["Invoice No"] and len(cleaned) > 1 and re.search(r"^\d+", cleaned[1]):
        invoice_record["Invoice No"] = cleaned[1]
        invoice_record["Date"] = ""

    return invoice_record


def _ocr_record_from_result(ocr_result: Sequence[Sequence[object]]) -> dict[str, str] | None:
    texts = []
    for item in ocr_result:
        if len(item) < 3:
            continue
        text = _clean_cell(item[1])
        if text:
            texts.append(text)
    if not texts:
        return None

    combined = " ".join(texts)
    record: dict[str, str] = {
        "Invoice No": "",
        "Date": "",
        "Supplier": "",
        "Country": "",
        "Currency": "",
        "Amount": "",
        "Description": "",
    }

    invoice_no_match = re.search(r"(?i)(?:INVOICE\s*NO|INV\s*NO)\s*([A-Z0-9-]+)", combined)
    if invoice_no_match:
        record["Invoice No"] = invoice_no_match.group(1).upper()

    date_match = re.search(r"(?i)(?:INVOICE\s*DATE|DATE)\s*([0-9]{2}-[0-9]{2}-[0-9]{4}|[0-9]{4}-[0-9]{2}-[0-9]{2})", combined)
    if date_match:
        record["Date"] = date_match.group(1)

    currency_match = re.search(r"(?i)(?:CURRENCY|CURR)\s*([A-Z]{3})", combined)
    if currency_match:
        record["Currency"] = currency_match.group(1).upper()

    amount_match = re.search(r"(?i)(?:GRAND\s*TOTAL|TOTAL|AMOUNT)\s*([0-9,]+\.[0-9]{2})\s*([A-Z]{3})?", combined)
    if amount_match:
        record["Amount"] = amount_match.group(1).replace(",", "")
        if amount_match.group(2):
            record["Currency"] = amount_match.group(2).upper()

    if not record["Amount"]:
        for text in texts:
            if re.search(r"\d+[.,]\d{2}", text) and re.search(r"(?i)(total|subtotal|amount)", text):
                amount_match = re.search(r"([0-9,]+\.[0-9]{2})", text)
                if amount_match:
                    record["Amount"] = amount_match.group(1).replace(",", "")
                    break

    country_name = ""
    if "United Arab Emirates" in combined:
        country_name = "United Arab Emirates"
    elif "Dubai" in combined:
        country_name = "Dubai"
    if country_name:
        record["Country"] = normalize_country_name(country_name)

    if not record["Supplier"]:
        if "Jebel Ali Free Zone" in combined:
            record["Supplier"] = "Jebel Ali Free Zone"
        elif "Dubai - United Arab Emirates" in combined:
            record["Supplier"] = "Dubai - United Arab Emirates"
        elif country_name:
            record["Supplier"] = country_name

    if not record["Description"]:
        record["Description"] = "Imported invoice" if record["Invoice No"] else "OCR fallback invoice"

    if not record["Invoice No"] and not record["Amount"]:
        return None

    return record


def _extract_rows_with_ocr(pdf_path: str | Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    try:
        from rapidocr_onnxruntime import RapidOCR
        import pypdfium2
    except ImportError:
        return rows

    try:
        pdf = pypdfium2.PdfDocument(str(pdf_path))
    except Exception:
        return rows

    try:
        ocr = RapidOCR()
        for page_index in range(len(pdf)):
            page = pdf[page_index]
            bitmap = page.render(scale=2)
            image = np.asarray(bitmap.to_pil())
            result, _ = ocr(image)
            if not result:
                continue

            record = _ocr_record_from_result(result)
            if record is not None:
                rows.append(record)
    except Exception:
        return rows
    finally:
        pdf.close()

    return rows


def _iter_table_rows(tables: Sequence[Sequence[object]] | None) -> Iterable[Sequence[object]]:
    if not tables:
        return []

    rows: list[Sequence[object]] = []
    for table in tables:
        if not table:
            continue
        if isinstance(table[0], (list, tuple)):
            rows.extend(row for row in table if row)
        else:
            rows.append(table)
    return rows


def extract_invoice_tables(pdf_path: str | Path) -> list[dict[str, str]]:
    path = Path(pdf_path)
    rows: list[dict[str, str]] = []

    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables() or []
                for row in _iter_table_rows(tables):
                    if not row or not any(_clean_cell(cell) for cell in row):
                        continue
                    record = _build_invoice_record(row)
                    if record is not None:
                        rows.append(record)

                page_text = page.extract_text() or ""
                is_meaningful_table = any(
                    any(_clean_cell(cell) for cell in row) for row in _iter_table_rows(tables)
                )
                if not page_text and not is_meaningful_table:
                    fallback_rows = _extract_rows_with_ocr(path)
                    if fallback_rows:
                        rows.extend(fallback_rows)
    except FileNotFoundError:
        if not path.exists():
            raise
        fallback_rows = _extract_rows_with_ocr(path)
        if fallback_rows:
            rows.extend(fallback_rows)
    except Exception:
        if path.exists():
            fallback_rows = _extract_rows_with_ocr(path)
            if fallback_rows:
                rows.extend(fallback_rows)

    return rows


def build_excel_workbooks(data: Iterable[dict[str, str]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    records = list(data)
    website_upload = pd.DataFrame(records)
    frappe_inbound = website_upload.copy()

    if "Invoice No" in frappe_inbound.columns:
        frappe_inbound = frappe_inbound.rename(columns={"Invoice No": "invoice_no"})
    if "Amount" in frappe_inbound.columns:
        frappe_inbound = frappe_inbound.rename(columns={"Amount": "amount"})

    standard_columns = [
        "Invoice No",
        "Date",
        "Supplier",
        "Country",
        "Currency",
        "Amount",
        "Description",
    ]

    website_upload = website_upload.reindex(columns=standard_columns, fill_value="")
    frappe_inbound = frappe_inbound.reindex(columns=standard_columns, fill_value="")

    return website_upload, frappe_inbound


def generate_excel_report(data: Iterable[dict[str, str]]) -> BytesIO:
    website_upload, frappe_inbound = build_excel_workbooks(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        website_upload.to_excel(writer, sheet_name="Website Upload", index=False)
        frappe_inbound.to_excel(writer, sheet_name="Frappe ERP Inbound", index=False)

    output.seek(0)
    return output


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract invoice tables and generate Excel output.")
    parser.add_argument("pdf_path", type=str, help="Path to the source PDF invoice file")
    parser.add_argument("--output", type=str, default="customs_output.xlsx", help="Output Excel file path")
    args = parser.parse_args()

    records = extract_invoice_tables(args.pdf_path)
    workbook = generate_excel_report(records)
    Path(args.output).write_bytes(workbook.getvalue())
    print(f"Generated {args.output} with {len(records)} invoice rows.")
