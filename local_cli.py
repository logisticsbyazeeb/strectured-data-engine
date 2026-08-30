from __future__ import annotations

import argparse
from pathlib import Path

from extract import extract_invoice_tables, generate_excel_report, generate_csv_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Customs Data Engine - Local PDF Invoice Processor")
    parser.add_argument("pdf_path", type=str, help="Path to the source PDF invoice file")
    parser.add_argument("--output", type=str, default="customs_output.xlsx", help="Output file path (.xlsx or .csv)")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}")
        return

    print(f"Processing: {pdf_path}")
    records = extract_invoice_tables(pdf_path)

    if not records:
        print("No invoice rows detected.")
        return

    output_path = Path(args.output)
    suffix = output_path.suffix.lower()

    if suffix == ".csv":
        csv_content = generate_csv_report(records)
        output_path.write_text(csv_content, encoding="utf-8")
        print(f"Generated {output_path} with {len(records)} invoice rows.")
    else:
        workbook = generate_excel_report(records)
        output_path.write_bytes(workbook.getvalue())
        print(f"Generated {output_path} with {len(records)} invoice rows.")


if __name__ == "__main__":
    main()