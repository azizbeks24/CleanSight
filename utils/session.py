import streamlit as st


def initialize_session_state():
    if "original_df" not in st.session_state:
        st.session_state.original_df = None

    if "working_df" not in st.session_state:
        st.session_state.working_df = None

    if "transformation_log" not in st.session_state:
        st.session_state.transformation_log = []

    if "history" not in st.session_state:
        st.session_state.history = []


def reset_session_state():
    st.session_state.original_df = None
    st.session_state.working_df = None
    st.session_state.transformation_log = []
    st.session_state.history = []


def save_undo_state(df):
    if df is not None:
        st.session_state.history.append(df.copy())


def undo_last_step():
    if st.session_state.history:
        st.session_state.working_df = st.session_state.history.pop()

        if st.session_state.transformation_log:
            st.session_state.transformation_log.pop()

        return True
    return False


def clear_history():
    st.session_state.history = []