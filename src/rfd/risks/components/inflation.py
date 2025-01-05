
import numpy as np
import pandas as pd

from rfd.risks.raw import (
    INFLATION_NAME,
    INFLATION_COLOR,
    get_inflation_risk
)

from rfd.settings import (
    DATE_COL,
    DEFAULT_YF_START_DATE,
    DEFAULT_YF_END_DATE,
    TIMES_MAPPING,
    TIMES_CHOICE
)

from rfd.tools.decomposition.pca import get_pca_components

NAME = "Inflation Risk"
COLOR = "rgb(200, 200, 150)"

RISKS = [INFLATION_NAME]

DATA_MAPPINGS = {
    INFLATION_NAME: get_inflation_risk
}

COLOR_MAPPINGS = {
    INFLATION_NAME: INFLATION_COLOR
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
4. Inflation and Inflation-Protected Securities
This group captures the risk associated with inflation and how it affects bonds and other financial instruments.

Inflation: TIP – iShares TIPS Bond ETF, representing inflation-protected bonds (TIPS), which hedge against inflation.
Group Name: Inflation Risk

Description: This group captures inflation risk and how rising prices can affect real bond yields and portfolio performance. TIPS are used to hedge against unexpected inflation.
"""