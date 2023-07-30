import math
from typing import Any, Callable

import pandas as pd

from pyfrag_plotter.config_handler import config
from pyfrag_plotter.errors import PyFragResultsProcessingError


# ====================================================================================================
# Data Trimming   ====================================================================================
# ====================================================================================================

def _trim_data_str(df: pd.DataFrame, trim_option: str, energy_key: str) -> pd.DataFrame:
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
        max_index = df[energy_key].idxmax()
        df = df.loc[:max_index]
        return df

    min_index = df[energy_key].idxmin()
    df = df.loc[:min_index]
    return df


def _trim_data_float(df: pd.DataFrame, trim_option: float, energy_key: str) -> pd.DataFrame:
    """Trims the dataframe up to the nearest specified energy value (dEint)

    Args:
        df (pd.DataFrame): dataframe to trim
        trim_option (float): energy value (dEint) to trim up to

    Returns:
        pd.DataFrame: trimmed dataframe
    """
    index = (df[energy_key] - trim_option).abs().idxmin()
    df = df.loc[:index]
    return df


def _trim_data_int(df: pd.DataFrame, trim_option: int, energy_key: str) -> pd.DataFrame:
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


def trim_data(df: pd.DataFrame) -> pd.DataFrame:
    """'Overloaded' function to trim the dataframe based on the type of the trim_parameter

    Args:
        df (pd.DataFrame): dataframe to trim
        trim_parameter (Union[str, float, int]): parameter to trim the dataframe with (either a string, integer, or float)

    Returns:
        pd.DataFrame: trimmed dataframe
    """
    energy_key = config.get("SHARED", "trim_key")
    trim_parameter = config.get("SHARED", "plot_until")

    if trim_parameter in ["false", "0", "no"]:
        return df

    if not isinstance(trim_parameter, (str, float, int)):
        raise PyFragResultsProcessingError(section="trim_data", message=f"trim_parameter {trim_parameter} is not a valid type. Valid types are str, float, and int")

    for key, value in overload_types.items():
        if isinstance(trim_parameter, key):
            return value(df, trim_parameter, energy_key)

    return df


# ====================================================================================================
# Dispersion term check ==============================================================================
# ====================================================================================================

def remove_dispersion_term(df: pd.DataFrame) -> pd.DataFrame:
    """ Removes the dispersion term from the dataframe if it is 0.0 everywhere.

    Args:
        df (pd.DataFrame): dataframe containing the resultsfile data

    Returns:
        pd.DataFrame: dataframe without the dispersion term if it is 0.0 everywhere
    """
    if "Disp" not in df.columns:
        return df

    # Check if the dispersion term is 0.0 everywhere
    if all([math.isclose(value, 0.0) for value in df["Disp"]]):
        # Remove the dispersion term
        df = df.drop(columns=["Disp"])

    return df


# ====================================================================================================
# Removing Outliers ==================================================================================
# ====================================================================================================
