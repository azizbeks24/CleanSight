import streamlit as st
import pandas as pd
import json
from datetime import datetime

from utils.session import initialize_session_state

initialize_session_state()

st.title("Export & Report")

if st.session_state.working_df is None:
    st.warning("No dataset available. Please upload and clean data first.")
    st.stop()

df = st.session_state.working_df
log = st.session_state.transformation_log if "transformation_log" in st.session_state else []

# =========================
# EXPORT DATASET
# =========================
st.subheader("Export Cleaned Dataset")

col1, col2, col3 = st.columns(3)

with col1:
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="cleaned_dataset.csv",
        mime="text/csv",
    )

with col2:
    excel_file = "cleaned_dataset.xlsx"
    df.to_excel(excel_file, index=False)
    with open(excel_file, "rb") as f:
        st.download_button(
            label="Download XLSX",
            data=f,
            file_name=excel_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

with col3:
    json_data = df.to_json(orient="records", indent=4)
    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name="cleaned_dataset.json",
        mime="application/json",
    )

# =========================
# TRANSFORMATION LOG
# =========================
st.subheader("Transformation Log")

if log:
    st.write("Transformation Steps:")
    st.dataframe(pd.DataFrame(log))

    log_json = json.dumps(log, indent=4)

    st.download_button(
        label="Download Transformation Log (JSON)",
        data=log_json,
        file_name="transformation_log.json",
        mime="application/json"
    )

# =========================
# OPTIONAL REPORT PREVIEW
# =========================
    report = {
        "report_generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_steps": len(log),
        "steps": log
    }

    with st.expander("Preview Transformation Report"):
        st.json(report)

else:
    st.info("No transformations to export.")