import pandas as pd
import numpy as np

from rfd.settings import DEFAULT_YF_START_DATE, DEFAULT_YF_END_DATE, TIMES_CHOICE

from rfd.risks import get_raw_risk_inputs_df

from rfd.tools.regression.linear_regularization import get_fit, get_proportion_df


def get_decomposition_df(
        asset_series,
        yf_start=DEFAULT_YF_START_DATE,
        yf_end=DEFAULT_YF_END_DATE,
        time_choice=TIMES_CHOICE,
        normalize=True,
        include_const=True,
        include_date=False,
        fill_missing_dates=False,
        fill_missing_method="ffill"
):
    """
    Return the raw risk decomposition
    :param yf_start:
    :param yf_end:
    :param time_choice:
    :param normalize:
    :param include_const:
    :param include_date:
    :param fill_missing_dates:
    :param fill_missing_method:
    :return:
    """
    df_risks = get_raw_risk_inputs_df(
        yf_start=yf_start,
        yf_end=yf_end,
        time_choice=time_choice,
        normalize=normalize,
        include_const=include_const,
        include_date=include_date,
        fill_missing_dates=fill_missing_dates,
        fill_missing_method=fill_missing_method
    )

    results = get_fit(asset_series, df_risks)
    df_proportions = get_proportion_df(asset_series, results)
    return df_proportions




