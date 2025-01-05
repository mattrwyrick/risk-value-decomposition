import os

from pathlib import Path
import datetime as dt

SRC_DIR = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()
APP_DIR = os.path.join(SRC_DIR, "bck")

SEED = 25193804


TIMES_MAPPING = {
    "Close": lambda x: x["Close"],
    "Open": lambda x: x["Open"],
    "Mean": lambda x: (x["Close"] + x["Open"]) / 2.0
}

TIMES_CHOICE = "Mean"

DATE_COL = "Date"

IDIOSYNCRATIC_RISK_NAME = "Idiosyncratic"


def get_yf_date(dtime):
    """
    Return the date format for yfinance
    :param dtime:
    :return:
    """
    year = dtime.year
    month = f"0{dtime.month}" if dtime.month < 10 else dtime.month
    day = f"0{dtime.day}" if dtime.day < 10 else dtime.day
    return f"{year}-{month}-{day}"


DEFAULT_RISK_TYPE = "structured"

DEFAULT_YEARS_BACK = 3

DEFAULT_DT_END_DATE = dt.datetime.today()
DEFAULT_YF_END_DATE = get_yf_date(DEFAULT_DT_END_DATE)

DEFAULT_DT_START_DATE = DEFAULT_DT_END_DATE - dt.timedelta(365 * DEFAULT_YEARS_BACK)  # 3 years
DEFAULT_YF_START_DATE = get_yf_date(DEFAULT_DT_START_DATE)


