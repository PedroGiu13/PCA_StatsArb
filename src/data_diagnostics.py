import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from src.config import (
    UNIVERSE_SIZE,
    MIN_HISTORY_DAYS,
    MISSING_DATA_THRESHOLD,
    LOW_CORR_THRESHOLD,
    EXTREME_THRESHOLD_10,
    EXTREME_THRESHOLD_25,
)


def structure_diagnostics(
    df: pd.DataFrame, expected_universe: int = UNIVERSE_SIZE, min_n_days: int = MIN_HISTORY_DAYS
) -> dict:
    """Compute structural diagnostics

    This function takes a dataframe and computes different structural metrics to create a diagnosis of the data. The goal is to analyze if the data is ready for the following analysis

    Args:
        df (pd.DataFrame): dataframe with ticker information indexed by time
        expected_universe (int): Expected number of tickers in the universe. Defaults to UNIVERSE_SIZE.
        min_n_days (int): Minimum number of trading days required to pass the structure check. Defaults to MIN_HISTORY_DAYS.

    Returns:
        dict: dictionary with structural metrics
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
        "PASS"
        if (n_tickers == expected_universe and index_monotonic and index_unique and all_float and n_days > min_n_days)
        else "FAIL"
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

    return structure_metrics


def ticker_diagnostics(df: pd.DataFrame, missing_threshold: float = MISSING_DATA_THRESHOLD) -> pd.DataFrame:
    """Per-ticker diagnostics

    Functions that computes the coverage and numerical summary of every ticker

    Args:
        df (pd.DataFrame): dataframe with ticker information indexed by time
        missing_threshold (float): Maximum acceptable proportion of missing values per ticker (e.g. 0.02 = 2%). Defaults to MISSING_DATA_THRESHOLD.

    Returns:
        pd.DataFrame: dataframe with metrics per ticker
    """
    total_days = len(df.index)
    valid_days_series = total_days - df.isna().sum()
    pct_missing_values = 1 - (valid_days_series / total_days)

    mean_series = df.mean()
    std_series = df.std()
    min_series = df.min()
    max_series = df.max()

    status = (
        (pct_missing_values < missing_threshold)
        & (min_series > -0.6)
        & (max_series < 0.8)
        & (std_series < 3 * std_series.median())
    )

    ticker_metrics = pd.DataFrame(
        {
            "valid_days": valid_days_series,
            "missing_pct": pct_missing_values * 100,
            "avg_return": mean_series,
            "std_return": std_series,
            "min_return": min_series,
            "max_return": max_series,
            "status": np.where(status, "PASS", "FAIL"),
        }
    )

    return ticker_metrics


def correlation_diagnostics(df: pd.DataFrame, low_corr_threshold: float = LOW_CORR_THRESHOLD) -> dict:
    """Correlation diagnostics

    Function that computes the correlation of the entire dataframe as well as per ticker correlations and checks dataframe is ready to continue wth further analysis

    Args:
        df (pd.DataFrame): dataframe with ticker information indexed by time
        low_corr_threshold (float): Minimum acceptable average pairwise correlation for a ticker. Tickers below this are flagged. Defaults to LOW_CORR_THRESHOLD.

    Returns:
        dict: dictionary with correlation metrics and diagnostics
    """

    df_corr = df.corr()

    avg_per_ticker_corr = df_corr.mean()
    low_corr_tickers = avg_per_ticker_corr[(avg_per_ticker_corr < low_corr_threshold)].index.tolist()

    status = "PASS" if (0.3 < df_corr.values.mean() <= 0.8 and len(low_corr_tickers) == 0) else "FAIL"

    corr_metrics = {
        "corr_matrix": df_corr,
        "avg_corr": df_corr.values.mean(),
        "std_corr": df_corr.values.std(),
        "min_corr": df_corr.values.min(),
        "max_corr": df_corr.values.max(),
        "avg_corr_per_ticker": avg_per_ticker_corr,
        "low_corr_tickers": low_corr_tickers,
        "status": status,
    }

    return corr_metrics


def extreme_returns_diagnostics(
    df: pd.DataFrame, threshold_10: float = EXTREME_THRESHOLD_10, threshold_25: float = EXTREME_THRESHOLD_25
) -> dict:
    """Identify extreme events in the dataframe

    This functions determines if the given dataframe contains extreme events to distinguish real market events from potential data errors, and flagging "stress dates" where the whole sector moved violently

    Args:
        df (pd.DataFrame): dataframe with ticker information indexed by time
        threshold_10 (float): Return magnitude threshold for stress date detection (e.g. 0.10 = 10%). Defaults to EXTREME_THRESHOLD_10.
        threshold_25 (float): Return magnitude threshold for suspicious ticker detection (e.g. 0.25 = 25%). Defaults to EXTREME_THRESHOLD_25.

    Returns:
        dict: dictionary with extreme events metrics and diagnostics
    """
    mask_10 = df.abs() > threshold_10
    mask_25 = df.abs() > threshold_25

    extreme_10 = mask_10.sum()
    extreme_25 = mask_25.sum()

    breaches_per_day = mask_10.sum(axis=1)
    stress_dates = breaches_per_day[breaches_per_day >= 3].sort_values(ascending=False)

    worst_return_per_ticker = df.min()
    best_return_per_ticker = df.max()

    mask_25_non_stress = mask_25[~mask_25.index.isin(stress_dates.index)]
    suspicious_tickers = mask_25_non_stress.any()[mask_25_non_stress.any()].index.tolist()

    status = "PASS" if (len(suspicious_tickers) == 0) else "FAIL"

    extreme_metrics = {
        "extreme_10pct_per_ticker": extreme_10,
        "extreme_25pct_per_ticker": extreme_25,
        "stress_dates": stress_dates,
        "n_stress_dates": len(stress_dates),
        "worst_return_per_ticker": worst_return_per_ticker,
        "best_return_per_ticker": best_return_per_ticker,
        "suspicious_tickers": suspicious_tickers,
        "status": status,
    }

    return extreme_metrics


def distribution_diagnostics(df: pd.DataFrame):
    pass


def stationarity_test():
    pass


def run_data_diagnostics(df: pd.DataFrame):
    print("=" * 50)
    print("Data Diagnostcs - EDA")
    print("=" * 50)
