import numpy as np
import pandas as pd

from rfd.risks.raw import (
    EQUITY_MARKET_NAME,
    EQUITY_MARKET_COLOR,
    get_equity_market_risk
)

from rfd.settings import (
    DATE_COL,
    DEFAULT_YF_START_DATE,
    DEFAULT_YF_END_DATE,
    TIMES_MAPPING,
    TIMES_CHOICE
)

from rfd.tools.decomposition.pca import get_pca_components

NAME = "Equity Market Exposure"
COLOR = "rgb(150, 200, 150)"

RISKS = [EQUITY_MARKET_NAME]

DATA_MAPPINGS = {
    EQUITY_MARKET_NAME: get_equity_market_risk
}

COLOR_MAPPINGS = {
    EQUITY_MARKET_NAME: EQUITY_MARKET_COLOR
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
    df_risk = pd.DataFrame({NAME: component.reshape(-1)})
    df_risk.index = df.index

    if include_meta:
        return df_risk, loadings, explained_variance
    else:
        return df_risk


"""
3. Equity Market and Systematic Risk
This category represents equity market performance and the systematic risk exposure of the portfolio.

Equity Market: ^GSPC – S&P 500 Index, representing the performance of the U.S. equity market.
Beta: Calculated as the sensitivity of an asset's returns to market returns (systematic risk).
Group Name: Equity Market Exposure

Description: This group captures the stock market’s performance and the systematic risk (beta) of the portfolio relative to the market. The equity market index and beta are key to understanding how the portfolio moves in relation to broader stock market trends.


"""