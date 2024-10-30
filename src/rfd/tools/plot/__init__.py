


from rfd.settings import DEFAULT_RISK_TYPE
from rfd.risks.calculated.idiosyncratic import NAME as IDIOSYNCRATIC_NAME
from rfd.risks.raw.baseline import NAME as BASELINE_NAME
from rfd.risks import RAW_RISK_TYPES, STRUCTURED_RISK_TYPES


def get_ordered_y_columns(df, risk_type=DEFAULT_RISK_TYPE):
    """
    Return an ordered y columns df before plotting
    :param df:
    :param risk_type:
    :return:
    """
    if risk_type == "structured":
        keep_cols = STRUCTURED_RISK_TYPES
    else:
        keep_cols = RAW_RISK_TYPES

    columns = [col for col in df.columns if col in keep_cols]

    if BASELINE_NAME in df.columns:
        columns = [BASELINE_NAME] + columns
    if IDIOSYNCRATIC_NAME in df.columns:
        columns = columns + [IDIOSYNCRATIC_NAME]

    return columns

