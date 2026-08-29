from pathlib import Path
import pdfplumber

p = Path('uploads/Stamp000217.pdf')
print('exists', p.exists(), 'size', p.stat().st_size if p.exists() else 0)
if not p.exists():
    raise SystemExit(1)

with pdfplumber.open(p) as pdf:
    print('pages', len(pdf.pages))
    for i, page in enumerate(pdf.pages[:3], 1):
        txt = page.extract_text() or ''
        print('--- PAGE', i, '---')
        print((txt[:1500]).replace('\n', ' | '))
        tables = page.extract_tables() or []
        print('tables', len(tables))
        for idx, table in enumerate(tables[:2]):
            print('table', idx, 'first_rows', table[:4])
