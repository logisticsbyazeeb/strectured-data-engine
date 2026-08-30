---
name: invoice-pdf-debugging
description: "Use when: debugging customs invoice extraction, analyzing uploaded PDF tables, validating rows from scanned or irregular PDFs, or investigating why a PDF yields no invoice rows in this repo."
---
# Invoice PDF debugging

This skill is for debugging PDF invoice parsing in this repository. Use it when the app uploads a PDF and fails to extract invoice rows or produces an incomplete Excel export.

## Goal
Diagnose and fix extraction issues with the real uploaded PDF layout before altering the export workflow.

## Constraints
- Prefer the project venv when running Python commands.
- Validate against the actual PDF in `uploads/` or the uploaded file, not against synthetic assumptions.
- Keep field names stable: `Invoice No`, `Date`, `Supplier`, `Country`, `Currency`, `Amount`, `Description`.
- Prefer targeted fixes in [extract.py](../../extract.py) over broad rewrites.
- Do not assume every invoice has a rigid 6-column table layout.

## Workflow
1. Reproduce the problem with the uploaded PDF or a sample file.
2. Inspect the raw `pdfplumber` output for pages and tables before changing filters.
3. Look for row-shape assumptions like `len(cleaned) < 6` that reject valid rows.
4. Fix the narrow parsing logic, keeping header and empty rows excluded.
5. Run a focused validation against the real PDF and confirm rows appear in the expected schema.

## Common pitfalls
- Over-filtering rows because they do not match a strict table width.
- Forgetting that scanned or irregular PDFs may have missing table structure or varying column counts.
- Running commands via `.venv\Scripts\Activate.ps1` instead of direct `.venv\Scripts\python.exe` calls in PowerShell.

## Useful commands
- `.\.venv\Scripts\python.exe debug_pdf_probe.py`
- `.\.venv\Scripts\streamlit.exe run app.py --server.port 8502`
- `.\.venv\Scripts\python.exe -m unittest test_extract.py`

## Output expectations
Return a concise summary containing:
- root cause found
- fix applied
- files changed
- validation evidence from the real PDF or regression test
- any remaining risk or follow-up item
