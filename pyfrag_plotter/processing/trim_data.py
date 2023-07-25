from typing import Any, Callable, Union
import pandas as pd
from pyfrag_plotter.pyfrag_errors import PyFragResultsProcessingError


ENERGY_KEY = "EnergyTotal"


def _trim_data_str(df: pd.DataFrame, trim_option: str) -> pd.DataFrame:
    """Trims the dataframe up to either the minimum or maximum energy value (dEint)

    Args:
        df (pd.DataFrame): dataframe to trim
        trim_option (str, optional): Either "min" or "max"

    Raises:
        PyFragResultsProcessingError: if trim_option is not "min" or "max"

    Returns:
        pd.DataFrame: trimmed dataframe
    """

    trim_option = trim_option.lower()
    options = ["min", "max"]

    if trim_option not in options:
        raise PyFragResultsProcessingError(section="trim_data_str", message=f"trim_option {trim_option} is not valid. Valid options are {options}")

    if trim_option == "max":
        max_index = df[ENERGY_KEY].idxmax()
        df = df.loc[:max_index]
        return df

    min_index = df[ENERGY_KEY].idxmin()
    df = df.loc[:min_index]
    return df


def _trim_data_float(df: pd.DataFrame, trim_option: float) -> pd.DataFrame:
    """Trims the dataframe up to the nearest specified energy value (dEint)

    Args:
        df (pd.DataFrame): dataframe to trim
        trim_option (float): energy value (dEint) to trim up to

    Returns:
        pd.DataFrame: trimmed dataframe
    """
    index = (df[ENERGY_KEY] - trim_option).abs().idxmin()
    df = df.loc[:index]
    return df


def _trim_data_int(df: pd.DataFrame, trim_option: int) -> pd.DataFrame:
    """Trims the dataframe up to the specified number of rows

    Args:
        df (pd.DataFrame): dataframe to trim
        trim_option (int): index number of row to trim up to

    Returns:
        pd.DataFrame: trimmed dataframe
    """
    df = df.iloc[:trim_option]
    return df


overload_types: dict[Any, Callable[..., pd.DataFrame]] = {
    str: _trim_data_str,
    float: _trim_data_float,
    int: _trim_data_int,
}


def trim_data(df: pd.DataFrame, trim_parameter: Union[str, float, int]) -> pd.DataFrame:
    """'Overloaded' function to trim the dataframe based on the type of the trim_parameter

    Args:
        df (pd.DataFrame): dataframe to trim
        trim_parameter (Union[str, float, int]): parameter to trim the dataframe with (either a string, integer, or float)

    Returns:
        pd.DataFrame: trimmed dataframe
    """

    if not isinstance(trim_parameter, (str, float, int)):
        raise PyFragResultsProcessingError(section="trim_data", message=f"trim_parameter {trim_parameter} is not a valid type. Valid types are str, float, and int")

    for key, value in overload_types.items():
        if isinstance(trim_parameter, key):
            return value(df, trim_parameter)

    return df
