from turtledemo.penrose import start

import numpy as np
import pandas as pd
import datetime as dt
import plotly.io as pio
import plotly.express as px

from flask import render_template

from rfd.settings import get_yf_date, DEFAULT_YF_START_DATE, DEFAULT_YF_END_DATE, TIMES_CHOICE, DATE_COL

from rfd.tools import get_asset_data

from rfd.process.decomposition import (
    get_raw_risks_decomposition_df,
    get_structured_risks_decomposition_df
)

from rfd.tools.plot.area import get_plot


TEMPLATE = "./decomposition.html"
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

    df_asset_raw = get_asset_data(
        ticker=ticker,
        yf_start=start_date,
        yf_end=end_date,
        normalize=False
    )

    df_asset = get_asset_data(
        ticker=ticker,
        yf_start=start_date,
        yf_end=end_date
    )

    if FILL_MISSING_DATES:
        date_range = pd.date_range(start=end_date, end=start_date)  # plz fix (later)
        df_asset = df_asset.reindex(date_range)
        df_asset = df_asset.fillna(method=FILL_MISSING_METHOD)
        df_asset["Date"] = df_asset.index

        df_asset_raw = df_asset_raw.reindex(date_range)
        df_asset_raw = df_asset_raw.fillna(method=FILL_MISSING_METHOD)
        df_asset_raw["Date"] = df_asset_raw.index

    df_asset_raw.dropna(inplace=True)
    df_asset.dropna(inplace=True)

    asset_series_raw = df_asset_raw[ticker]
    asset_series = df_asset[ticker]
    date_series = df_asset[DATE_COL]

    df_results = get_structured_risks_decomposition_df(
        asset_series,
        yf_start=end_date,
        yf_end=start_date,
        time_choice=time_choice,
        normalize=normalize,
        include_const=True,
        include_date=False,
        fill_missing_dates=False,
        fill_missing_method="ffill"

    )

    if normalize:
        for col in df_results.columns:
            df_results[col] = df_results[col] * asset_series_raw

    df_results["Date"] = df_asset["Date"]

    fig_area = get_plot(df_results)
    fig_area.update_yaxes(range=[0, asset_series_raw.max() + (0.05 * np.mean(asset_series_raw))])
    html_area = fig_area.to_html()

    fig_line = px.line(df_asset_raw, x=DATE_COL, y=ticker)
    fig_line.update_yaxes(range=[0, asset_series_raw.max() + (0.05 * np.mean(asset_series_raw))])
    html_line = fig_line.to_html()

    #
    # html = fig.to_html()
    #
    # fig_area = df_results.area_plot()
    # html_area = pio.to_html(fig_area)
    #
    # fig_line = px.line(asset_series)
    # fig_line.update_layout(
    #     legend=dict(
    #         orientation="h",
    #         yanchor="top",
    #         y=-0.2,
    #         xanchor="center",
    #         x=0.5
    #     )
    # )
    # html_line = pio.to_html(fig_line)

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
        start_date = values["start_date"].strip() if "start_date" in values else DEFAULT_YF_START_DATE
        if start_date:
            ymd = [int(p.strip()) for p in start_date.split("-")]  # MM/DD/YYYY
            dtime = dt.datetime(year=ymd[0], month=ymd[1], day=ymd[2])
            start_date = get_yf_date(dtime)
    except Exception as e:
        start_date = None

    try:
        end_date = values["end_date"].strip() if "end_date" in values else DEFAULT_YF_END_DATE
        if end_date:
            ymd = [int(p.strip()) for p in end_date.split("-")]  # MM/DD/YYYY
            dtime = dt.datetime(year=ymd[0], month=ymd[1], day=ymd[2])
            end_date = get_yf_date(dtime)
    except Exception as e:
        end_date = None

    if start_date is not None and end_date is not None:
        start_date = start_date if start_date < end_date else end_date
        end_date = end_date if start_date < end_date else start_date

    try:
        l1_wt = float(values["l1_wt"].strip()) if "l1_wt" in values else None
    except:
        l1_wt = None

    try:
        alpha = float(values["alpha"].strip()) if "alpha" in values else None
    except:
        alpha = None

    return ticker, start_date, end_date, time_choice, normalize, l1_wt, alpha


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
