import pandas as pd
import yfinance as yf
from pathlib import Path


def fetch_data(tickers: list[str], start_date: str, end_date: str, cache_dir: str = "data/raw") -> pd.DataFrame:
    """Function that retrieves the adjusted closing price from the yahoo finance API, saves it, and retruns a dataframe.

    This function retrieves the adjusted closing prices of every ticker given in a list. If the data has not been fetched yet, it downloads it, saves it in the 'raw' data folder as a '.parquet' file, and it returns a dataframe. Otherwise, it directly returns the dataframe form the folder

    Args:
        tickers (list[str]): list of tickers
        start_date (str): start date
        end_date (str): end date
        cache_dir (str, optional): directory to save the file

    Returns:
        pd.DataFrame: dataframe with Adjusted Closing Price of every ticker
    """

    # Define parent folder to save the data
    file_dir = Path(cache_dir)
    file_dir.mkdir(parents=True, exist_ok=True)

    file_name = "raw_prices.parquet"
    file_path = file_dir / file_name

    # Check file existance
    if file_path.exists():
        print("Data already in memory")
        return pd.read_parquet(file_path)

    else:
        print(f"Fetching data for: {tickers}")
        try:
            prices = yf.download(
                tickers=tickers,
                start=start_date,
                end=end_date,
                auto_adjust=True,
                progress=True,
                multi_level_index=False,
            )["Close"]

            prices.to_parquet(file_path, engine="pyarrow", compression="snappy")

            return prices

        except Exception as e:
            raise RuntimeError(f"Unable to fetch {tickers}. {e}")
