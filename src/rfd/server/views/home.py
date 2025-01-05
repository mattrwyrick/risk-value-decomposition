import numpy as np
import pandas as pd
import datetime as dt
import plotly.io as pio
import plotly.express as px

from flask import render_template


from rfd.settings import get_yf_date, DEFAULT_YF_START_DATE, DEFAULT_YF_END_DATE, TIMES_CHOICE, DATE_COL

from rfd.tools import get_asset_data



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
    return render_template(TEMPLATE, **cache)
