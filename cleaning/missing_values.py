import pandas as pd


def get_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100

    summary = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": missing.values,
        "Percentage (%)": missing_percent.values
    })

    return summary


def drop_rows_with_missing(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return df.dropna(subset=columns)


def drop_columns_by_threshold(df: pd.DataFrame, threshold_percent: float) -> pd.DataFrame:
    min_non_null = int(len(df) * (1 - threshold_percent / 100))
    return df.dropna(axis=1, thresh=min_non_null)


def fill_missing_with_constant(df: pd.DataFrame, column: str, value) -> pd.DataFrame:
    df = df.copy()
    df[column] = df[column].fillna(value)
    return df


def fill_missing_with_stat(df: pd.DataFrame, column: str, method: str) -> pd.DataFrame:
    df = df.copy()

    if method == "mean":
        df[column] = df[column].fillna(df[column].mean())
    elif method == "median":
        df[column] = df[column].fillna(df[column].median())
    elif method == "mode":
        mode_value = df[column].mode()
        if not mode_value.empty:
            df[column] = df[column].fillna(mode_value[0])

    return df


def fill_missing_forward(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df = df.copy()
    df[column] = df[column].ffill()
    return df


def fill_missing_backward(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df = df.copy()
    df[column] = df[column].bfill()
    return df