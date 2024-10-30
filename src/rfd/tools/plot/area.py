import pandas as pd
import plotly.express as px

from rfd.settings import DATE_COL, DEFAULT_RISK_TYPE
from rfd.tools.plot import get_ordered_y_columns

from rfd.risks import RAW_RISK_COLOR_MAPPING, STRUCTURED_RISK_COLOR_MAPPING


def get_plot(df, risk_type=DEFAULT_RISK_TYPE, show=False):
    """
    Return the plot
    :param df:
    :param risk_type:
    :param show:
    :return:
    """
    df[DATE_COL] = pd.to_datetime(df[DATE_COL])

    if risk_type == "structure":
        color_mapping = STRUCTURED_RISK_COLOR_MAPPING
    else:
        color_mapping = RAW_RISK_COLOR_MAPPING

    columns = get_ordered_y_columns(df)

    fig = px.area(df, x=DATE_COL, y=[columns], color_discrete_map=color_mapping)

    if show:
        fig.show()

    return fig


