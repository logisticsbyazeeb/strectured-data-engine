# # Customs Data Engine 🚀

A Python-powered data processing and automation engine designed to streamline JAFZA & Dubai Customs documentation workflows, invoice processing, and dual-sheet Excel generation (Website Upload & Frappe ERP Inbound).

---

## 📌 Overview

**Customs Data Engine** automates data entry and table extraction from PDF invoices using `pdfplumber`, normalizes country names into standard ISO codes, and generates structured Excel output for customs and ERP integration.

---

## ✨ Features

- 📄 **PDF Extraction:** Extracts invoice tables directly using `pdfplumber`.
- 🌐 **ISO Country Normalization:** Standardizes country names into official ISO codes.
- 📊 **Dual-Sheet Excel Output:** Automatically populates:
  - Sheet 1: Website Upload
  - Sheet 2: Frappe ERP Inbound
- 💻 **Streamlit App:** Provides an interactive web UI (`app.py`) for easy document uploading and processing.

---

## 📁 Key Project Files

- `app.py` – Streamlit web interface for interactive invoice processing.
- `extract.py` – CLI script for extracting invoice data.
- `requirements.txt` – Python dependencies.

---

## 🛠️ Setup & Installation

```bash
# Clone the repository
git clone [https://github.com/logisticsbyazeeb/customs-data-engine.git](https://github.com/logisticsbyazeeb/customs-data-engine.git)
cd customs-data-engine

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py