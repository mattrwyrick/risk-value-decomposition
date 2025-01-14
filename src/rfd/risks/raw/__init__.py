
import pandas as pd

from rfd.settings import DEFAULT_YF_START_DATE, DEFAULT_YF_END_DATE, TIMES_CHOICE

from rfd.risks.raw.baseline import COLOR as BASELINE_COLOR, NAME as BASELINE_NAME, get_risk as get_baseline_risk

from rfd.risks.raw.bond_market import COLOR as BOND_MARKET_COLOR, NAME as BOND_MARKET_NAME, get_risk as get_bond_market_risk
from rfd.risks.raw.bond_market_high_yield import COLOR as BOND_MARKET_HY_COLOR, NAME as BOND_MARKET_HY_NAME, get_risk as get_bond_market_hy_risk

from rfd.risks.raw.equity_market import COLOR as EQUITY_MARKET_COLOR, NAME as EQUITY_MARKET_NAME, get_risk as get_equity_market_risk
from rfd.risks.raw.market_liquidity import COLOR as MARKET_LIQUIDITY_COLOR, NAME as MARKET_LIQUIDITY_NAME, get_risk as get_market_liquidity_risk
from rfd.risks.raw.market_volatility import COLOR as MARKET_VOLATILITY_COLOR, NAME as MARKET_VOLATILITY_NAME, get_risk as get_market_volatility_risk

from rfd.risks.raw.inflation import COLOR as INFLATION_COLOR, NAME as INFLATION_NAME, get_risk as get_inflation_risk

from rfd.risks.raw.interest_rate_30y import COLOR as INTEREST_RATE_30Y_COLOR, NAME as INTEREST_RATE_30Y_NAME, get_risk as get_interest_rate_30y_risk
from rfd.risks.raw.interest_rate_10y import COLOR as INTEREST_RATE_10Y_COLOR, NAME as INTEREST_RATE_10Y_NAME, get_risk as get_interest_rate_10y_risk
from rfd.risks.raw.interest_rate_5y import COLOR as INTEREST_RATE_5Y_COLOR, NAME as INTEREST_RATE_5Y_NAME, get_risk as get_interest_rate_5y_risk
from rfd.risks.raw.interest_rate_13w import COLOR as INTEREST_RATE_13W_COLOR, NAME as INTEREST_RATE_13W_NAME, get_risk as get_interest_rate_13w_risk


RISK_TYPES = [
    BASELINE_NAME,
    BOND_MARKET_NAME,
    BOND_MARKET_HY_NAME,
    EQUITY_MARKET_NAME,
    MARKET_LIQUIDITY_NAME,
    MARKET_VOLATILITY_NAME,
    INFLATION_NAME,
    INTEREST_RATE_30Y_NAME,
    INTEREST_RATE_10Y_NAME,
    INTEREST_RATE_5Y_NAME,
    INTEREST_RATE_13W_NAME
]


RISK_INDICATOR_MAPPING = {
    BASELINE_NAME: get_baseline_risk,

    BOND_MARKET_NAME: get_bond_market_risk,
    BOND_MARKET_HY_NAME: get_bond_market_hy_risk,

    EQUITY_MARKET_NAME: get_equity_market_risk,
    MARKET_LIQUIDITY_NAME: get_market_liquidity_risk,
    MARKET_VOLATILITY_NAME: get_market_volatility_risk,

    INFLATION_NAME: get_inflation_risk,

    INTEREST_RATE_30Y_NAME: get_interest_rate_30y_risk,
    INTEREST_RATE_10Y_NAME: get_interest_rate_10y_risk,
    INTEREST_RATE_5Y_NAME: get_interest_rate_5y_risk,
    INTEREST_RATE_13W_NAME: get_interest_rate_13w_risk
}

RISK_COLOR_MAPPING = {
    BASELINE_NAME: BASELINE_COLOR,

    BOND_MARKET_NAME: BOND_MARKET_COLOR,
    BOND_MARKET_HY_NAME: BOND_MARKET_HY_COLOR,

    EQUITY_MARKET_NAME: EQUITY_MARKET_COLOR,
    MARKET_LIQUIDITY_NAME: MARKET_LIQUIDITY_COLOR,
    MARKET_VOLATILITY_NAME: MARKET_VOLATILITY_COLOR,

    INFLATION_NAME: INFLATION_COLOR,

    INTEREST_RATE_30Y_COLOR: INTEREST_RATE_30Y_COLOR,
    INTEREST_RATE_10Y_COLOR: INTEREST_RATE_10Y_COLOR,
    INTEREST_RATE_5Y_COLOR: INTEREST_RATE_5Y_NAME,
    INTEREST_RATE_13W_COLOR: INTEREST_RATE_13W_COLOR
}


def get_risk_inputs_df(
        risk_types=RISK_TYPES,
        yf_start=DEFAULT_YF_START_DATE,
        yf_end=DEFAULT_YF_END_DATE,
        time_choice=TIMES_CHOICE,
        normalize=True,
        include_const=True,
        include_date=False,
        fill_missing_dates=False,
        fill_missing_method="ffill"
):
    """
    Return a df of the risk types
    :param risk_types:
    :param yf_start:
    :param yf_end:
    :param time_choice:
    :param normalize:
    :param include_const:
    :param include_date:
    :param fill_missing_dates:
    :param fill_missing_method:
    :return:
    """
    df_risk_inputs = pd.DataFrame()
    for risk_type in risk_types:
        if risk_type in RISK_INDICATOR_MAPPING:
            if risk_type == BASELINE_NAME and not include_const:
                continue

            df_risk = RISK_INDICATOR_MAPPING[risk_type](
                yf_start=yf_start,
                yf_end=yf_end,
                time_choice=time_choice,
                normalize=normalize,
                include_date=include_date
            )
            for col in df_risk.columns:
                df_risk_inputs[col] = df_risk[col]

    if fill_missing_dates:
        date_range = pd.date_range(start=yf_start, end=yf_end)
        df_risk_inputs = df_risk_inputs.reindex(date_range)
        df_risk_inputs = df_risk_inputs.ffill()

    return df_risk_inputs


