# AGENTS.md

## Project overview
This repository is a small Python app for processing customs invoice PDFs and generating Excel files for downstream ERP or website upload workflows.

Core files:
- [app.py](app.py) — Streamlit UI; uploads a PDF, extracts rows, and offers the Excel download
- [extract.py](extract.py) — invoice parsing, country normalization, and workbook generation
- [README.md](README.md) — project-level usage notes
- [requirements.txt](requirements.txt) — Python dependencies
- [uploads/](uploads/) — local sample and uploaded PDFs

## Working conventions
- Prefer using the project virtual environment directly instead of relying on `Activate.ps1` in PowerShell. In this repo, commands should be run as:
  - `.\.venv\Scripts\python.exe ...`
  - `.\.venv\Scripts\streamlit.exe run app.py`
- The app is expected to accept a PDF upload and produce an Excel workbook with two sheets: `Website Upload` and `Frappe ERP Inbound`.
- Extraction logic should remain evidence-driven: validate against the real PDF layout before tightening or relaxing row filters.
- Keep record fields stable: `Invoice No`, `Date`, `Supplier`, `Country`, `Currency`, `Amount`, `Description`.

## Development workflow
- Start the app from the repo root:
  - `.\.venv\Scripts\streamlit.exe run app.py --server.port 8502`
- Use the local upload directory for sample PDFs or debugging output.
- Prefer small, targeted fixes in [extract.py](extract.py) over large rewrites.
- If a PDF is scanned or irregular, assume the layout may not match a rigid 6-column table. Validate parsed rows before rejecting them.

## Common pitfalls
- The first failure mode in this project is over-filtering rows. A strict `len(cleaned) < 6` check can discard valid invoice data from real PDFs.
- PowerShell execution policy can block `.venv\Scripts\Activate.ps1`; do not rely on that activation path.
- Avoid creating broad abstractions when the app only needs a narrow extraction-and-export workflow.

## Validation
- Use the project venv when testing Python code.
- For extraction work, validate with the real uploaded sample PDF before declaring the bug fixed.
- When adding logic, prefer a focused regression test for the edge case being fixed.

## Related files
- [AGENTS.md](AGENTS.md) — repo-wide guidance for agents
- [.github/agents/customs-invoice-processor.agent.md](.github/agents/customs-invoice-processor.agent.md) — specialized agent for invoice extraction debugging
