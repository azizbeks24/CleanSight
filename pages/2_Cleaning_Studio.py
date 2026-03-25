import streamlit as st
import pandas as pd

from utils.session import initialize_session_state
from cleaning.missing_values import (
    get_missing_summary,
    drop_rows_with_missing,
    drop_columns_by_threshold,
    fill_missing_with_constant,
    fill_missing_with_stat,
    fill_missing_forward,
    fill_missing_backward,
)
from cleaning.duplicates import (
    count_full_duplicates,
    get_full_duplicates,
    count_subset_duplicates,
    get_subset_duplicates,
    remove_duplicates,
)
from cleaning.types import (
    convert_to_numeric,
    convert_to_datetime,
    convert_to_string,
    get_column_types,
)

initialize_session_state()

st.title("Cleaning Studio")
st.write("Clean and prepare your dataset step by step.")

if st.session_state.working_df is None:
    st.warning("No dataset loaded. Please go to Upload Overview first.")
    st.stop()

df = st.session_state.working_df.copy()

show_original = st.checkbox("Show original dataset")

if show_original and st.session_state.original_df is not None:
    st.subheader("Original Dataset Preview")
    st.dataframe(st.session_state.original_df.head())

st.subheader("Current Dataset Preview")
st.dataframe(df.head())

st.subheader("Missing Values Summary")
missing_summary = get_missing_summary(df)
st.dataframe(missing_summary)

total_missing_now = int(df.isnull().sum().sum())
st.info(f"Total missing values currently in working dataset: {total_missing_now}")

st.subheader("Missing Values Tools")

tab1, tab2, tab3 = st.tabs([
    "Drop Missing",
    "Fill Missing",
    "Advanced Fill"
])

with tab1:
    st.markdown("### Drop Missing Data")

    drop_action = st.radio(
        "Choose drop action",
        ["Drop rows with missing values", "Drop columns above threshold"],
        key="drop_action"
    )

    if drop_action == "Drop rows with missing values":
        selected_columns = st.multiselect(
            "Select columns",
            df.columns,
            key="drop_rows_columns"
        )

        confirm_drop_rows = st.checkbox(
            "Confirm row drop transformation",
            key="confirm_drop_rows"
        )

        if st.button("Apply row drop"):
            if not selected_columns:
                st.warning("Please select at least one column.")
            elif not confirm_drop_rows:
                st.warning("Please confirm the transformation before applying it.")
            else:
                before_rows = len(df)
                before_missing = df.isnull().sum().sum()

                new_df = drop_rows_with_missing(df, selected_columns)

                after_rows = len(new_df)
                after_missing = new_df.isnull().sum().sum()

                st.session_state.working_df = new_df
                st.session_state.transformation_log.append({
                    "operation": "drop_rows_with_missing",
                    "columns": selected_columns,
                    "rows_before": before_rows,
                    "rows_after": after_rows,
                    "missing_before": int(before_missing),
                    "missing_after": int(after_missing),
                })

                st.success("Row drop applied successfully.")
                st.info(f"Rows: {before_rows} → {after_rows}")
                st.info(f"Missing values: {int(before_missing)} → {int(after_missing)}")
                st.success(f"Total missing values now: {int(after_missing)}")

    elif drop_action == "Drop columns above threshold":
        threshold = st.slider(
            "Missing value threshold (%)",
            0,
            100,
            30,
            key="drop_column_threshold"
        )

        confirm_drop_cols = st.checkbox(
            "Confirm column drop transformation",
            key="confirm_drop_cols"
        )

        if st.button("Apply column drop"):
            if not confirm_drop_cols:
                st.warning("Please confirm the transformation before applying it.")
            else:
                before_cols_count = df.shape[1]
                before_missing = df.isnull().sum().sum()
                before_cols = list(df.columns)

                new_df = drop_columns_by_threshold(df, threshold)

                after_cols_count = new_df.shape[1]
                after_missing = new_df.isnull().sum().sum()
                after_cols = list(new_df.columns)

                removed_cols = [col for col in before_cols if col not in after_cols]

                st.session_state.working_df = new_df
                st.session_state.transformation_log.append({
                    "operation": "drop_columns_by_threshold",
                    "threshold_percent": threshold,
                    "removed_columns": removed_cols,
                    "columns_before": before_cols_count,
                    "columns_after": after_cols_count,
                    "missing_before": int(before_missing),
                    "missing_after": int(after_missing),
                })

                st.success("Column drop applied successfully.")
                st.info(f"Columns: {before_cols_count} → {after_cols_count}")
                st.info(f"Missing values: {int(before_missing)} → {int(after_missing)}")
                st.write("Removed columns:", removed_cols if removed_cols else "None")
                st.success(f"Total missing values now: {int(after_missing)}")

with tab2:
    st.markdown("### Fill Missing Data")

    fill_action = st.radio(
        "Choose fill action",
        ["Fill with constant value", "Fill with mean / median / mode"],
        key="fill_action"
    )

    if fill_action == "Fill with constant value":
        column = st.selectbox("Select column", df.columns, key="constant_column")
        constant_value = st.text_input("Enter constant value", key="constant_value")

        confirm_constant = st.checkbox(
            "Confirm constant fill transformation",
            key="confirm_constant_fill"
        )

        if st.button("Apply constant fill"):
            if not confirm_constant:
                st.warning("Please confirm the transformation before applying it.")
            else:
                before_missing = df[column].isnull().sum()
                total_before_missing = df.isnull().sum().sum()

                new_df = fill_missing_with_constant(df, column, constant_value)

                after_missing = new_df[column].isnull().sum()
                total_after_missing = new_df.isnull().sum().sum()

                st.session_state.working_df = new_df
                st.session_state.transformation_log.append({
                    "operation": "fill_missing_with_constant",
                    "column": column,
                    "value": constant_value,
                    "missing_before": int(before_missing),
                    "missing_after": int(after_missing),
                })

                st.success(f"Missing values in '{column}' filled with '{constant_value}'.")
                st.info(f"Missing in '{column}': {int(before_missing)} → {int(after_missing)}")
                st.success(f"Total missing values now: {int(total_after_missing)}")
                st.info(f"Overall missing values: {int(total_before_missing)} → {int(total_after_missing)}")

    elif fill_action == "Fill with mean / median / mode":
        column = st.selectbox("Select column", df.columns, key="stat_column")
        method = st.selectbox("Choose method", ["mean", "median", "mode"], key="stat_method")

        confirm_stat = st.checkbox(
            "Confirm statistical fill transformation",
            key="confirm_stat_fill"
        )

        if st.button("Apply statistical fill"):
            if not confirm_stat:
                st.warning("Please confirm the transformation before applying it.")
            elif method in ["mean", "median"] and not pd.api.types.is_numeric_dtype(df[column]):
                st.error("Mean and median can only be used on numeric columns.")
            else:
                before_missing = df[column].isnull().sum()
                total_before_missing = df.isnull().sum().sum()

                new_df = fill_missing_with_stat(df, column, method)

                after_missing = new_df[column].isnull().sum()
                total_after_missing = new_df.isnull().sum().sum()

                st.session_state.working_df = new_df
                st.session_state.transformation_log.append({
                    "operation": "fill_missing_with_stat",
                    "column": column,
                    "method": method,
                    "missing_before": int(before_missing),
                    "missing_after": int(after_missing),
                })

                st.success(f"Missing values in '{column}' filled using {method}.")
                st.info(f"Missing in '{column}': {int(before_missing)} → {int(after_missing)}")
                st.success(f"Total missing values now: {int(total_after_missing)}")
                st.info(f"Overall missing values: {int(total_before_missing)} → {int(total_after_missing)}")

with tab3:
    st.markdown("### Advanced Fill")

    advanced_action = st.radio(
        "Choose advanced fill action",
        ["Forward fill", "Backward fill"],
        key="advanced_action"
    )

    if advanced_action == "Forward fill":
        column = st.selectbox("Select column", df.columns, key="ffill_column")

        confirm_ffill = st.checkbox(
            "Confirm forward fill transformation",
            key="confirm_ffill"
        )

        if st.button("Apply forward fill"):
            if not confirm_ffill:
                st.warning("Please confirm the transformation before applying it.")
            else:
                before_missing = df[column].isnull().sum()
                total_before_missing = df.isnull().sum().sum()

                new_df = fill_missing_forward(df, column)

                after_missing = new_df[column].isnull().sum()
                total_after_missing = new_df.isnull().sum().sum()

                st.session_state.working_df = new_df
                st.session_state.transformation_log.append({
                    "operation": "forward_fill",
                    "column": column,
                    "missing_before": int(before_missing),
                    "missing_after": int(after_missing),
                })

                st.success(f"Forward fill applied to '{column}'.")
                st.info(f"Missing in '{column}': {int(before_missing)} → {int(after_missing)}")
                st.success(f"Total missing values now: {int(total_after_missing)}")
                st.info(f"Overall missing values: {int(total_before_missing)} → {int(total_after_missing)}")

    elif advanced_action == "Backward fill":
        column = st.selectbox("Select column", df.columns, key="bfill_column")

        confirm_bfill = st.checkbox(
            "Confirm backward fill transformation",
            key="confirm_bfill"
        )

        if st.button("Apply backward fill"):
            if not confirm_bfill:
                st.warning("Please confirm the transformation before applying it.")
            else:
                before_missing = df[column].isnull().sum()
                total_before_missing = df.isnull().sum().sum()

                new_df = fill_missing_backward(df, column)

                after_missing = new_df[column].isnull().sum()
                total_after_missing = new_df.isnull().sum().sum()

                st.session_state.working_df = new_df
                st.session_state.transformation_log.append({
                    "operation": "backward_fill",
                    "column": column,
                    "missing_before": int(before_missing),
                    "missing_after": int(after_missing),
                })

                st.success(f"Backward fill applied to '{column}'.")
                st.info(f"Missing in '{column}': {int(before_missing)} → {int(after_missing)}")
                st.success(f"Total missing values now: {int(total_after_missing)}")
                st.info(f"Overall missing values: {int(total_before_missing)} → {int(total_after_missing)}")

st.subheader("Duplicates Tools")

dup_tab1, dup_tab2 = st.tabs([
    "Full-Row Duplicates",
    "Subset Duplicates"
])

with dup_tab1:
    st.markdown("### Full-Row Duplicates")

    full_dup_count = count_full_duplicates(df)
    st.info(f"Full-row duplicate count: {full_dup_count}")

    show_full_duplicates = st.checkbox(
        "Show full duplicate rows",
        key="show_full_duplicates"
    )

    if show_full_duplicates:
        full_dup_df = get_full_duplicates(df)
        if not full_dup_df.empty:
            st.dataframe(full_dup_df)
        else:
            st.info("No full-row duplicates found.")

    keep_option_full = st.selectbox(
        "When removing duplicates, which row should be kept?",
        ["first", "last"],
        key="keep_full_duplicates"
    )

    confirm_full_remove = st.checkbox(
        "Confirm full-row duplicate removal",
        key="confirm_full_remove"
    )

    if st.button("Remove full-row duplicates"):
        if not confirm_full_remove:
            st.warning("Please confirm the transformation before applying it.")
        else:
            before_rows = len(df)
            new_df = remove_duplicates(df, keep=keep_option_full)
            after_rows = len(new_df)
            removed_rows = before_rows - after_rows

            st.session_state.working_df = new_df
            st.session_state.transformation_log.append({
                "operation": "remove_full_duplicates",
                "keep": keep_option_full,
                "rows_before": before_rows,
                "rows_after": after_rows,
                "rows_removed": removed_rows,
            })

            st.success("Full-row duplicate removal applied successfully.")
            st.info(f"Rows: {before_rows} → {after_rows}")
            st.info(f"Duplicate rows removed: {removed_rows}")

with dup_tab2:
    st.markdown("### Subset Duplicates")

    subset_columns = st.multiselect(
        "Select columns to check duplicates by",
        df.columns,
        key="subset_duplicate_columns"
    )

    if subset_columns:
        subset_dup_count = count_subset_duplicates(df, subset_columns)
        st.info(f"Subset duplicate count: {subset_dup_count}")

        show_subset_duplicates = st.checkbox(
            "Show subset duplicate rows",
            key="show_subset_duplicates"
        )

        if show_subset_duplicates:
            subset_dup_df = get_subset_duplicates(df, subset_columns)
            if not subset_dup_df.empty:
                st.dataframe(subset_dup_df)
            else:
                st.info("No subset duplicates found.")

        keep_option_subset = st.selectbox(
            "When removing subset duplicates, which row should be kept?",
            ["first", "last"],
            key="keep_subset_duplicates"
        )

        confirm_subset_remove = st.checkbox(
            "Confirm subset duplicate removal",
            key="confirm_subset_remove"
        )

        if st.button("Remove subset duplicates"):
            if not confirm_subset_remove:
                st.warning("Please confirm the transformation before applying it.")
            else:
                before_rows = len(df)
                new_df = remove_duplicates(df, keep=keep_option_subset, subset=subset_columns)
                after_rows = len(new_df)
                removed_rows = before_rows - after_rows

                st.session_state.working_df = new_df
                st.session_state.transformation_log.append({
                    "operation": "remove_subset_duplicates",
                    "subset_columns": subset_columns,
                    "keep": keep_option_subset,
                    "rows_before": before_rows,
                    "rows_after": after_rows,
                    "rows_removed": removed_rows,
                })

                st.success("Subset duplicate removal applied successfully.")
                st.info(f"Rows: {before_rows} → {after_rows}")
                st.info(f"Duplicate rows removed: {removed_rows}")
    else:
        st.write("Select one or more columns to analyze subset duplicates.")

st.subheader("Data Type Conversion")

types_tab1, types_tab2 = st.tabs([
    "View Types",
    "Convert Types"
])

with types_tab1:
    st.markdown("### Column Data Types")
    types_df = get_column_types(df)
    st.dataframe(types_df)

with types_tab2:
    st.markdown("### Convert Column Type")

    column = st.selectbox("Select column", df.columns, key="type_column")

    target_type = st.selectbox(
        "Convert to",
        ["numeric", "datetime", "string"],
        key="target_type"
    )

    confirm_convert = st.checkbox(
        "Confirm type conversion",
        key="confirm_type_conversion"
    )

    if st.button("Apply conversion"):
        if not confirm_convert:
            st.warning("Please confirm before applying.")
        else:
            before_type = str(df[column].dtype)

            if target_type == "numeric":
                new_df = convert_to_numeric(df, column)
            elif target_type == "datetime":
                new_df = convert_to_datetime(df, column)
            else:
                new_df = convert_to_string(df, column)

            after_type = str(new_df[column].dtype)

            st.session_state.working_df = new_df
            st.session_state.transformation_log.append({
                "operation": "type_conversion",
                "column": column,
                "from": before_type,
                "to": after_type,
            })

            st.success(f"Converted '{column}' from {before_type} → {after_type}")

st.subheader("Updated Dataset Preview")
st.dataframe(st.session_state.working_df.head())

st.subheader("Transformation Log")
if st.session_state.transformation_log:
    st.dataframe(pd.DataFrame(st.session_state.transformation_log))
else:
    st.info("No transformations applied yet.")
