""" Module that contains functions for interpolating data """
from typing import Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
import scipy as sp
from scipy.interpolate import BSpline, make_interp_spline

from pyfrag_plotter import config
from pyfrag_plotter.errors import PyFragInterpolationError
from pyfrag_plotter.pyfrag_object import Array1D, PyFragResultsObject


def interpolate_plot(x_axis: np.ndarray, y_axis: np.ndarray, x_range: Optional[Sequence[float]] = None) -> Tuple[np.ndarray, BSpline]:
    """
    Interpolates the data to a finer grid for plotting purposes using the scipy spline library.

    Args:
        x_axis (np.ndarray): The x-axis data to interpolate.
        y_axis (np.ndarray): The y-axis data to interpolate.
        x_range (Optional[Sequence[float]], optional): The range of x-axis values to interpolate over. Defaults to None.

    Returns:
        Tuple[np.ndarray, BSpline]: The interpolated x-axis and y-axis data.
    """
    n_interpolation_points = config.get("SHARED", "n_interpolation_points")
    reverse_axis = config.get("SHARED", "reverse_x_axis")
    if x_range is None:
        x_min, x_max = x_axis.min(), x_axis.max()
    else:
        x_min, x_max = x_range[0], x_range[1]

    mask = (x_axis >= x_min) & (x_axis <= x_max)
    x_filtered = x_axis[mask] if not reverse_axis else x_axis[mask][::-1]
    y_filtered = y_axis[mask] if not reverse_axis else y_axis[mask][::-1]

    try:
        X_Y_Spline = make_interp_spline(x_filtered, y_filtered, k=3)
    except ValueError as e:
        raise PyFragInterpolationError(f"Error: {e}\nThe data could not be interpolated. This is likely due to the data not strictly increasing. Please check the data, and possibly adjust the x.")

    # Returns evenly spaced numbers over a specified interval.
    X_ = np.linspace(x_min, x_max, n_interpolation_points)
    Y_ = X_Y_Spline(X_)
    return X_, Y_


def remove_duplicate_x_values(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Removes duplicate x-axis values from the input arrays.

    Args:
        x (np.ndarray): The x-axis data.
        y (np.ndarray): The y-axis data.

    Returns:
        Tuple[np.ndarray, np.ndarray]: The modified x-axis and y-axis data with duplicates removed.
    """
    # Find indices of unique x-axis values
    _, unique_indices = np.unique(x, return_index=True)

    # Sort the indices to ensure that the x-axis values are in increasing order
    unique_indices = np.sort(unique_indices)

    # Return the modified x-axis and y-axis data
    return x[unique_indices], y[unique_indices]


def interpolate_data(input_data: Union[PyFragResultsObject, pd.DataFrame], irc_coord: str, point: float) -> pd.DataFrame:
    """
    Interpolates data that can be in the format of a PyFragResultsObject or a pandas DataFrame.

    This function takes input data in the format of a PyFragResultsObject or a pandas DataFrame and interpolates the data at a specified point along the x-axis.

    Args:
        input_data (Union[PyFragResultsObject, pd.DataFrame]): The input data to interpolate.
        irc_coord (str): The name of the x-axis coordinate to interpolate along.
        point (float): The point along the x-axis to interpolate at.

    Raises:
        TypeError: If the input data is not a PyFragResultsObject or a pandas DataFrame.

    Returns:
        pandas DataFrame: A pandas DataFrame containing the interpolated data.
    """

    if isinstance(input_data, PyFragResultsObject):
        input_data = input_data.dataframe

    return _interpolate_dataframe(input_data, irc_coord, point)


def _interpolate_dataframe(df: pd.DataFrame, irc_coord: str, point: float, x_axis: Union[pd.Series, Array1D, None] = None) -> pd.DataFrame:
    """
    This function takes a pandas DataFrame and interpolates the data at a specified point along the x-axis. The interpolated data is stored in the DataFrame.

    Args:
        df (pd.DataFrame): The pandas DataFrame to interpolate.
        irc_coord (str): The name of the x-axis coordinate to interpolate along.
        point (float): The point along the x-axis to interpolate at.
        x_axis (Union[pd.Series, Array1D, None], optional): The x-axis data. If None, the data from the 'irc_coord' column of the DataFrame is used. Defaults to None.

    Returns:
        pandas DataFrame: The interpolated DataFrame at the specified point (1 row).
    """
    # First, determine the x-axis
    x_axis = df[irc_coord] if x_axis is None else x_axis  # type: ignore

    for key in df.columns:
        # Get the y-axis
        y_axis = df[key]

        # Interpolate
        df[key] = sp.interpolate.interp1d(x_axis, y_axis)(point)

    # Return the interpolated dataframe at the specified point (1 row)
    return df.iloc[[0]]
