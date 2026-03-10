from datetime import datetime

# Date Defaults
START_DATE = "2015-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")


# Stock Allocation
TICKERS_LIST = [
    "NVDA",
    "AMD",
    "INTC",
    "QCOM",
    "AVGO",
    "TXN",
    "MU",
    "MRVL",
    "ADI",
    "NXPI",
    "ON",
    "MPWR",
    "SWKS",
    "QRVO",
    "CRUS",
    "SLAB",
    "MCHP",
    "STM",
    "SMTC",
    "LSCC",
]

UNIVERSE_SIZE = len(TICKERS_LIST)


# Diagnostics Checks
MIN_HISTORY_DAYS = 2500
MISSING_DATA_THRESHOLD = 0.02
LOW_CORR_THRESHOLD = 0.2
EXTREME_THRESHOLD_10 = 0.10
EXTREME_THRESHOLD_25 = 0.25
