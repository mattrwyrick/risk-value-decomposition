
import pandas as pd
import plotly.express as px

from rfd.settings import DATE_COL, DEFAULT_RISK_TYPE
from rfd.tools.plot import get_ordered_y_columns

from rfd.risks import RAW_RISK_COLOR_MAPPING, STRUCTURED_RISK_COLOR_MAPPING
from rfd.risks.raw.baseline import COLOR as BASELINE_COLOR, NAME as BASELINE_NAME
from rfd.settings import IDIOSYNCRATIC_RISK_NAME, IDIOSYNCRATIC_RISK_COLOR


def get_plot(df, risk_type=DEFAULT_RISK_TYPE, show=False):
    """
    Return the plot
    :param df:
    :param risk_type:
    :param show:
    :return:
    """
    df[DATE_COL] = pd.to_datetime(df[DATE_COL])

    if risk_type == "raw":
        color_mapping = RAW_RISK_COLOR_MAPPING
    else:
        color_mapping = STRUCTURED_RISK_COLOR_MAPPING

    columns = get_ordered_y_columns(df)

    fig = px.area(df, x=DATE_COL, y=[str(c) for c in columns], color_discrete_map=color_mapping)

    if show:
        fig.show()

    return fig


def get_directional_plot(df, show=False):
    """
    Return the plot
    :param df:
    :param risk_type:
    :param show:
    :return:
    """
    df[DATE_COL] = pd.to_datetime(df[DATE_COL])

    columns = get_ordered_y_columns(df)

    color_mapping = {}
    count = 0.0
    switch = False
    step = 255 / (len(columns) - 2)
    for col in columns:
        value = df[col].iloc[0]
        if col == IDIOSYNCRATIC_RISK_NAME:
            color_mapping[IDIOSYNCRATIC_RISK_NAME] = IDIOSYNCRATIC_RISK_COLOR
        elif col == BASELINE_NAME:
            color_mapping[BASELINE_NAME] = BASELINE_COLOR
        elif value >= 0:
            green_value = int(255 - count)
            color = f"rgb(0,{green_value},0)"
            color_mapping[col] = color
            count += step
        else:
            if not switch:
                count = 0.0
                switch = True
            red_value = int(255 - count)
            color = f"rgb({red_value},0,0)"
            color_mapping[col] = color
            count += step

    df_abs = df.drop(columns=['Date']).abs()
    df_abs[DATE_COL] = df[DATE_COL]
    fig = px.area(df_abs, x=DATE_COL, y=[str(c) for c in columns], color_discrete_map=color_mapping)

    if show:
        fig.show()

    return fig


