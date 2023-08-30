import math
from typing import Any, Callable, Dict, Optional, Union

import pandas as pd

from pyfrag_plotter.config_handler import config
from pyfrag_plotter.errors import PyFragResultsProcessingError


# ====================================================================================================
# Data Trimming   ====================================================================================
# ====================================================================================================

def _trim_data_str(df: pd.DataFrame, trim_option: str, energy_key: str) -> pd.DataFrame:
    """Private function that performs the actual trimming of the dataframe with a string trim_option"""
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
    """Private function that performs the actual trimming of the dataframe with a float trim_option"""
    index = (df[energy_key] - trim_option).abs().idxmin()
    df = df.loc[:index]
    return df


def _trim_data_int(df: pd.DataFrame, trim_option: int, energy_key: str) -> pd.DataFrame:
    """Private function that performs the actual trimming of the dataframe with a integer trim_option"""
    df = df.iloc[:trim_option]
    return df


_overload_types: Dict[Any, Callable[..., pd.DataFrame]] = {
    str: _trim_data_str,
    float: _trim_data_float,
    int: _trim_data_int,
}


def trim_data(df: pd.DataFrame, trim_parameter: Optional[Union[str, float, int]] = None, trim_key: Optional[str] = None) -> pd.DataFrame:
    """'Overloaded' function to trim the dataframe based on the type of the trim_parameter.

    This function trims the given dataframe based on the type of the trim_parameter.
    The trim_parameter is read from the configuration file and can be either a string ("min", "max"), integer (IRC point), or float (energy value).
    The function returns the trimmed dataframe.

    Args:
        df (pd.DataFrame): The dataframe to trim.
        trim_parameter (Optional[Union[str, float, int]]): The parameter to use for trimming. Defaults to None.
        trim_key (Optional[str]): The key to use for reading the trim_parameter from the configuration file. Defaults to None.

    Raises:
        PyFragResultsProcessingError: If the trim_parameter is not a valid type.

    Returns:
        pd.DataFrame: The trimmed dataframe.

    """
    trim_key = config["config"].get("SHARED", "trim_key") if trim_key is None else trim_key
    trim_parameter = config["config"].get("SHARED", "plot_until") if trim_parameter is None else trim_parameter

    if trim_parameter in ["false", "0", "no"]:
        return df

    if not isinstance(trim_parameter, (str, float, int)):
        raise PyFragResultsProcessingError(section="trim_data", message=f"trim_parameter {trim_parameter} is not a valid type. Valid types are str, float, and int")

    for key, value in _overload_types.items():
        if isinstance(trim_parameter, key):
            return value(df, trim_parameter, trim_key)

    return df


# ====================================================================================================
# Dispersion term check ==============================================================================
# ====================================================================================================

def remove_dispersion_term(df: pd.DataFrame) -> pd.DataFrame:
    """Removes the dispersion term from the dataframe if it is 0.0 everywhere.

    This function takes a pandas DataFrame containing the results file data and removes the dispersion term if it is 0.0 everywhere. The function returns the modified DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the results file data.

    Returns:
        pd.DataFrame: The modified DataFrame without the dispersion term if it is 0.0 everywhere.

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
