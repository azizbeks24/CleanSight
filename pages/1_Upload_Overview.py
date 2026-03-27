from utils.session import initialize_session_state, reset_session_state, clear_history
import streamlit as st
import pandas as pd
import json

initialize_session_state()

st.title("Upload & Overview")

top_left, top_right = st.columns([4, 1])

with top_left:
    st.write("Upload your dataset to begin analysis.")

with top_right:
    if st.button("Reset session"):
        reset_session_state()
        st.success("Session reset successfully.")

file = st.file_uploader("Upload your dataset", type=["csv", "xlsx", "json"])

if file is not None:
    df = None

    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)

        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)

        elif file.name.endswith(".json"):
            data = json.load(file)

            if isinstance(data, dict) and "data" in data:
                df = pd.DataFrame(data["data"])

            elif isinstance(data, list):
                df = pd.DataFrame(data)

            elif isinstance(data, dict):
                df = pd.json_normalize(data)

            else:
                st.error("Unsupported JSON structure.")
                st.stop()

        if df is not None:
            st.success("File uploaded successfully!")
            st.session_state.original_df = df.copy()
            st.session_state.working_df = df.copy()
            st.session_state.transformation_log = []
            clear_history()
            st.info("Dataset loaded. Proceed to Cleaning Studio.")
        else:
            st.error("Could not process file format.")

    except Exception as e:
        st.error(f"Error reading file: {e}")

if st.session_state.working_df is not None:
    df = st.session_state.working_df

    st.success("Dataset is stored in session.")

    st.subheader("Quick Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Missing Values", int(df.isnull().sum().sum()))
    col2.metric("Duplicate Rows", int(df.duplicated().sum()))
    col3.metric("Columns", df.shape[1])

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Info")
    col1, col2 = st.columns(2)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    st.subheader("Column Types")
    dtype_df = df.dtypes.astype(str).reset_index()
    dtype_df.columns = ["Column", "Data Type"]
    st.dataframe(dtype_df)

    st.subheader("Missing Values")
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": missing.values,
        "Percentage (%)": missing_percent.values
    })
    st.dataframe(missing_df)

    st.subheader("Duplicates")
    duplicates = df.duplicated().sum()
    st.write("Number of duplicate rows:", duplicates)