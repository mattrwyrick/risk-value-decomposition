import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.tools as sm_tools

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge, Lasso
from sklearn.pipeline import make_pipeline

from rfd.risk_indicators import RISK_TYPES, RISK_INDICATOR_MAPPINGS


def get_linear_decompositions(series):
    """
    Return a linear decomposition of the time series data
    :param series:
    :return:
    """


