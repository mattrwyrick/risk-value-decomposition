
import numpy as np
import pandas as pd
import yfinance as yf

from rfd.settings import get_yf_date, DEFAULT_YF_START_DATE, DEFAULT_YF_END_DATE, TIMES_CHOICE, DATE_COL

from rfd.tools import get_asset_data

from rfd.risk_indicators import RISK_TYPES, get_risk_inputs_df

from rfd.decomposition.results import Results

from rfd.decomposition.ridge_lasso import (
    get_linear_decomposition,
    get_linear_proportion_df,

    get_nonlinear_decomposition,
    get_nonlinear_proportion_df
)


TICKER = "JPM"


def main(ticker=TICKER):
    """
    Run a decomposition
    :return:
    """
    time_choice = TIMES_CHOICE  # Open, Close, Mean
    normalize = True

    add_constant = True
    L1_wt = 0.75
    alpha = 0.05

    df_asset = get_asset_data(
        ticker=ticker,
        yf_start=DEFAULT_YF_START_DATE,
        yf_end=DEFAULT_YF_END_DATE
    )

    target_series = df_asset[ticker]
    date_series = df_asset[DATE_COL]

    df_risk_inputs = get_risk_inputs_df(
        risk_types=RISK_TYPES,
        yf_start=DEFAULT_YF_START_DATE,
        yf_end=DEFAULT_YF_END_DATE,
        time_choice=time_choice,
        normalize=normalize,
        include_date=False
    )

    model = get_linear_decomposition(
        target_series=target_series,
        df_inputs=df_risk_inputs,
        add_constant=add_constant,
        alpha=alpha,
        L1_wt=L1_wt,
    )

    param_values = list(model.params)
    param_names = model.model.exog_names
    if param_names[0] == "const":
        param_names[0] = "Idiosyncratic"
        df_risk_inputs["Idiosyncratic"] = np.mean(target_series) * param_values[0]

    df_risk_inputs, ordered_columns = get_linear_proportion_df(
        df_results=df_risk_inputs,
        param_names=param_names,
        param_values=param_values
    )

    results = Results(
        dates=date_series,
        target_series=target_series,
        df_inputs=df_risk_inputs,
        ordered_columns=ordered_columns
    )

    fig = results.area_plot(save_tmp=True)

    import plotly.express as px
    import plotly.io as pio
    import time

    time.sleep(2)
    fig2 = px.line(target_series)
    fig2.update_yaxes(range=[0, target_series.max()])
    pio.write_html(fig2, file='tmp_chart.html', auto_open=True)

    a = 1


if __name__ == "__main__":
    main()


