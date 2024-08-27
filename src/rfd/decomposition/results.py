import numpy as np
import plotly.express as px
import plotly.io as pio

from rfd.settings import DATE_COL
from rfd.risk_indicators import RISK_COLOR_MAPPING, RISK_TYPES


class Results(object):

    def __init__(self, df, ordered_columns=False):
        """
        A class to store results to standardize plotting
        :param df:
        :param ordered_columns:
        """
        self.df = df
        if DATE_COL not in df.columns:
            self.df[DATE_COL] = df.index

        if not ordered_columns:
            self.ordered_columns = [col for col in df.columns if col.lower() not in ("date", DATE_COL.lower())]
        else:
            self.ordered_columns = ordered_columns

        self.color_mapping = dict()
        self._set_color_mapping()

    def area_plot(self, show=False, save_tmp=False, adj_legend=True):
        """
        Plot the data
        :return:
        """
        fig = px.area(self.df, x=DATE_COL, y=self.ordered_columns, color_discrete_map=self.color_mapping)
        if adj_legend:
            fig.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
        if show:
            fig.show()
        if save_tmp:
            pio.write_html(fig, file='tmp_chart.html', auto_open=True)
        return fig

    def line_plot(self, show=True):
        """
        Plot the data
        :return:
        """
        fig = px.area(self.df, x=DATE_COL, y=self.ordered_columns, color_discrete_map=self.color_mapping)
        if show:
            fig.show()
        return fig

    def pie_plot(self, show=True):
        """
        Plot a pie chart
        :param show:
        :return:
        """
        pass

    def _set_color_mapping(self):
        """
        Create the color mapping
        :return:
        """
        risks_with_colors = list(set(self.ordered_columns).intersection(set(RISK_TYPES)))
        risks_without_colors = [risk for risk in self.ordered_columns if risk not in risks_with_colors]

        for risk in risks_with_colors:
            self.color_mapping[risk] = RISK_COLOR_MAPPING[risk]

        grayscale_values = np.linspace(0, 255, len(risks_without_colors), dtype=int)
        for i, risk in enumerate(risks_without_colors):
            rgb = grayscale_values[i]
            self.color_mapping[risk] = f"rgb({rgb},{rgb},{rgb})"

        return self.color_mapping