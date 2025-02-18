from turtledemo.penrose import start

import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf

import plotly.io as pio
import plotly.express as px

from scipy.stats import norm

from datetime import datetime, timedelta
from flask import render_template

from rfd.settings import get_yf_date


TEMPLATE = "./calls.html"
FILL_MISSING_DATES = True
FILL_MISSING_METHOD = "ffill"  # forward fill

DEFAULT_TICKER = ""
DEFAULT_TIME_CHOICE = "Close"

DEFAULT_TIME_TO_EXPIRATION = 90
DEFAULT_STRIKE_PRICE = None
DEFAULT_RISK_FREE_RATE = 0.043
YEAR_DAYS = 252

DEFAULT_START_DATE_STR = "2024-01-01"
DEFAULT_START_DATE = datetime.strptime(DEFAULT_START_DATE_STR, "%Y-%m-%d")


def view(request, cache={}):
    """
    Create the home page
    :param request:
    :param cache: dict
    :return:
    """
    ticker, strike_price, time_to_expiration, start_date_str, risk_free_rate = get_values_from_request(request)
    cache = add_to_cache(cache, ticker, strike_price, time_to_expiration, start_date_str, risk_free_rate)

    if not (ticker and strike_price and time_to_expiration and start_date_str and risk_free_rate):
        return render_template(TEMPLATE, **cache)

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    buffer_start = start_date - timedelta(days=time_to_expiration)
    end_date = start_date + timedelta(days=time_to_expiration)
    buffer_end = end_date + timedelta(days=time_to_expiration)

    stock_data = yf.download(ticker, start=buffer_start, end=buffer_end)
    date_range = pd.date_range(start=buffer_start, end=buffer_end, freq='D')
    df = stock_data.reindex(date_range, method='ffill')
    df = df['Close']
    df["Date"] = df.index

    df["Returns"] = df[ticker] / df[ticker].shift(1)
    df["Log Returns"] = np.log(df["Returns"])

    df["Volatility"] = np.nan
    df["Strike"] = np.nan
    df["Option Price"] = np.nan

    df["Delta"] = np.nan
    df["Gamma"] = np.nan
    df["Vega"] = np.nan
    df["Theta"] = np.nan

    for i, row in df.loc[start_date: end_date].iterrows():
        current_date = row["Date"]

        volatility = calculate_volatility(df["Log Returns"], current_date, window=time_to_expiration)

        remaining_days = (end_date - current_date).days  # Calculate remaining days to expiration
        T = remaining_days / YEAR_DAYS  # Convert to fraction of year
        spot_price = row[ticker]

        call_price, d1, d2 = calculate_black_scholes(spot_price, strike_price, T, risk_free_rate, volatility)
        theta = calculate_theta(spot_price, strike_price, T, risk_free_rate, volatility, d1, d2)
        delta = calculate_delta(d1)
        gamma = calculate_gamma(spot_price, volatility, T, d1)
        vega = calculate_vega(spot_price, T, d1, volatility)

        df.loc[current_date, "Strike"] = strike_price
        df.loc[current_date, "Option Price"] = call_price
        df.loc[current_date, "Volatility"] = volatility
        df.loc[current_date, "Delta"] = delta
        df.loc[current_date, "Gamma"] = gamma
        df.loc[current_date, "Vega"] = vega
        df.loc[current_date, "Theta"] = theta

    df[f"{ticker} Scaled"] = (df[ticker] / df[ticker].mean()) * df["Option Price"].mean()
    df[f"Strike Scaled"] = (df["Strike"] / df[ticker].mean()) * df["Option Price"].mean()

    df = df.loc[start_date:end_date]
    columns = ["Option Price", "Delta", "Gamma", "Vega", "Theta", f"{ticker} Scaled", "Strike Scaled"]
    fig_greek = px.line(df, x="Date", y=columns)
    fig_greek.update_layout(title=f"{ticker} {time_to_expiration} day Call")
    greek_html = fig_greek.to_html()
    cache["area_chart"] = greek_html

    columns = [ticker, "Strike"]
    fig_stock = px.line(df, x="Date", y=columns)
    fig_stock.update_layout(title=f"{ticker} {time_to_expiration} day Call")
    stock_html = fig_stock.to_html()
    cache["pie_chart"] = stock_html

    fig_vol = px.line(df, x="Date", y="Volatility")
    fig_vol.update_layout(title=f"{ticker} {time_to_expiration} day Call")
    fig_html = fig_vol.to_html()
    cache["line_chart"] = fig_html

    return render_template(TEMPLATE, **cache)


def calculate_black_scholes(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + (sigma ** 2) / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price, d1, d2


def calculate_theta(S, K, T, r, sigma, d1, d2):
    theta = -S * sigma * norm.pdf(d1) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    return theta


def calculate_delta(d1):
    return norm.cdf(d1)


def calculate_gamma(S, sigma, T, d1):
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))


def calculate_vega(S, T, d1, sigma):
    return S * np.sqrt(T) * norm.pdf(d1)


def calculate_volatility(stock_returns, current_date, window=90):
    start_idx = current_date - pd.Timedelta(days=window)
    historical_returns = stock_returns.loc[start_idx:current_date]
    volatility = historical_returns.std() * np.sqrt(YEAR_DAYS)  # Annualizing the volatility
    return volatility


def get_values_from_request(request):
    """
    Get the values from the request
    :param request:
    :return:
    """
    values = request.values

    ticker = values["ticker"].strip() if "ticker" in values else DEFAULT_TICKER

    try:
        start_date = values["start_date"].strip() if "start_date" in values else DEFAULT_START_DATE_STR
        if start_date:
            ymd = [int(p.strip()) for p in start_date.split("-")]
            dtime = dt.datetime(year=ymd[0], month=ymd[1], day=ymd[2])
            start_date = get_yf_date(dtime)
    except Exception as e:
        start_date = None

    try:
        strike_price = float(values["strike_price"]) if "strike_price" in values else DEFAULT_STRIKE_PRICE
    except Exception as e:
        strike_price = DEFAULT_STRIKE_PRICE

    try:
        time_to_expiration = int(values["time_to_exp"]) if "time_to_exp" in values else DEFAULT_TIME_TO_EXPIRATION
    except Exception as e:
        time_to_expiration = DEFAULT_TIME_TO_EXPIRATION

    try:
        risk_free_rate = float(values["risk_free_rate"]) if "risk_free_rate" in values else DEFAULT_RISK_FREE_RATE
    except Exception as e:
        risk_free_rate = DEFAULT_RISK_FREE_RATE

    return ticker, strike_price, time_to_expiration, start_date, risk_free_rate


def add_to_cache(cache, ticker=None, strike_price=None, time_to_expiration=None, start_date=None, risk_free_rate=None):
    """
    Add values to the cache
    :param cache:
    :param ticker:
    :param strike_price:
    :param time_to_expiration:
    :param start_date:
    :param risk_free_rate:
    :return:
    """
    if ticker:
        cache["ticker"] = ticker
    if strike_price:
        cache["strike_price"] = strike_price
    if time_to_expiration:
        cache["time_to_exp"] = time_to_expiration
    if start_date:
        cache["start_date"] = start_date
    if risk_free_rate:
        cache["risk_free_rate"] = risk_free_rate
    return cache
