from __future__ import annotations

from pathlib import Path

import streamlit as st

from extract import extract_invoice_tables, generate_excel_report


st.set_page_config(page_title="Customs Data Engine", page_icon="🚀", layout="wide")
st.title("Customs Data Engine")
st.caption("Extract invoice tables, normalize country codes, and create dual-sheet Excel output.")

uploaded_file = st.file_uploader("Upload an invoice PDF", type=["pdf"])

if uploaded_file is not None:
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    file_path = upload_dir / uploaded_file.name
    file_path.write_bytes(uploaded_file.read())

    try:
        records = extract_invoice_tables(file_path)
        if not records:
            st.warning("No invoice rows were detected in the uploaded PDF.")
        else:
            excel_bytes = generate_excel_report(records)
            st.success(f"Extracted {len(records)} rows successfully.")
            st.download_button(
                label="Download Excel output",
                data=excel_bytes.getvalue(),
                file_name="customs_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

            st.dataframe(records[:10], use_container_width=True)
    except Exception as exc:  # pragma: no cover - UI side error handling
        st.error(f"An error occurred while processing the PDF: {exc}")

else:
    st.info("Upload a PDF invoice to generate the customs Excel workbook.")
