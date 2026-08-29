from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Iterable

import pandas as pd
import pdfplumber

COUNTRY_CODES = {
    "uae": "ARE",
    "united arab emirates": "ARE",
    "dubai": "ARE",
    "saudi arabia": "SAU",
    "india": "IND",
    "china": "CHN",
    "united states": "USA",
    "united kingdom": "GBR",
    "european union": "EU",
    "japan": "JPN",
    "singapore": "SGP",
    "germany": "DEU",
    "france": "FRA",
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


def extract_invoice_tables(pdf_path: str | Path) -> list[dict[str, str]]:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    rows: list[dict[str, str]] = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables() or []
            for table in tables:
                for row in table:
                    if not row or not any(_clean_cell(cell) for cell in row):
                        continue

                    cleaned = [_clean_cell(cell) for cell in row]
                    if len(cleaned) < 6:
                        continue

                    invoice_record = {
                        "Invoice No": cleaned[0],
                        "Date": cleaned[1] if len(cleaned) > 1 else "",
                        "Supplier": cleaned[2] if len(cleaned) > 2 else "",
                        "Country": normalize_country_name(cleaned[3] if len(cleaned) > 3 else ""),
                        "Currency": cleaned[4] if len(cleaned) > 4 else "",
                        "Amount": cleaned[5] if len(cleaned) > 5 else "",
                        "Description": " ".join(cleaned[6:]) if len(cleaned) > 6 else "",
                    }

                    rows.append(invoice_record)

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
