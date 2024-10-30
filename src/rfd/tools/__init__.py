import pandas as pd
import numpy as np
import yfinance as yf

from rfd.settings import (
    DEFAULT_YF_START_DATE,
    DEFAULT_YF_END_DATE,
    TIMES_MAPPING,
    TIMES_CHOICE,
    DATE_COL
)


def get_asset_data(ticker, yf_start=DEFAULT_YF_START_DATE, yf_end=DEFAULT_YF_END_DATE, time_choice=TIMES_CHOICE, normalize=True):
    """
    Get the asset data from yfinance
    :param ticker:
    :param yf_start:
    :param yf_end:
    :param time_choice:
    :param normalize:
    :return:
    """
    company = yf.Ticker(ticker)
    company_name = company.info['longName']

    df = pd.DataFrame()
    df_tmp = yf.download(ticker, start=yf_end, end=yf_start)  # plz fix (later)
    df.index = df_tmp.index
    df[DATE_COL] = df.index
    df[ticker] = TIMES_MAPPING[time_choice](df_tmp)
    if normalize:
        df[ticker] = df[ticker] / df[ticker].mean()
    return df


def get_proportion_df(df_fit):
    """
    Return df that contains the proportions of each params influence
    :param df_fit:
    :return:
    """
    df_proportions = pd.DataFrame()
    df_proportions["Date"] = df_fit["Date"]



