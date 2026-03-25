import streamlit as st
import pandas as pd
import io

st.title("Export")

df = st.session_state.working_df

if df is not None:
    st.subheader("Download Cleaned Dataset")

    # CSV
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download as CSV",
        data=csv_data,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

    # Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="CleanedData")
    excel_data = excel_buffer.getvalue()

    st.download_button(
        label="Download as Excel",
        data=excel_data,
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # JSON
    json_data = df.to_json(orient="records", indent=4)
    st.download_button(
        label="Download as JSON",
        data=json_data,
        file_name="cleaned_data.json",
        mime="application/json"
    )

else:
    st.warning("No dataset available. Please upload and clean a dataset first.")