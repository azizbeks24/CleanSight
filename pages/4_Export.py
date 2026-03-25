import streamlit as st

from utils.session import initialize_session_state

initialize_session_state()

st.title("Export Data")

if st.session_state.working_df is None:
    st.warning("No data available. Please upload and process data first.")
    st.stop()

df = st.session_state.working_df.copy()

st.subheader("Preview Final Dataset")
st.dataframe(df.head())

st.subheader("Download Options")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download as CSV",
    data=csv,
    file_name="cleaned_data.csv",
    mime="text/csv"
)
