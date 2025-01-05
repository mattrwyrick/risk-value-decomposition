import pandas as pd
import numpy as np
import yfinance as yf

from rfd.risks.raw import (
    get_interest_rate_13w_risk,
    INTEREST_RATE_13W_NAME,

    get_interest_rate_5y_risk,
    INTEREST_RATE_5Y_NAME,

    get_interest_rate_10y_risk,
    INTEREST_RATE_10Y_NAME,

    get_interest_rate_30y_risk,
    INTEREST_RATE_30Y_NAME,
)

from rfd.settings import (
    DATE_COL,
    DEFAULT_YF_START_DATE,
    DEFAULT_YF_END_DATE,
    TIMES_MAPPING,
    TIMES_CHOICE
)

TREASURY_NAME = "Treasury"
BOND_NAME = "Bond"

NAME = "Credit Spread"  # bond
COLOR = "rgb(140, 140, 140)"

def get_risk(yf_start=DEFAULT_YF_START_DATE, yf_end=DEFAULT_YF_END_DATE, time_choice=TIMES_CHOICE, normalize=True, include_date=False):
    """
    Return the risk indicator time series for the given daterange
    :param yf_start: str YYYY-MM-DD
    :param yf_end: str YYYY-MM-DD
    :parma time_choice: str (Close, Open, Mean)
    :param include_date: bool
    :return: np.Array
    """
    start_date = pd.to_datetime(yf_start)
    end_date = pd.to_datetime(yf_end)

    years = (end_date - start_date).days / 365.25

    treasury_tickers = {
        1: get_interest_rate_13w_risk,
        2: get_interest_rate_5y_risk,
        5: get_interest_rate_10y_risk,
        10: get_interest_rate_30y_risk
    }

    if years < 2:
        df_tmp_1 = treasury_tickers[1](yf_start, yf_end, time_choice, normalize, include_date)
        t_name = INTEREST_RATE_13W_NAME
    elif years < 5:
        df_tmp_1 = treasury_tickers[2](yf_start, yf_end, time_choice, normalize, include_date)
        t_name = INTEREST_RATE_5Y_NAME
    elif years < 10:
        df_tmp_1 = treasury_tickers[5](yf_start, yf_end, time_choice, normalize, include_date)
        t_name = INTEREST_RATE_10Y_NAME
    else:
        df_tmp_1 = treasury_tickers[10](yf_start, yf_end, time_choice, normalize, include_date)
        t_name = INTEREST_RATE_30Y_NAME

    df_tmp_1[TREASURY_NAME] = df_tmp_1[t_name]

    if normalize:
        df_tmp_1[TREASURY_NAME] = df_tmp_1[TREASURY_NAME] / df_tmp_1[TREASURY_NAME].mean()


    ticker = "LQD"  # iShares iBoxx $ Investment Grade Corporate Bond ETF
    df_tmp_2 = yf.download(ticker, start=yf_start, end=yf_end)
    df_tmp_1[BOND_NAME] = TIMES_MAPPING[time_choice](df_tmp_2)
    if normalize:
        df_tmp_1[BOND_NAME] = df_tmp_2[BOND_NAME] / df_tmp_2[BOND_NAME].mean()


    df = pd.DataFrame()
    df[NAME] = df_tmp_1[BOND_NAME] - df_tmp_1[TREASURY_NAME]
    if include_date:
        df[DATE_COL] = df_tmp_1[DATE_COL]
        df.index = df_tmp_1.index

    return df