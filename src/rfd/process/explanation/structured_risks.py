import numpy as np

from rfd.risks.components import (
    BOND_MARKET_NAME,
    EQUITY_MARKET_NAME,
    INFLATION_NAME,
    INTEREST_RATE_NAME,
    MARKET_LIQUIDITY_NAME,
    MARKET_VOLATILITY_NAME
)


def report(ticker, start_date, end_date, proportion_dict, directional_dict):
    """
    Generates a financial explanation report for a given asset based on risk factors.

    :param proportion_dict: Dictionary of factor contributions
    :param directional_dict: Dictionary indicating the direction of each factor's influence
    :param start_date: Start date for the period of analysis
    :param end_date: End date for the period of analysis
    :return: Formatted report explaining asset movements based on risk factors
    """
    proportion_dict = {proportion_dict[key]: key for key in proportion_dict}
    directional_dict = {directional_dict[key]: key for key in directional_dict}

    columns = [key for key in proportion_dict]
    date_text = f"<b><i>{ticker}</i></b><br>{start_date} to {end_date}"
    input_texts = list()

    for col in columns:
        POS = "rise"
        NEG = "fall"
        direction = POS if directional_dict[col] > 0 else NEG
        text = None

        # **Bond Market Risk**
        if col == BOND_MARKET_NAME:
            if direction == POS:
                text = f"<b>{col}</b>: As the value of corporate bonds and high yield bonds rises, expect {ticker} to rise as well, reflecting the positive correlation between the asset and the bond market."
            else:
                text = f"<b>{col}</b>: As the value of corporate bonds and high yield bonds rises, expect {ticker} to fall, as tighter liquidity conditions or rising bond yields may put downward pressure on the stock."

        # **Equity Market Exposure**
        if col == EQUITY_MARKET_NAME:
            if direction == POS:
                text = f"<b>{col}</b>: As the value of the S&P 500 rises, expect {ticker} to rise as well, reflecting a positive correlation between the stock and broader market performance."
            else:
                text = f"<b>{col}</b>: As the value of the S&P 500 rises, expect {ticker} to fall, possibly due to company-specific risks or macroeconomic pressures that decouple it from the broader equity market."

        # **Inflation Risk**
        if col == INFLATION_NAME:
            if direction == POS:
                text = f"<b>{col}</b>: As inflation expectations rise (through inflation-protected securities), expect {ticker} to rise, as companies often pass on higher costs to consumers, benefiting from inflationary environments."
            else:
                text = f"<b>{col}</b>: As inflation expectations rise (through inflation-protected securities), expect {ticker} to fall, reflecting pressure on margins and potential declines in consumer spending as costs increase."

        # **Interest Rate Risk**
        if col == INTEREST_RATE_NAME:
            if direction == POS:
                text = f"<b>{col}</b>: This asset is tied to Treasury yields across various maturities (13-week, 5-year, 10-year, and 30-year). As interest rates rise, expect {ticker} to fall, as higher rates reduce the present value of future earnings and increase borrowing costs."
            else:
                text = f"<b>{col}</b>: This asset is inversely tied to Treasury yields across various maturities. As interest rates fall, expect {ticker} to rise, as lower rates generally increase stock valuations and reduce financing costs."

        # **Market Liquidity Risk**
        if col == MARKET_LIQUIDITY_NAME:
            if direction == POS:
                text = f"<b>{col}</b>: As the value of investment-grade bonds rises, expect {ticker} to rise as well, reflecting improved liquidity conditions that generally benefit corporate assets."
            else:
                text = f"<b>{col}</b>: As the value of investment-grade bonds rises, expect {ticker} to fall, indicating that tighter liquidity in the bond market may signal reduced access to capital for companies."

        # **Market Volatility Risk**
        if col == MARKET_VOLATILITY_NAME:
            if direction == POS:
                text = f"<b>{col}</b>: As market uncertainty and perceived risk (CBOE $VIX) rise, expect {ticker} to rise as well, reflecting a positive correlation with increased market volatility."
            else:
                text = f"<b>{col}</b>: As market uncertainty and perceived risk (CBOE $VIX) rise, expect {ticker} to fall, as higher volatility typically leads to a negative response from the asset."

        if text:
            input_texts.append(text)

    col_text = "\n".join(input_texts)
    explanation = f"{date_text}\n\n{col_text}"
    return explanation
