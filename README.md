# Customs Data Engine 🚀

A Python-powered data processing and automation engine for customs invoice workflows, PDF table extraction, and Excel output generation.

## Overview

This project extracts invoice data from PDF documents, normalizes country values, and produces a dual-sheet Excel workbook suitable for customs website upload and ERP processing workflows.

## Features

- PDF table extraction with `pdfplumber`
- Basic country normalization for common invoice destinations
- Excel workbook generation with two sheets:
  - Website Upload
  - Frappe ERP Inbound
- A Streamlit web interface for uploading PDFs and downloading output

## Project files

- `app.py` – Streamlit web interface
- `extract.py` – extraction and Excel generation logic
- `requirements.txt` – Python dependencies
- `.gitignore` – repo ignore rules

## Setup

```bash
cd "c:\Users\Lenovo\OneDrive\Documents\GitHub\strectured-data-engine"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Usage

1. Start the app with `streamlit run app.py`.
2. Upload a PDF invoice.
3. Download the generated Excel workbook.

## Notes

This is a starting project structure intended to support customs invoice processing tasks. It may need further tuning depending on the exact invoice layout and ERP schema you expect to support.