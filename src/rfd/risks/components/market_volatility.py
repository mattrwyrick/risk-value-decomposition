


import pandas as pd
import numpy as np
import yfinance as yf


from rfd.risks.raw import (
    MARKET_VOLATILITY_NAME,
    MARKET_VOLATILITY_COLOR,
    get_market_volatility_risk
)

from rfd.settings import (
    DATE_COL,
    DEFAULT_YF_START_DATE,
    DEFAULT_YF_END_DATE,
    TIMES_MAPPING,
    TIMES_CHOICE
)

from rfd.tools.decomposition.pca import get_pca_components


NAME = "Volatility and Tail Risk"
COLOR = "rgb(150, 200, 200)"

RISKS = [MARKET_VOLATILITY_NAME]

DATA_MAPPINGS = {
    MARKET_VOLATILITY_NAME: get_market_volatility_risk
}

COLOR_MAPPINGS = {
    MARKET_VOLATILITY_NAME: MARKET_VOLATILITY_COLOR
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
6. Market Volatility and Tail Risk
This category captures volatility and tail risks, which measure the likelihood of extreme market events and deviations from normal market behavior.

Market Volatility: ^VIX – CBOE Vix Index, representing expected stock market volatility (often called the "fear index").
Tail Risk (Skew): Measures the asymmetry of the return distribution, indicating the likelihood of extreme negative events.
Tail Risk (Kurtosis): Measures the fat-tailedness of return distributions, indicating the likelihood of extreme deviations from the mean.
Group Name: Volatility and Tail Risk

Description: This group captures market uncertainty, extreme risk events, and the overall level of volatility. The VIX measures expected market volatility, while skewness and kurtosis capture the likelihood of rare, extreme events.
"""