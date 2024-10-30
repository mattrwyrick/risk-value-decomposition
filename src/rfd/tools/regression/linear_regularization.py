"""
Ridge (high penalty)        L1_wt = 1.0
Elastic (medium penalty)    0.33 < L1_wt < 0.66
LASSO (low penalty)         L1_wt = 0.0
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm


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
    model = sm.OLS(target_series, df_inputs).fit_regularized(alpha=alpha, L1_wt=L1_wt)
    return model


def get_proportion_df(df, pfilter=False, threshold=0.0):
    """
    Return a proportional df
    :param df:
    :param pfilter:
    :param threshold:
    :return:
    """
    columns = [col for col in df.columns if col.lower().strip() != "date"]
    df["Total"] = df[columns].sum(axis=1)

    df_proportions = pd.DataFrame()
    df_proportions.index = df.index

    for col in columns:
        mean = df[col].mean()
        if pfilter:
            if mean >= threshold:
                new_col = f"% {col}"
                df_proportions[new_col] = np.divide(
                    df[col],
                    df["Total"],
                    out=np.zeros_like(df[col]),
                    where=df["Total"] != 0
                )

        else:
            new_col = f"% {col}"
            df_proportions[new_col] = np.divide(
                df[col],
                df["Total"],
                out=np.zeros_like(df[col]),
                where=df["Total"] != 0
            )

    return df_proportions