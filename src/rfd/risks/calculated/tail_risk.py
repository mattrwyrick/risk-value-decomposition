from scipy.stats import skew, kurtosis

# Calculate daily returns of the ETF
etf_returns = etf_data['Close'].pct_change().dropna()

# Calculate skewness and kurtosis
skewness = skew(etf_returns)
kurt = kurtosis(etf_returns, fisher=False)  # Fisher=False for Pearson Kurtosis

print(f"Skewness: {skewness}")
print(f"Kurtosis: {kurt}")


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
COLOR1 = "rgb(110, 160, 160)"
COLOR2 = "rgb(90, 140, 140)"

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