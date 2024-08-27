import numpy as np
import pandas as pd
import datetime as dt
import plotly.io as pio
import plotly.express as px

from flask import render_template


from rfd.settings import get_yf_date, DEFAULT_YF_START_DATE, DEFAULT_YF_END_DATE, TIMES_CHOICE, DATE_COL

from rfd.tools import get_asset_data

from rfd.risk_indicators import RISK_TYPES, RISK_INDICATOR_MAPPINGS, get_risk_inputs_df

from rfd.decomposition.results import Results

from rfd.decomposition.ridge_lasso import (
    get_linear_decomposition,
    get_proportion_df,

    # get_nonlinear_decomposition,
    # get_nonlinear_proportion_df
)


TEMPLATE = "./home.html"
FILL_MISSING_DATES = True
FILL_MISSING_METHOD = "ffill"  # forward fill


def view(request, cache={}):
    """
    Create the home page
    :param request:
    :param cache: dict
    :return:
    """
    ticker, end_date, start_date, time_choice, normalize, l1_wt, alpha = get_values_from_request(request)
    cache = add_to_cache(cache, ticker, end_date, start_date, time_choice, normalize, l1_wt, alpha)

    if not (ticker and end_date and start_date and time_choice and l1_wt and alpha):
        return render_template(TEMPLATE, **cache)

    add_constant = True

    df_asset = get_asset_data(
        ticker=ticker,
        yf_start=start_date,
        yf_end=end_date
    )

    if FILL_MISSING_DATES:
        date_range = pd.date_range(start=end_date, end=start_date)  # plz fix (later)
        df_asset = df_asset.reindex(date_range)
        df_asset = df_asset.fillna(method=FILL_MISSING_METHOD)

    target_series = df_asset[ticker]
    date_series = df_asset[DATE_COL]

    df_risk_inputs = get_risk_inputs_df(
        risk_types=RISK_TYPES,
        yf_start=end_date,
        yf_end=start_date,
        time_choice=time_choice,
        normalize=normalize,
        include_date=False,
        include_const=add_constant,
        fill_missing_dates=FILL_MISSING_DATES,
        fill_missing_method=FILL_MISSING_METHOD
    )

    model = get_linear_decomposition(
        target_series=target_series,
        df_inputs=df_risk_inputs,
        alpha=alpha,
        L1_wt=l1_wt,
    )

    df_fit = pd.DataFrame()
    df_fit["Date"] = df_asset["Date"]

    param_values = np.abs(list(model.params))
    param_names = model.model.exog_names

    for i, col in enumerate(param_names):  # plz fix - add statistical tests to filter inputs prior
        fit_col = f"Fit {col}"
        df_fit[fit_col] = df_risk_inputs[col] * param_values[i]

    df_fit["Fit Idiosyncratic"] = np.abs(target_series - model.fittedvalues)

    df_proportions = get_proportion_df(df=df_risk_inputs, pfilter=False, threshold=0.0)

    df_results

    results = Results(
        dates=date_series,
        target_series=target_series,
        df_inputs=df_risk_inputs,
        ordered_columns=ordered_columns
    )

    fig_area = results.area_plot()
    html_area = pio.to_html(fig_area)

    fig_line = px.line(target_series)
    fig_line.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    fig_line.update_yaxes(range=[0, target_series.max() + (0.05 * np.mean(target_series))])
    html_line = pio.to_html(fig_line)

    cache["area_chart"] = html_area
    cache["line_chart"] = html_line

    return render_template(TEMPLATE, **cache)


def get_values_from_request(request):
    """
    Get the values from the request
    :param request:
    :return:
    """
    values = request.values

    ticker = values["ticker"].strip() if "ticker" in values else None
    time_choice = values["time_choice"].strip() if "time_choice" in values else None
    normalize = False if "normalize" in values and values["normalize"] == "No" else True

    try:
        end_date = values["end_date"].strip() if "end_date" in values else DEFAULT_YF_END_DATE
        if end_date:
            ymd = [int(p.strip()) for p in end_date.split("-")]  # MM/DD/YYYY
            dtime = dt.datetime(year=ymd[0], month=ymd[1], day=ymd[2])
            end_date = get_yf_date(dtime)
    except Exception as e:
        end_date = None

    try:
        start_date = values["start_date"].strip() if "start_date" in values else DEFAULT_YF_START_DATE
        if start_date:
            ymd = [int(p.strip()) for p in start_date.split("-")]  # MM/DD/YYYY
            dtime = dt.datetime(year=ymd[0], month=ymd[1], day=ymd[2])
            start_date = get_yf_date(dtime)
    except Exception as e:
        start_date = None

    try:
        l1_wt = float(values["l1_wt"].strip()) if "l1_wt" in values else None
    except:
        l1_wt = None

    try:
        alpha = float(values["alpha"].strip()) if "alpha" in values else None
    except:
        alpha = None

    return ticker, end_date, start_date, time_choice, normalize, l1_wt, alpha


def add_to_cache(cache, ticker=None, end_date=None, start_date=None, time_choice=None,
                 normalize=None, l1_wt=None, alpha=None):
    """
    Add values to the cache
    :param cache:
    :param ticker:
    :param end_date:
    :param start_date:
    :param time_choice:
    :param normalize:
    :param l1_wt:
    :param alpha:
    :return:
    """
    if ticker:
        cache["ticker"] = ticker
    if end_date:
        cache["end_date"] = end_date
    if start_date:
        cache["start_date"] = start_date
    if time_choice:
        cache["time_choice"] = time_choice

    if normalize:
        cache["normalize"] = "Yes"
    else:
        cache["normalize"] = "No"

    if l1_wt:
        cache["l1_wt"] = l1_wt
    if alpha:
        cache["alpha"] = alpha
    return cache
