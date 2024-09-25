import pandas as pd

# Example: Load Treasury and Corporate bond yield data
treasury_yield = pd.read_csv('treasury_yield.csv')  # Data from FRED
corp_bond_yield = pd.read_csv('corp_bond_yield.csv')  # Corporate bond yields from FRED

# Calculate Credit Spread (Corporate Bond Yield - Treasury Yield)
credit_spread = corp_bond_yield['Yield'] - treasury_yield['Yield']
data['Credit_Spread'] = credit_spread


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