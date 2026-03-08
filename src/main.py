from src.config import START_DATE, END_DATE, SEMICONDUCTOR_TICKER
from src.data_ingestion import fetch_data

# lu_tickers = ["HLT", "IHG", "MAR", "WH", "CHH"]

df = fetch_data(SEMICONDUCTOR_TICKER, START_DATE, END_DATE)
print(df.tail())
