import numpy as np
import pandas as pd
import yfinance as yf

from scipy.stats import norm

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt
from datetime import datetime, timedelta


TICKER = "JPM"
TIME_TO_EXPIRATION = 90
STRIKE_PRICE = 139.0  # Example strike
RISK_FREE_RATE = 0.03  # 3% annual risk-free rate (for example)
YEAR_DAYS = 252

START_DATE_STR = "2023-01-01"
START_DATE = datetime.strptime(START_DATE_STR, "%Y-%m-%d")
BUFFER_START = START_DATE - timedelta(days=TIME_TO_EXPIRATION)

END_DATE = START_DATE + timedelta(days=TIME_TO_EXPIRATION)
END_DATE_STR = END_DATE.strftime("%Y-%m-%d")
BUFFER_END = END_DATE + timedelta(days=TIME_TO_EXPIRATION)


def main():
    """
    Run the greek decomposition
    :return:
    """
    stock_data = yf.download(TICKER, start=BUFFER_START, end=BUFFER_END)
    date_range = pd.date_range(start=BUFFER_START, end=BUFFER_END, freq='D')
    df = stock_data.reindex(date_range, method='ffill')
    df = df['Close']
    df["Date"] = df.index


    df["Returns"] = df[TICKER] / df[TICKER].shift(1)
    df["Log Returns"] = np.log(df["Returns"])

    df["Volatility"] = np.nan
    df["Strike"] = np.nan
    df["Option Price"] = np.nan

    df["Delta"] = np.nan
    df["Gamma"] = np.nan
    df["Vega"] = np.nan
    df["Theta"] = np.nan

    for i, row in df.loc[START_DATE: END_DATE].iterrows():
        current_date = row["Date"]
        if current_date < START_DATE - timedelta(TIME_TO_EXPIRATION):
            continue

        volatility = calculate_volatility(df["Log Returns"], current_date, window=TIME_TO_EXPIRATION)

        remaining_days = (END_DATE - current_date).days  # Calculate remaining days to expiration
        T = remaining_days / YEAR_DAYS  # Convert to fraction of year
        spot_price = row[TICKER]

        call_price, d1, d2 = black_scholes(spot_price, STRIKE_PRICE, T, RISK_FREE_RATE, volatility)
        theta = calculate_theta(spot_price, STRIKE_PRICE, T, RISK_FREE_RATE, volatility, d1, d2)
        delta = calculate_delta(d1)
        gamma = calculate_gamma(spot_price, volatility, T, d1)
        vega = calculate_vega(spot_price, T, d1, volatility)

        df.loc[current_date, "Strike"] = STRIKE_PRICE
        df.loc[current_date, "Option Price"] = call_price
        df.loc[current_date, "Volatility"] = volatility
        df.loc[current_date, "Delta"] = delta
        df.loc[current_date, "Gamma"] = gamma
        df.loc[current_date, "Vega"] = vega
        df.loc[current_date, "Theta"] = theta

    df[f"{TICKER} Scaled"] = (df[TICKER] / df[TICKER].mean()) * df["Option Price"].mean()
    df[f"Strike Scaled"] = (df["Strike"] / df[TICKER].mean()) * df["Option Price"].mean()

    columns = [f"{TICKER} Scaled", "Strike Scaled", "Option Price", "Volatility", "Delta", "Gamma", "Vega", "Theta"]
    fig = px.line(df, x="Date", y=columns)
    fig.update_layout(title=f"{TICKER} {TIME_TO_EXPIRATION} day Call")
    fig.show()

    columns = [TICKER, "Strike"]
    fig = px.line(df, x="Date", y=columns)
    fig.update_layout(title=f"{TICKER} {TIME_TO_EXPIRATION} day Call")
    fig.show()

    pd.set_option('display.max_rows', None)  # No limit on rows
    pd.set_option('display.max_columns', None)  # No limit on columns
    pd.set_option('display.width', None)  # Prevent line wrapping
    pd.set_option('display.max_colwidth', None)  # No limit on column width
    print("#######")
    print(f"Risk Free Rate: {RISK_FREE_RATE}")
    print(f"Strike: {STRIKE_PRICE}")
    print(f"Duration (days): {TIME_TO_EXPIRATION}")
    print("\n")
    df.dropna(inplace=True)
    print(df)



def black_scholes(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + (sigma ** 2) / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price, d1, d2

# Theta calculation
def calculate_theta(S, K, T, r, sigma, d1, d2):
    theta = -S * sigma * norm.pdf(d1) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    return theta

# Delta calculation
def calculate_delta(d1):
    return norm.cdf(d1)

# Gamma calculation
def calculate_gamma(S, sigma, T, d1):
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))

# Vega calculation
def calculate_vega(S, T, d1, sigma):
    return S * np.sqrt(T) * norm.pdf(d1)

# Function to calculate historical volatility over a rolling window
def calculate_volatility(stock_returns, current_date, window=90):
    start_idx = current_date - pd.Timedelta(days=window)
    historical_returns = stock_returns.loc[start_idx:current_date]
    volatility = historical_returns.std() * np.sqrt(YEAR_DAYS)  # Annualizing the volatility
    return volatility


if __name__ == "__main__":
    main()
