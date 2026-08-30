import importlib.util
import shutil
print('tesseract', shutil.which('tesseract'))
for name in ['pytesseract', 'PIL', 'fitz', 'pymupdf', 'pypdf', 'pdf2image', 'pycountry']:
    print(name, bool(importlib.util.find_spec(name)))
