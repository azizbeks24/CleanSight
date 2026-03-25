import pandas as pd


def convert_to_numeric(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df = df.copy()
    df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def convert_to_datetime(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df = df.copy()
    df[column] = pd.to_datetime(df[column], errors="coerce")
    return df


def convert_to_string(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df = df.copy()
    df[column] = df[column].astype(str)
    return df


def get_column_types(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })