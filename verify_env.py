import importlib.util, json
mods = ['pdfplumber','pandas','openpyxl','pycountry','pytesseract','PIL','fitz','pymupdf','pypdf','pdf2image','rapidocr_onnxruntime','pypdfium2']
result = {m: bool(importlib.util.find_spec(m)) for m in mods}
path = 'verify_env.json'
with open(path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
