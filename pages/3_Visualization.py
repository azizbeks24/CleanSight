import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.session import initialize_session_state

initialize_session_state()

st.title("Visualization Studio")
st.write("Create simple visualizations from the cleaned dataset.")

if st.session_state.working_df is None:
    st.warning("No dataset available. Please upload and clean data first.")
    st.stop()

df = st.session_state.working_df.copy()

st.subheader("Dataset Preview")
st.dataframe(df.head())

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
datetime_cols = df.select_dtypes(include=["datetime64[ns]"]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

st.subheader("Chart Builder")

chart_type = st.selectbox(
    "Select chart type",
    ["Histogram", "Line Chart", "Bar Chart"]
)

if chart_type == "Histogram":
    st.caption("Histogram requires one numeric column.")

    if not numeric_cols:
        st.warning("No numeric columns available for histogram.")
    else:
        column = st.selectbox("Select numeric column", numeric_cols)

        if st.button("Generate Histogram"):
            fig, ax = plt.subplots()
            ax.hist(df[column].dropna(), bins=20)
            ax.set_title(f"Histogram of {column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

elif chart_type == "Line Chart":
    st.caption("Line chart requires numeric or datetime X-axis, and numeric Y-axis.")

    valid_x_cols = numeric_cols + datetime_cols

    if not valid_x_cols:
        st.warning("No numeric or datetime columns available for X-axis.")
    elif not numeric_cols:
        st.warning("No numeric columns available for Y-axis.")
    else:
        x_col = st.selectbox("Select X-axis", valid_x_cols)
        y_col = st.selectbox("Select Y-axis (numeric)", numeric_cols)

        if st.button("Generate Line Chart"):
            plot_df = df[[x_col, y_col]].dropna().copy()
            plot_df = plot_df.sort_values(by=x_col)

            fig, ax = plt.subplots()
            ax.plot(plot_df[x_col], plot_df[y_col])
            ax.set_title(f"{y_col} over {x_col}")
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            plt.xticks(rotation=45)
            st.pyplot(fig)

elif chart_type == "Bar Chart":
    st.caption("Bar chart works best with categorical columns.")

    if not categorical_cols:
        st.warning("No categorical columns available for bar chart.")
    else:
        column = st.selectbox("Select categorical column", categorical_cols)

        if st.button("Generate Bar Chart"):
            counts = df[column].value_counts().head(10)

            fig, ax = plt.subplots()
            counts.plot(kind="bar", ax=ax)
            ax.set_title(f"Top 10 values of {column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Count")
            plt.xticks(rotation=45)
            st.pyplot(fig)
            