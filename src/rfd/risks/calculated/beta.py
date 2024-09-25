import numpy as np
import pandas as pd

# Example: ETF price and S&P 500 Index price
etf_returns = etf_data['Close'].pct_change()  # daily returns of ETF
market_returns = sp500_data['Close'].pct_change()  # daily returns of S&P 500

# Calculate the covariance between ETF and market returns
cov_matrix = np.cov(etf_returns[1:], market_returns[1:])  # ignoring first NaN

# Extract covariance and market variance
covariance = cov_matrix[0, 1]
market_variance = cov_matrix[1, 1]

# Calculate Beta
beta = covariance / market_variance
print(f"Beta: {beta}")



import pandas as pd
import numpy as np
import yfinance as yf

from rfd.settings import (
    DATE_COL,
    DEFAULT_YF_START_DATE,
    DEFAULT_YF_END_DATE,
    TIMES_MAPPING,
    TIMES_CHOICE
)

NAME = "Idiosyncratic"
COLOR = "rgb(255, 99, 71)"


def get_risk(yf_start=DEFAULT_YF_START_DATE, yf_end=DEFAULT_YF_END_DATE, time_choice=TIMES_CHOICE, normalize=True, include_date=False):
    """
    Return the risk indicator time series for the given daterange
    :param yf_start: str YYYY-MM-DD
    :param yf_end: str YYYY-MM-DD
    :parma time_choice: str (Close, Open, Mean)
    :param include_date: bool
    :return: np.Array
    """
    return None