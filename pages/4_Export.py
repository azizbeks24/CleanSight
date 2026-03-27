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

# =========================
# EXPORT DATASET
# =========================
st.subheader("Export Cleaned Dataset")

col1, col2 = st.columns(2)

with col1:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv",
    )

with col2:
    excel_file = "cleaned_dataset.xlsx"
    df.to_excel(excel_file, index=False)
    with open(excel_file, "rb") as f:
        st.download_button(
            label="Download Excel",
            data=f,
            file_name=excel_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

# =========================
# TRANSFORMATION REPORT
# =========================
st.subheader("Transformation Report")

log = st.session_state.transformation_log

if log:
    st.write("Transformation Steps:")
    st.dataframe(pd.DataFrame(log))

    report = {
        "report_generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_steps": len(log),
        "steps": log
    }

    json_report = json.dumps(report, indent=4)

    st.download_button(
        label="Download JSON Report",
        data=json_report,
        file_name="transformation_report.json",
        mime="application/json"
    )

else:
    st.info("No transformations to export.")