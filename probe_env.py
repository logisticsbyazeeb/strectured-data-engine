import importlib.util, shutil, json

checks = {
    'tesseract': shutil.which('tesseract'),
    'pytesseract': bool(importlib.util.find_spec('pytesseract')),
    'PIL': bool(importlib.util.find_spec('PIL')),
    'fitz': bool(importlib.util.find_spec('fitz')),
    'pymupdf': bool(importlib.util.find_spec('pymupdf')),
    'pypdf': bool(importlib.util.find_spec('pypdf')),
    'pdf2image': bool(importlib.util.find_spec('pdf2image')),
    'pdfplumber': bool(importlib.util.find_spec('pdfplumber')),
}
open('probe_env_out.txt', 'w', encoding='utf-8').write(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
