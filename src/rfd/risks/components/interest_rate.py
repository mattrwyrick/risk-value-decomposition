import numpy as np
import pandas as pd

from rfd.risks.raw import (
    INTEREST_RATE_13W_NAME,
    INTEREST_RATE_13W_COLOR,
    get_interest_rate_13w_risk,

    INTEREST_RATE_5Y_NAME,
    INTEREST_RATE_5Y_COLOR,
    get_interest_rate_5y_risk,

    INTEREST_RATE_10Y_NAME,
    INTEREST_RATE_10Y_COLOR,
    get_interest_rate_10y_risk,

    INTEREST_RATE_30Y_NAME,
    INTEREST_RATE_30Y_COLOR,
    get_interest_rate_30y_risk
)

from rfd.settings import (
    DATE_COL,
    DEFAULT_YF_START_DATE,
    DEFAULT_YF_END_DATE,
    TIMES_MAPPING,
    TIMES_CHOICE
)

from rfd.tools.decomposition.pca import get_pca_components

NAME = "Yield Curve Dynamics"
COLOR = "rgb(200, 150, 150)"

RISKS = [INTEREST_RATE_13W_NAME, INTEREST_RATE_5Y_NAME, INTEREST_RATE_10Y_NAME, INTEREST_RATE_30Y_NAME]

DATA_MAPPINGS = {
    INTEREST_RATE_13W_NAME: get_interest_rate_13w_risk,
    INTEREST_RATE_5Y_NAME: get_interest_rate_5y_risk,
    INTEREST_RATE_10Y_NAME: get_interest_rate_10y_risk,
    INTEREST_RATE_30Y_NAME: get_interest_rate_30y_risk
}

COLOR_MAPPINGS = {
    INTEREST_RATE_13W_NAME: INTEREST_RATE_13W_COLOR,
    INTEREST_RATE_5Y_NAME: INTEREST_RATE_5Y_COLOR,
    INTEREST_RATE_10Y_NAME: INTEREST_RATE_10Y_COLOR,
    INTEREST_RATE_30Y_NAME: INTEREST_RATE_30Y_COLOR
}


def get_risk(
        yf_start=DEFAULT_YF_START_DATE,
        yf_end=DEFAULT_YF_END_DATE,
        time_choice=TIMES_CHOICE,
        normalize=True,
        include_date=False,
        include_meta=True
):
    """
    Return the risk indicator time series for the given daterange
    :param yf_start:
    :param yf_end:
    :param time_choice:
    :param normalize:
    :param include_date:
    :param include_meta:
    :return:
    """
    df = pd.DataFrame()

    for risk in RISKS:
        df[risk] = DATA_MAPPINGS[risk](
            yf_start=yf_start,
            yf_end=yf_end,
            time_choice=time_choice,
            normalize=normalize,
            include_date=include_date
        )

    component, loadings, explained_variance = get_pca_components(df, n_components=1, include_meta=True)
    component.index = df.index

    if include_meta:
        return component, loadings, explained_variance
    else:
        return component

"""
1. Interest Rate and Yield Curve
This category groups variables that represent the bond market's response to changes in interest rates across different maturities. These rates are key drivers of fixed-income market movements and bond valuations.

Interest Rate (5y): ^FVX – 5-year Treasury bill yield, representing medium-term interest rates.
Interest Rate (10y): ^TNX – 10-year Treasury bill yield, representing long-term interest rates and commonly used as a benchmark for bond pricing.
Interest Rate (13w): ^IRX – 13-week Treasury bill yield, representing short-term interest rates and liquidity preferences.
Interest Rate (30y): ^TYX – 30-year Treasury bill yield, representing very long-term interest rates and future inflation expectations.
Group Name: Yield Curve Dynamics

Description: This group captures the sensitivity of the financial system to changes in interest rates across different maturities, reflecting the term structure of interest rates (yield curve). These factors influence the pricing of bonds, equities, and borrowing costs.
"""
