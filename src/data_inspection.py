import pandas as pd


def structure_diagnostics(df: pd.DataFrame) -> dict:
    """Compute structural diagnostics

    This function takes a dataframe and computes different structural metrics to create a diagnosis of the data. The goal is to analyze if the data is ready for the following analysis

    Args:
        df (pd.DataFrame): dataframe with ticker information

    Returns:
        dict: dictionary with metrics
    """
    # Shape basics
    n_rows, n_cols = df.shape
    n_tickers = len(df.columns)

    # Date Coverage
    start_date = df.index.min()
    end_date = df.index.max()
    n_days = len(df.index)

    # Index quality
    index_monotonic = df.index.is_monotonic_increasing
    index_unique = df.index.is_unique
    index_nan = df.index.hasnans
    n_duplicates = df.index.duplicated().sum()

    # Column quality
    tickers_list = df.columns.tolist()
    dtypes = df.dtypes.value_counts()
    all_float = all(dt.kind in "fi" for dt in df.dtypes)

    # General check
    status = (
        "Quality Check - Pass"
        if (n_tickers == 20 and index_monotonic and index_unique and all_float and n_days > 2500)
        else "Quality Check - Failed"
    )

    # Build Dictionary with metrics
    structure_metrics = {
        "n_rows": n_rows,
        "n_columns": n_cols,
        "n_tickers": n_tickers,
        "start_date": start_date,
        "end_date": end_date,
        "n_days": n_days,
        "is_monotonic": index_monotonic,
        "is_unique": index_unique,
        "has_nan": index_nan,
        "n_duplicates": n_duplicates,
        "tickers": tickers_list,
        "dtypes": dtypes,
        "dtypes_all_float": all_float,
        "status": status,
    }

    return structure_metrics


def ticker_diagnostics(df: pd.DataFrame) -> pd.DataFrame:
    pass


def visual_diagnostics():
    pass


def stationarity_test():
    pass


def run_data_inspection(df: pd.DataFrame):
    print("=" * 50)
    print("Data Diagnostcs - EDA")
    print("=" * 50)
