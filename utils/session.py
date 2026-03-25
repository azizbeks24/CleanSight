import streamlit as st

def initialize_session_state():
    if "original_df" not in st.session_state:
        st.session_state.original_df = None

    if "working_df" not in st.session_state:
        st.session_state.working_df = None

    if "transformation_log" not in st.session_state:
        st.session_state.transformation_log = []

def reset_session_state():
    st.session_state.original_df = None
    st.session_state.working_df = None
    st.session_state.transformation_log = []
