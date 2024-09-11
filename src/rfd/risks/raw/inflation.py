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

NAME = "Inflation Risk"
COLOR = "rgb(255, 215, 0)"


def get_risk(yf_start=DEFAULT_YF_START_DATE, yf_end=DEFAULT_YF_END_DATE, time_choice=TIMES_CHOICE, normalize=True, include_date=False):
    """
    Return the risk indicator time series for the given daterange
    :param yf_start: str YYYY-MM-DD
    :param yf_end: str YYYY-MM-DD
    :parma time_choice: str (Close, Open, Mean)
    :param include_date: bool
    :return: np.Array
    """
    ticker = "TIP"  #  iShares TIPS Bond ETF (TIP)

    company = yf.Ticker(ticker)
    company_name = company.info['longName']

    df = pd.DataFrame()
    df_tmp = yf.download(ticker, start=yf_start, end=yf_end)
    df.index = df_tmp.index
    if include_date:
        df[DATE_COL] = df.index
    df[NAME] = TIMES_MAPPING[time_choice](df_tmp)
    if normalize:
        df[NAME] = df[NAME] / df[NAME].mean()
    return df
