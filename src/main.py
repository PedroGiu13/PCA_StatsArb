from src.config import START_DATE, END_DATE, TICKERS_LIST
from src.data_ingestion import fetch_data
from src.utils import transform_log_returns


def run_pipeline():
    # ===== Stage 1: Data preprocessing =====
    # Fetch asset prices
    df_prices = fetch_data(TICKERS_LIST, START_DATE, END_DATE)

    # Transform prices -> log returns
    df_returns = transform_log_returns(df_prices)

    # Data Inspection


if __name__ == "__main__":
    run_pipeline()
