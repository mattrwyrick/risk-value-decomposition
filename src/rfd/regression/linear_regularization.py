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
    # df_proportions["Date"] = df["Date"]
    # df_proportions.set_index('Date', inplace=True)

    for col in columns:
        mean = df[col].mean()
        if pfilter:
            if mean >= threshold:
                new_col = f"% {col}"
                # df_proportions[new_col] = np.where(df[df["Total"]] != 0.0, df[col] / df["Total"], 0.0)
                df_proportions[new_col] = np.divide(
                    df[col],
                    df["Total"],
                    out=np.zeros_like(df[col]),
                    where=df["Total"] != 0
                )

        else:
            new_col = f"% {col}"
            # df_proportions[new_col] = np.where(df[df["Total"]] != 0.0, df[col] / df["Total"], 0.0)
            df_proportions[new_col] = np.divide(
                df[col],
                df["Total"],
                out=np.zeros_like(df[col]),
                where=df["Total"] != 0
            )

    return df_proportions


def get_results_df(target_series, df_proportions):
    """
    Return the results data frame based on the target series and input proportions
    :param target_series:
    :param df_proportions:
    :return:
    """
    df_results = pd.DataFrame()
    df_proportions.index = df_proportions.index
    for col in df_proportions.columns:
        if col.startswith("%"):
            new_col = col.split("% ")[-1]
            df_results[new_col] = target_series * df_proportions[col]
    return df_results

#
#
#     param_abs_values = [abs(float(v)) for v in param_values]
#     param_value_total = float(sum(param_abs_values))
#     param_proportion = [v / param_value_total for v in param_abs_values]
#
#     key_value = [(param_names[i], param_proportion[i]) for i in range(len(param_names))]
#     key_value.sort(key=lambda x: x[1], reverse=True)
#
#     for name, proportion in key_value:
#         value = (df_results[name] * proportion)
#         df_results[name] = value
#
#     ordered_columns = [kv[0] for kv in key_value]
#     return df_results, ordered_columns
#
# #
# def get_nonlinear_decomposition(target_series, df_inputs, add_constant=True, degree=2, alpha=DEFAULT_ALPHA, L1_wt=DEFAULT_L1):
#     """
#     Return a linear decomposition of the time series data
#     :param target_series:
#     :param df_inputs:
#     :param add_constant:
#     :param degree:
#     :param alpha:
#     :param L1_wt:
#     :return:
#     """
#     original_column_names = df_inputs.columns.tolist()
#     X_poly = PolynomialFeatures(degree=degree, include_bias=False).fit_transform(df_inputs)
#     X_poly = pd.DataFrame(X_poly, columns=original_column_names)
#     X_poly.fillna(X_poly.mean(), inplace=True)
#     X_poly = sm.add_constant(X_poly, prepend=False) if add_constant else X_poly
#     model = sm.OLS(target_series, X_poly).fit_regularized(alpha=alpha, L1_wt=L1_wt)
#     return model
#
#
# def get_nonlinear_proportion_df(df_results, param_names, param_values):
#     """
#     Return a proportional df based on the model params
#     :param df_results:
#     :param param_names:
#     :param param_values:
#     :return:
#     """
#     param_abs_values = [abs(float(v)) for v in param_values]
#     param_value_total = float(sum(param_abs_values))
#     param_proportion = [v / param_value_total for v in param_abs_values]
#
#     key_value = [(param_names[i], param_proportion[i]) for i in range(len(param_names))]
#     key_value.sort(key=lambda x: x[1], reverse=True)
#
#     for name, proportion in key_value:
#         value = (df_results[name] * proportion)
#         df_results[name] = value
#
#     return df_results
#


# plz fix - akaike information criterion (aic) and bayesian information criterion (bic)
