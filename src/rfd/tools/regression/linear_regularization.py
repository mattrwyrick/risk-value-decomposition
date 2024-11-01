"""
Ridge (high penalty)        L1_wt = 1.0
Elastic (medium penalty)    0.33 < L1_wt < 0.66
LASSO (low penalty)         L1_wt = 0.0
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm

from settings import DATE_COL

PARAMS = {
    "ridge": {
        "alpha": 1.25,
        "L1_wt": 0.90
    },
    "lasso": {
        "alpha": 0.25,
        "L1_wt": 0.10
    },
    "elastic": {
        "alpha": 0.75,
        "L1_wt": 0.50
    }
}


DEFAULT_ALPHA = PARAMS["ridge"]["alpha"]
DEFAULT_L1 = PARAMS["ridge"]["L1_wt"]


def get_fit(target_series, df_inputs, alpha=DEFAULT_ALPHA, L1_wt=DEFAULT_L1, model=None):
    """
    Return a linear decomposition of the time series data
    :param target_series:
    :param df_inputs:
    :param alpha:
    :param L1_wt:
    :param model: ["ridge", "lasso", "elastic"]
    :return:
    """
    if model and (model in PARAMS) and (alpha == DEFAULT_L1 and L1_wt == DEFAULT_L1):
        alpha = PARAMS[model]["alpha"]
        L1_wt = PARAMS[model]["L1_wt"]
    # model = sm.OLS(target_series, df_inputs).fit_regularized(alpha=alpha, L1_wt=L1_wt)
    model = sm.OLS(target_series, df_inputs).fit()
    return model


def get_proportion_df(asset_series, results, columns, pfilter=False, threshold=0.0):
    """
    Return a proportional df
    :param df:
    :param pfilter:
    :param threshold:
    :return:
    """
    c=1
    df = pd.DataFrame()
    df.index = df.index
    fit = results.fittedvalues
    residuals = results.resid

    params_abs = np.abs(list(results.params))
    params_total = np.sum(params_abs)
    params_scaled = params_abs / params_total

    for i, col in enumerate(columns):
        df[col] = asset_series * params_scaled[i]

    return df
