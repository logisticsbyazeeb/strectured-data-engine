from pathlib import Path
import pdfplumber

p = Path(r'.\uploads\Stamp000217.pdf')
print('exists', p.exists(), 'size', p.stat().st_size if p.exists() else 0)
with pdfplumber.open(p) as pdf:
    print('pages', len(pdf.pages))
    for i, page in enumerate(pdf.pages[:3], 1):
        text = (page.extract_text() or '')[:2000]
        print(f'--- PAGE {i} TEXT ---')
        print(text)
        tables = page.extract_tables() or []
        print(f'--- PAGE {i} TABLE COUNT {len(tables)} ---')
        for j, table in enumerate(tables[:3]):
            print(f'TABLE {j}:')
            for row in table[:12]:
                print(row)
            print('---')
