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

NAME = "Baseline"
COLOR = "rgb(200, 200, 200)"

def get_risk(yf_start=DEFAULT_YF_START_DATE, yf_end=DEFAULT_YF_END_DATE, time_choice=TIMES_CHOICE, normalize=True, include_date=False):
    """
    Return the risk indicator time series for the given daterange
    :param yf_start: str YYYY-MM-DD
    :param yf_end: str YYYY-MM-DD
    :parma time_choice: str (Close, Open, Mean)
    :param include_date: bool
    :return: np.Array
    """
    date_range = pd.date_range(start=yf_start, end=yf_end)
    df = pd.DataFrame(date_range, columns=['Date'])
    df.set_index('Date', inplace=True)
    df[NAME] = 1.0
    return df
