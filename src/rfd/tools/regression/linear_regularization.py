"""
Ridge (high penalty)        L1_wt = 1.0
Elastic (medium penalty)    0.33 < L1_wt < 0.66
LASSO (low penalty)         L1_wt = 0.0
"""
import logging

import numpy as np
import pandas as pd
import statsmodels.api as sm

from flask import current_app

from rfd.risks.raw.baseline import NAME as BASELINE_RISK_NAME
from rfd.settings import IDIOSYNCRATIC_RISK_NAME

from rfd.settings import DATE_COL

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

    target_series = target_series.dropna()
    df_inputs = df_inputs.dropna()

    n_target = len(target_series)
    n_inputs = df_inputs.shape[0]

    if n_target < n_inputs:
        df_inputs = df_inputs.iloc[n_inputs - n_target:]
    elif n_target > n_inputs:
        target_series = target_series[n_inputs - n_target:]
    model = sm.OLS(target_series, df_inputs).fit()
    return model


def get_proportion_df(asset_series, results, columns, pfilter=False, threshold=0.03):
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
    residuals_abs = np.abs(list(residuals))
    residual_coeff = np.mean(residuals_abs)
    columns.append(IDIOSYNCRATIC_RISK_NAME)

    params_abs = np.abs(list(results.params) + [residual_coeff])
    params_total = np.sum(params_abs + [residual_coeff])
    params_scaled = params_abs / params_total

    if threshold:
        keep_params = list()
        keep_columns = list()
        for value, col in zip(params_scaled, columns):
            if value >= threshold or col in [BASELINE_RISK_NAME, IDIOSYNCRATIC_RISK_NAME]:
                keep_params.append(value)
                keep_columns.append(col)

        params_total = np.sum(keep_params)
        params_scaled = keep_params / params_total
        columns = keep_columns

    for i, col in enumerate(columns):
        df[col] = np.full(len(asset_series), params_scaled[i])

    val_col = sorted(zip(params_scaled, columns), reverse=True)
    sorted_cols = [pair[1] for pair in val_col if pair[1] not in [BASELINE_RISK_NAME, IDIOSYNCRATIC_RISK_NAME]]

    if IDIOSYNCRATIC_RISK_NAME in columns:
        sorted_cols.insert(0, IDIOSYNCRATIC_RISK_NAME)
    if BASELINE_RISK_NAME in columns:
        sorted_cols.insert(0, BASELINE_RISK_NAME)

    df = df[sorted_cols]
    proportion_dict = {col: value for col, value in val_col}

    return df, proportion_dict


def get_directional_df(asset_series, results, columns, pfilter=False, threshold=0.03):
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
    residuals_abs = np.abs(list(residuals))
    residual_coeff = np.mean(residuals_abs)
    columns.append(IDIOSYNCRATIC_RISK_NAME)

    params = list(results.params) + [residual_coeff]
    params_abs = np.abs(params)
    params_total = np.sum(params_abs + [residual_coeff])
    params_scaled = params_abs / params_total
    polarities = list()
    for value, scaled_value in zip(params, params_scaled):
        if value >= 0:
            polarities.append(1 * scaled_value)
        else:
            polarities.append(-1 * scaled_value)

    if threshold:
        keep_params = list()
        keep_columns = list()
        polarities = list()
        for value, scaled_value, col in zip(params, params_scaled, columns):
            if scaled_value >= threshold or col in [BASELINE_RISK_NAME, IDIOSYNCRATIC_RISK_NAME]:
                keep_params.append(scaled_value)
                keep_columns.append(col)

                if col in [BASELINE_RISK_NAME, IDIOSYNCRATIC_RISK_NAME]:
                    polarities.append(1 * scaled_value)  # really none but don't change coeff polarity
                elif value >= 0:
                    polarities.append(1 * scaled_value)
                else:
                    polarities.append(-1 * scaled_value)

        params_total = np.sum(keep_params)
        polarities = np.divide(polarities, params_total)

        columns = keep_columns

    for i, col in enumerate(columns):
        df[col] = np.full(len(asset_series), polarities[i])

    val_col = sorted(zip(polarities, columns), reverse=True)
    sorted_cols = [pair[1] for pair in val_col if pair[1] not in [BASELINE_RISK_NAME, IDIOSYNCRATIC_RISK_NAME]]

    if IDIOSYNCRATIC_RISK_NAME in columns:
        sorted_cols.insert(0, IDIOSYNCRATIC_RISK_NAME)
    if BASELINE_RISK_NAME in columns:
        sorted_cols.insert(0, BASELINE_RISK_NAME)

    df = df[sorted_cols]
    directional_dict = {col: value for col, value in val_col}

    return df, directional_dict
