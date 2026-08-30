import unittest
from pathlib import Path
from types import SimpleNamespace

import extract


class FakePage:
    def extract_tables(self):
        return [[
            "INV-2045",
            "2026-08-01",
            "Acme Trading",
            "United Arab Emirates",
            "AED",
            "2500",
            "Import goods",
        ]] 


class FakePdf:
    def __init__(self):
        self.pages = [FakePage()]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakePageNoTables:
    def extract_tables(self):
        return []

    def extract_text(self):
        return ""


class FakePdfNoTables:
    def __init__(self):
        self.pages = [FakePageNoTables()]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class ExtractInvoiceTablesTests(unittest.TestCase):
    def test_accepts_irregular_invoice_rows(self):
        real_open = extract.pdfplumber.open
        try:
            extract.pdfplumber.open = lambda path: FakePdf()
            rows = extract.extract_invoice_tables(Path("uploads/example.pdf"))
        finally:
            extract.pdfplumber.open = real_open

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Invoice No"], "INV-2045")
        self.assertEqual(rows[0]["Country"], "ARE")
        self.assertEqual(rows[0]["Currency"], "AED")
        self.assertEqual(rows[0]["Amount"], "2500")

    def test_uses_ocr_fallback_when_pdf_has_no_tables(self):
        real_open = extract.pdfplumber.open
        real_fallback = getattr(extract, "_extract_rows_with_ocr", None)
        try:
            extract.pdfplumber.open = lambda path: FakePdfNoTables()
            extract._extract_rows_with_ocr = lambda path: [{
                "Invoice No": "INV-1001",
                "Date": "2026-08-01",
                "Supplier": "Acme Co",
                "Country": "ARE",
                "Currency": "AED",
                "Amount": "3210",
                "Description": "OCR fallback row",
            }]
            rows = extract.extract_invoice_tables(Path("uploads/example.pdf"))
        finally:
            extract.pdfplumber.open = real_open
            if real_fallback is None:
                delattr(extract, "_extract_rows_with_ocr")
            else:
                extract._extract_rows_with_ocr = real_fallback

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Invoice No"], "INV-1001")
        self.assertEqual(rows[0]["Amount"], "3210")


if __name__ == "__main__":
    unittest.main()
