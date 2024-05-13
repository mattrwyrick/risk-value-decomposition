
from rfd.risk_indicators.bond_market import NAME as BOND_MARKET_NAME, get_risk as get_bond_market_risk
from rfd.risk_indicators.bond_market_high_yield import NAME as BOND_MARKET_HY_NAME, get_risk as get_bond_market_risk_high_yield

from rfd.risk_indicators.equity_market import NAME as EQUITY_MARKET_NAME, get_risk as get_equity_market_risk
from rfd.risk_indicators.market_liquidity import NAME as MARKET_LIQUIDITY_NAME, get_risk as get_market_liquidity_risk
from rfd.risk_indicators.market_volatility import NAME as MARKET_VOLATILITY_NAME, get_risk as get_market_volatility_risk

from rfd.risk_indicators.inflation import NAME as INFLATION_NAME, get_risk as get_inflation_risk
from rfd.risk_indicators.interest_rate_long_term import NAME as INTEREST_RATE_LT_NAME, get_risk as get_interest_rate_long_term_risk
from rfd.risk_indicators.interest_rate_medium_term import NAME as INTEREST_RATE_MT_NAME, get_risk as get_interest_rate_medium_term_risk
from rfd.risk_indicators.interest_rate_short_term import NAME as INTEREST_RATE_ST_NAME, get_risk as get_interest_rate_short_term_risk

RISK_TYPES = [
    BOND_MARKET_NAME,
    BOND_MARKET_HY_NAME,
    EQUITY_MARKET_NAME,
    MARKET_LIQUIDITY_NAME,
    MARKET_VOLATILITY_NAME,
    INFLATION_NAME,
    INTEREST_RATE_LT_NAME,
    INTEREST_RATE_MT_NAME,
    INTEREST_RATE_ST_NAME
]


RISK_INDICATOR_MAPPINGS = {

    BOND_MARKET_NAME: get_bond_market_risk,
    BOND_MARKET_HY_NAME: get_bond_market_risk_high_yield,

    EQUITY_MARKET_NAME: get_equity_market_risk,
    MARKET_LIQUIDITY_NAME: get_market_liquidity_risk,
    MARKET_VOLATILITY_NAME: get_market_volatility_risk,

    INFLATION_NAME: get_inflation_risk,
    INTEREST_RATE_LT_NAME: get_interest_rate_long_term_risk,
    INTEREST_RATE_MT_NAME: get_interest_rate_medium_term_risk,
    INTEREST_RATE_ST_NAME: get_interest_rate_short_term_risk

}


