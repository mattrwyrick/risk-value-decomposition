import numpy as np


def report(ticker, start_date, end_date, proportion_dict, directional_dict):
    """

    :param proportion_dict:
    :param directional_dict:
    :param start_date:
    :param end_date:
    :return:
    """
    proportion_dict = {proportion_dict[key]: key for key in proportion_dict}
    directional_dict = {directional_dict[key]: key for key in directional_dict}

    columns = [key for key in proportion_dict]
    date_text = f"{ticker} from {start_date} to {end_date}"
    input_texts = list()
    for col in columns:
        direction = "positively" if directional_dict[col] > 0 else "negatively"
        text = f"<b>{col}</b>: Contributed {direction} by {round(proportion_dict[col] * 100.0, 1)}%"
        input_texts.append(text)
    col_text = "\n".join(input_texts)
    explanation = f"{date_text}\n\n{col_text}"
    return explanation



