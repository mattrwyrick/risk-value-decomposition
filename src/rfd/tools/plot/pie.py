import plotly.graph_objects as go

from rfd.risks import RAW_RISK_COLOR_MAPPING, STRUCTURED_RISK_COLOR_MAPPING
from rfd.risks.raw.baseline import COLOR as BASELINE_COLOR, NAME as BASELINE_NAME
from rfd.settings import IDIOSYNCRATIC_RISK_NAME, IDIOSYNCRATIC_RISK_COLOR


def get_plot(ticker, start_date, end_date, proportion_dict, directional_dict):
    """
    Generates a performance attribution report with a pie chart for a given asset.

    :param ticker: str - Asset ticker symbol
    :param start_date: str - Start date of analysis period
    :param end_date: str - End date of analysis period
    :param proportion_dict: dict - Factor contribution proportions (e.g. {'Inflation Risk': 0.345})
    :param directional_dict: dict - Directional impact (e.g. {'Inflation Risk': -1})
    :return: str - A formatted financial-style report
    """
    proportion_dict = {proportion_dict[key]: key for key in proportion_dict}
    directional_dict = {directional_dict[key]: key for key in directional_dict}

    factor_labels = []
    factor_values = []
    colors = []

    # Gradient color settings
    positive_colors = []  # Store shades of green
    negative_colors = []  # Store shades of red
    step = 255 / (len(proportion_dict) - 2)  # Gradient step calculation
    count = 0.0
    switch = False

    # Generate factor labels, values, and colors
    for factor, proportion in proportion_dict.items():
        contribution = round(proportion * 100.0, 1)
        direction = "+" if directional_dict[factor] > 0 else "-"

        if factor not in [IDIOSYNCRATIC_RISK_NAME, BASELINE_NAME]:
            factor_labels.append(f"{factor}")
            factor_values.append(contribution)
        else:
            factor_labels.append(factor)
            factor_values.append(contribution)

        # Assign custom colors to Baseline and Idiosyncratic factors
        if factor == BASELINE_NAME:
            color = BASELINE_COLOR
        elif factor == IDIOSYNCRATIC_RISK_NAME:
            color = IDIOSYNCRATIC_RISK_COLOR
        elif directional_dict[factor] > 0:
            green_value = int(255 - count)
            color = f"rgb(0,{green_value},0)"  # Gradient green shades for positive factors
            positive_colors.append(color)
            count += step
        else:
            if not switch:
                count = 0.0  # Reset count when switching to negative
                switch = True
            red_value = int(255 - count)
            color = f"rgb({red_value},0,0)"  # Gradient red shades for negative factors
            negative_colors.append(color)
            count += step

        colors.append(color)

    # Generate Pie Chart
    fig = go.Figure(data=[go.Pie(
        labels=factor_labels,
        values=factor_values,
        textinfo='label+percent',
        insidetextorientation='radial',
        marker=dict(colors=colors)  # Apply the gradient color scheme
    )])

    fig.update_layout(
        title=f"Factor Contribution for {ticker}",
        font=dict(size=14),
        showlegend=True,
        legend=dict(
            orientation="h",  # Horizontal layout
            x=0.5,  # Center legend horizontally
            y=-0.2,  # Position legend below the chart
            xanchor="center",
            yanchor="top"
        ),
        margin=dict(l=20, r=20, t=50, b=80)
    )

    # Convert plot to HTML for embedding
    # pie_chart_html = fig.to_html(full_html=False)

    return fig
