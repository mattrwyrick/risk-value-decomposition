"""
Ridge (low penalty)         L1_wt = 0.0
LASSO (high penalty)        L1_wt = 1.0
Elastic (medium penalty)    0.0 < L1_wt < 1.0
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm

from sklearn.preprocessing import PolynomialFeatures

from rfd.risk_indicators import RISK_TYPES, RISK_INDICATOR_MAPPINGS


DEFAULT_L1 = 0.50
DEFAULT_ALPHA = 0.20  # regularization


def get_linear_decomposition(target_series, df_inputs, add_constant=True, alpha=DEFAULT_ALPHA, L1_wt=DEFAULT_L1):
    """
    Return a linear decomposition of the time series data
    :param target_series:
    :param df_inputs:
    :param add_constant:
    :param alpha:
    :param L1_wt:
    :return:
    """
    X = sm.add_constant(df_inputs) if add_constant else df_inputs
    X.fillna(X.mean(), inplace=True)
    model = sm.OLS(target_series, X).fit_regularized(alpha=alpha, L1_wt=L1_wt)
    return model


def get_linear_proportion_df(df_results, param_names, param_values):
    """
    Return a proportional df based on the model params
    :param df_results:
    :param param_names:
    :param param_values:
    :return:
    """
    param_abs_values = [abs(float(v)) for v in param_values]
    param_value_total = float(sum(param_abs_values))
    param_proportion = [v / param_value_total for v in param_abs_values]

    key_value = [(param_names[i], param_proportion[i]) for i in range(len(param_names))]
    key_value.sort(key=lambda x: x[1], reverse=True)

    for name, proportion in key_value:
        value = (df_results[name] * proportion)
        df_results[name] = value

    ordered_columns = [kv[0] for kv in key_value]
    return df_results, ordered_columns


def get_nonlinear_decomposition(target_series, df_inputs, add_constant=True, degree=2, alpha=DEFAULT_ALPHA, L1_wt=DEFAULT_L1):
    """
    Return a linear decomposition of the time series data
    :param target_series:
    :param df_inputs:
    :param add_constant:
    :param degree:
    :param alpha:
    :param L1_wt:
    :return:
    """
    original_column_names = df_inputs.columns.tolist()
    X_poly = PolynomialFeatures(degree=degree, include_bias=False).fit_transform(df_inputs)
    X_poly = pd.DataFrame(X_poly, columns=original_column_names)
    X_poly.fillna(X_poly.mean(), inplace=True)
    X_poly = sm.add_constant(X_poly, prepend=False) if add_constant else X_poly
    model = sm.OLS(target_series, X_poly).fit_regularized(alpha=alpha, L1_wt=L1_wt)
    return model


def get_nonlinear_proportion_df(df_results, param_names, param_values):
    """
    Return a proportional df based on the model params
    :param df_results:
    :param param_names:
    :param param_values:
    :return:
    """
    param_abs_values = [abs(float(v)) for v in param_values]
    param_value_total = float(sum(param_abs_values))
    param_proportion = [v / param_value_total for v in param_abs_values]

    key_value = [(param_names[i], param_proportion[i]) for i in range(len(param_names))]
    key_value.sort(key=lambda x: x[1], reverse=True)

    for name, proportion in key_value:
        value = (df_results[name] * proportion)
        df_results[name] = value

    return df_results

