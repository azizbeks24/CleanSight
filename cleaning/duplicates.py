import pandas as pd


def count_full_duplicates(df: pd.DataFrame) -> int:
    return int(df.duplicated().sum())


def get_full_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.duplicated(keep=False)].copy()


def count_subset_duplicates(df: pd.DataFrame, columns: list[str]) -> int:
    if not columns:
        return 0
    return int(df.duplicated(subset=columns).sum())


def get_subset_duplicates(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    if not columns:
        return pd.DataFrame()
    return df[df.duplicated(subset=columns, keep=False)].copy()


def remove_duplicates(df: pd.DataFrame, keep: str = "first", subset: list[str] | None = None) -> pd.DataFrame:
    if subset:
        return df.drop_duplicates(subset=subset, keep=keep).copy()
    return df.drop_duplicates(keep=keep).copy()