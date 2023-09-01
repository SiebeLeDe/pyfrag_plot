import math
from typing import Any, Callable, Dict, Optional, Sequence, Union
import numpy as np
import pandas as pd

from pyfrag_plotter.config_handler import config
from pyfrag_plotter.errors import PyFragResultsProcessingError, PyFragResultsProcessingWarning

# ====================================================================================================
# Main Processing Function   =========================================================================
# ====================================================================================================


def process_results_file(
        df: pd.DataFrame,
        trim_option: Optional[Union[str, float, int, Sequence]] = None,
        trim_key: Optional[str] = None,
        *args,
) -> pd.DataFrame:
    """Processes the results file data.

    Args:
        df: A pandas DataFrame containing the results file data.
        trim_option: An optional argument specifying how to trim the data. Can be "max", "min", "x_limits", or None.
        trim_key: An optional argument specifying the key to use for trimming the data. Can be "EnergyTotal" or None.
        irc_coord: An optional argument specifying the IRC coordinate to use for trimming the data. Can be "x" or "y", or None.
        *args: Additional positional arguments.

    Returns:
        A pandas DataFrame containing the processed results file data.

    Raises:
        PyFragResultsProcessingError: If an error occurs during processing.

    """
    # Remove the dispersion term if it is 0.0 everywhere
    df = remove_dispersion_term(df)

    # Trim the data
    df = trim_data(df, trim_option, trim_key)

    # Remove outliers
    df = remove_outliers(df)

    return df

# ====================================================================================================
# Data Trimming   ====================================================================================
# ====================================================================================================


def _trim_data_str(df: pd.DataFrame, trim_option: str, energy_key: str) -> pd.DataFrame:
    """Private function that performs the actual trimming of the dataframe with a string trim_option"""
    trim_option = trim_option.lower().strip()
    options = ["min", "max"]

    if trim_option == "max":
        max_index = df[energy_key].idxmax()
        df = df.loc[:max_index]
    elif trim_option == "min":
        min_index = df[energy_key].idxmin()
        df = df.loc[:min_index]
    else:
        raise PyFragResultsProcessingError(section="trim_data_str", message=f"trim_option {trim_option} is not valid. Valid options are {options}")

    return df


def _trim_data_float(df: pd.DataFrame, trim_option: float, energy_key: str) -> pd.DataFrame:
    """Private function that performs the actual trimming of the dataframe with a float trim_option"""
    index = (df[energy_key] - trim_option).abs().idxmin()
    df = df.loc[:index]
    return df


def _trim_data_int(df: pd.DataFrame, trim_option: int, *args) -> pd.DataFrame:
    """Private function that performs the actual trimming of the dataframe with a integer trim_option"""
    df = df.iloc[:trim_option]
    return df


def _trim_data_sequence(df: pd.DataFrame, trim_option: Optional[Sequence[float]] = None, irc_coord: Optional[str] = None) -> pd.DataFrame:
    """ Private function that performs the actual trimming of the dataframe with a sequence trim_option"""

    x_limits: Sequence[float] = tuple(config["config"].get("SHARED", "x_limits")) if trim_option is None else trim_option
    reverse_axis = bool(config["config"].get("SHARED", "reverse_x_axis"))

    if irc_coord is None:
        irc_coord: str = "bondlength_1"
        message = f"irc_coord {irc_coord} is not correct. Valid options are bondlength_x, angle_x, or dihedral_x. Using default value {irc_coord} WHICH MAY NOT BE PRESENT."
        raise PyFragResultsProcessingWarning(section="trim_data_sequence",
                                             message=message)

    if not isinstance(x_limits, Sequence) or len(x_limits) != 2 or x_limits[0] >= x_limits[1]:
        raise PyFragResultsProcessingError(section="trim_data_sequence", message=f"Invalid x_limits {x_limits} specified in the configuration file.")

    x_data: np.ndarray = df[irc_coord].values  # type: ignore since it is a numpy array
    x_min = max(x_data.min(), x_limits[0])
    x_max = min(x_data.max(), x_limits[1])
    x_indices = np.where((x_data >= x_min) & (x_data <= x_max))[0]
    if x_indices.size == 0:
        raise PyFragResultsProcessingError(section="trim_data_sequence", message=f"No data points within the specified x limits {x_limits} for key {irc_coord}.")

    if not reverse_axis:
        x_indices = np.concatenate(([max(0, x_indices[0] - 1)], x_indices, [min(x_data.size - 1, x_indices[-1] + 1)]))
    else:
        x_indices = np.concatenate(([max(0, x_indices[0] + 1)], x_indices, [min(x_data.size - 1, x_indices[-1] - 1)]))

    df = df.iloc[x_indices]
    return df


_overload_types: Dict[Any, Callable[..., pd.DataFrame]] = {
    str: _trim_data_str,
    float: _trim_data_float,
    int: _trim_data_int,
    Sequence: _trim_data_sequence,
}


def trim_data(df: pd.DataFrame, trim_option: Optional[Union[str, float, int, Sequence]] = None, trim_key: Optional[str] = None) -> pd.DataFrame:
    """'Overloaded' function to trim the dataframe based on the type of the trim_option.

    This function trims the given dataframe based on the type of the trim_option.
    The trim_option is read from the configuration file and can be either a string ("min", "max"), integer (IRC point), float (energy value), or a sequence (x_limits such as (1.0, 3.0))).
    The function returns the trimmed dataframe.

    Args:
        df (pd.DataFrame): The dataframe to trim.
        trim_option (Optional[Union[str, float, int]]): The parameter to use for trimming. Defaults to None.
        trim_key (Optional[str]): The key to use for reading the trim_option from the configuration file. Defaults to None.
        irc_coord (Optional[str]): The IRC coordinate to use for trimming. Defaults to None.

    Raises:
        PyFragResultsProcessingError: If the trim_option is not a valid type.

    Returns:
        pd.DataFrame: The trimmed dataframe.

    """
    trim_key = config["config"].get("SHARED", "trim_key") if trim_key is None else trim_key
    trim_option = config["config"].get("SHARED", "trim_option") if trim_option is None else trim_option

    if not isinstance(trim_option, (str, float, int, Sequence)):
        raise PyFragResultsProcessingError(section="trim_data", message=f"trim_option {trim_option} is not a valid type. Valid types are str, float, and int")

    # Handle the case where the trim_option is a string but needs to be converted to a sequence (i.e. x_lim)
    if isinstance(trim_option, str):
        trim_option = trim_option.lower().strip()
        if trim_option in ["x_lim", "xlim", "x_limits", "xlimits"]:
            trim_option = tuple(config["config"].get("SHARED", "x_lim"))
        return df

    for key, value in _overload_types.items():
        if isinstance(trim_option, key):
            return value(df, trim_option, trim_key)

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

def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Removes outliers from the dataframe.

    This function takes a pandas DataFrame containing the results file data and removes outliers from the dataframe. The function returns the modified DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the results file data.

    Returns:
        pd.DataFrame: The modified DataFrame without outliers.

    """
    # Calculate the difference between each value and its neighbors
    diff = df["EnergyTotal"].diff().abs()

    # Identify the outliers
    outliers = diff > 70

    # Remove the outliers
    df = df[~outliers]

    return df
