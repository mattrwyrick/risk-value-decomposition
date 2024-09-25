import numpy as np
import pandas as pd

from rfd.risks.raw import (
    BOND_MARKET_NAME,
    BOND_MARKET_COLOR,
    get_bond_market_risk,

    BOND_MARKET_HY_NAME,
    BOND_MARKET_HY_COLOR,
    get_bond_market_hy_risk
)

from rfd.settings import (
    DATE_COL,
    DEFAULT_YF_START_DATE,
    DEFAULT_YF_END_DATE,
    TIMES_MAPPING,
    TIMES_CHOICE
)

from rfd.decomposition.pca import get_pca_components


NAME = "Credit and Bond Market Risk"
COLOR = "rgb(0, 0, 0)"

RISKS = [BOND_MARKET_NAME, BOND_MARKET_HY_NAME]

DATA_MAPPINGS = {
    BOND_MARKET_NAME: get_bond_market_risk,
    BOND_MARKET_HY_NAME: get_bond_market_hy_risk
}

COLOR_MAPPINGS = {
    BOND_MARKET_NAME: BOND_MARKET_COLOR,
    BOND_MARKET_HY_NAME: BOND_MARKET_HY_COLOR
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
2. Bond Market and Credit Risk
These variables represent different aspects of the bond market, including investment-grade and high-yield bonds, as well as credit risk (spreads between corporate and Treasury yields).

Bond Market: AGG – iShares U.S. Aggregate Bond ETF, representing the investment-grade bond market.
Bond Market (High-Yield): JNK – BlackRock High-Yield Bond ETF, representing high-risk, high-yield corporate bonds.
Credit Spread: Calculated as the difference between corporate bond yields and risk-free Treasury yields, indicating the market’s perception of credit risk.
Group Name: Credit and Bond Market Risk

Description: This group focuses on bond market performance and the risk associated with corporate credit. It includes investment-grade bonds, high-yield bonds, and the spread that reflects the premium for taking on credit risk."""
