
from statsmodels.tsa.seasonal import STL


def get_seasonal_component(series, period_length=1):
    """
    Return the seasonal component
    :param period_length:
    :return:
    """
    stl = STL(series, period=period_length, trend=1, robust=True)  # trend=1 forces a constant trend
    result = stl.fit()
    seasonal_component = result.seasonal
    return seasonal_component
