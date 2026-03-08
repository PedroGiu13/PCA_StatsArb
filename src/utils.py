import pandas as pd
import numpy as np
from pathlib import Path


def transform_log_returns(df, cache_dir: str = "data/processed") -> pd.DataFrame:
    """Function to transform asset prices to log retruns

    This function creates a new dataframe with log retruns of each asset. It takes the asset price dataframe as an input, checks if the log retruns file already exists, and returns a new dataframe with the prices transformation.

    Args:
        df (_type_): asset prices dataframe
        cache_dir (str, optional): directory to save the file Defaults to "data/processed".

    Returns:
        pd.DataFrame: log returns df
    """
    # Set parent directory
    file_dir = Path(cache_dir)
    file_dir.mkdir(parents=True, exist_ok=True)

    file_name = "log_returns.parquet"
    file_path = file_dir / file_name

    if file_path.exists():
        print("\nData already transformed")
        return pd.read_parquet(file_path)

    else:
        print("\nTransforming asset prices")
        # Make log tranformation
        df_returns = np.log(df / df.shift(1))
        df_returns = df_returns.dropna()

        df_returns.to_parquet(file_path, engine="pyarrow", compression="snappy")
        return df_returns
