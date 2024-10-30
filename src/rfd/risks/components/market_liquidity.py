
import numpy as np
import pandas as pd

from rfd.risks.raw import (
    MARKET_LIQUIDITY_NAME,
    MARKET_LIQUIDITY_COLOR,
    get_market_liquidity_risk
)

from rfd.settings import (
    DATE_COL,
    DEFAULT_YF_START_DATE,
    DEFAULT_YF_END_DATE,
    TIMES_MAPPING,
    TIMES_CHOICE
)

from rfd.decomposition.pca import get_pca_components

NAME = "Liquidity Risk"
COLOR = "rgb(150, 150, 200)"

RISKS = [MARKET_LIQUIDITY_NAME]

DATA_MAPPINGS = {
    MARKET_LIQUIDITY_NAME: get_market_liquidity_risk
}

COLOR_MAPPINGS = {
    MARKET_LIQUIDITY_NAME: MARKET_LIQUIDITY_COLOR
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
5. Market Liquidity
This group represents liquidity risk, focusing on how easily assets can be traded without affecting prices.

Market Liquidity: LQD – iShares Investment Grade Corporate Bond ETF, which tracks liquidity conditions in the corporate bond market. You may want to consider adding a commercial paper spread to capture short-term corporate liquidity.
Group Name: Liquidity Risk

Description: This group focuses on the ability to buy or sell assets without large price changes, representing liquidity conditions in the bond market and overall market stress levels.


"""