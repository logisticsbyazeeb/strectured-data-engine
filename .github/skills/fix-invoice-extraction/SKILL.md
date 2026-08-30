---
name: fix-invoice-extraction
description: fix-invoice-extraction
disable-model-invocation: true
---
Diagnose and fix the invoice PDF extraction bug in this repo.

Focus on:
- the real uploaded PDF in `uploads/`
- the parsing logic in [extract.py](../../extract.py)
- the Streamlit upload flow in [app.py](../../app.py)
- preserving the expected output schema for `Invoice No`, `Date`, `Supplier`, `Country`, `Currency`, `Amount`, and `Description`

Instructions:
1. Reproduce the issue with the actual PDF before changing logic.
2. Check whether the parser is over-filtering rows because of a rigid table-shape assumption.
3. Prefer a small, evidence-based fix in the extraction layer.
4. Validate with the real sample PDF or a focused regression test.
5. Report the root cause, files changed, and validation evidence.
