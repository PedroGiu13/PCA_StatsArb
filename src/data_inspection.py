import pandas as pd
import seaborns as sns
import matplotlib.pyplot as plt


def structure_diagnostics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute structural diagnostics

    This function takes a dataframe and computes different structural metrics to create a diagnosis of the data. The goal is to analyze if the data is ready for the following analysis

    Args:
        df (pd.DataFrame): dataframe with ticker information indexed by time

    Returns:
        pd.DataFrame: dataframe with structural metrics
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

    # Build dataframe with metrics
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

    return pd.DataFrame(structure_metrics)


def ticker_diagnostics(df: pd.DataFrame) -> pd.DataFrame:
    """Per-ticker diagnostics

    Functions that computes the coverage and numerical summary of every ticker

    Args:
        df (pd.DataFrame): dataframe with ticker information indexed by time

    Returns:
        pd.DataFrame: dataframe with six metrics per ticker
    """
    total_days = len(df.index)
    valid_days_series = total_days - df.isna().sum()
    pct_missing_values = 1 - (valid_days_series / total_days)

    ticker_metrics = pd.DataFrame(
        {
            "Valid Days": valid_days_series,
            "Missing %": pct_missing_values,
            "Mean Return": df.mean(),
            "Std Return": df.std(),
            "Min Return": df.min(),
            "Max Return": df.max(),
        }
    )

    return ticker_metrics


def correlation_diagnostics(df: pd.DataFrame) -> dict:
    df_corr = df.corr()

    corr_metrics = {
        "Corr Df": df_corr,
        "Avg Corr": df_corr.mean(),
        "Std Corr": df_corr.std(),
        "Min Cor": df_corr.min(),
        "Max Corr": df_corr.max(),
    }

    return corr_metrics


def extreme_returns_diagnostics(df: pd.DataFrame):
    pass


def stationarity_test():
    pass


def run_data_inspection(df: pd.DataFrame):
    print("=" * 50)
    print("Data Diagnostcs - EDA")
    print("=" * 50)
