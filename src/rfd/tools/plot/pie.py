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
    factor_sort = []
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
            factor_sort.append(["IDIO", direction, contribution, factor])
        else:
            factor_labels.append(factor)
            factor_values.append(contribution)
            factor_sort.append(["", direction, contribution, factor])


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
        factor_sort[-1].append(color)


    factor_sort.sort()

    factor_labels = [x[3] for x in factor_sort]
    factor_values = [x[2] for x in factor_sort]
    colors = [x[4] for x in factor_sort]

    # Generate Pie Chart
    fig = go.Figure(data=[go.Pie(
        labels=factor_labels,
        values=factor_values,
        textinfo='label+percent',
        insidetextorientation='radial',
        marker=dict(colors=colors),
        sort=False
    )])

    fig.update_layout(
        title=f"Factors ({ticker})",
        font=dict(size=14),
        showlegend=True,
        legend=dict(
            orientation="v",  # Vertical layout
            x=1.50,  # Position legend far right
            y=0.03,  # Position the legend closer to the bottom
            xanchor="left",  # Anchor to the left of the legend box
            yanchor="bottom",  # Anchor to the bottom of the legend box
            font=dict(size=10),  # Shrink the legend font size
            traceorder="normal",  # Keep the order of items in the legend as they are
        ),
        margin=dict(l=20, r=150, t=50, b=80)  # Adjust right margin to accommodate legend
    )

    return fig
