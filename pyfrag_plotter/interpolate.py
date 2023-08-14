""" Module that contains functions for interpolating data """

from pyfrag_plotter.pyfrag_object import PyFragResultsObject
import pandas as pd
from typing import Union, Dict
import scipy as sp


def interpolate_data(input_data: Union[PyFragResultsObject, pd.DataFrame], irc_coord: str, point: float) -> Dict[str, float]:
    """ Interface function for interpolating data that can be in the format of a PyFragResultsObject or a pandas DataFrame"""
    if isinstance(input_data, PyFragResultsObject):
        return _interpolate_pyfrag_object(input_data, irc_coord, point)
    elif isinstance(input_data, pd.DataFrame):
        return _interpolate_dataframe(input_data, irc_coord, point)
    else:
        raise TypeError(f"Input data must be either a PyFragResultsObject or a pandas DataFrame, not {type(input_data)}")


def _interpolate_pyfrag_object(obj: PyFragResultsObject, irc_coord: str, point: float):
    # Get the x-axis
    ret_dict: Dict[str, float] = {}
    x_axis = obj.get_x_axis(irc_coord)

    # Interpolate eda, asm, and extra strain keys
    for key, value in {**obj.eda, **obj.asm, **obj.extra_strain}.items():
        # Get the y-axis
        y_axis = value
        # Interpolate
        ret_dict[key] = float(sp.interpolate.interp1d(x_axis, y_axis)(point))

    for key in ["overlap", "population", "orbitalenergy", "vdd", "irrep"]:
        for i, entry in enumerate(obj.__getattribute__(key)):
            # Get the y-axis
            y_axis = entry.data

            # Interpolate
            ret_dict[f"{key}_{i+1}"] = float(sp.interpolate.interp1d(x_axis, y_axis)(point))

    return ret_dict


def _interpolate_dataframe(df: pd.DataFrame, irc_coord: str, point: float):
    raise NotImplementedError("Interpolation of dataframes is not yet implemented")
    # First, determine the x-axis
    x_axis = df[irc_coord] = df[irc_coord]

    for key in df.columns:
        # Get the y-axis
        y_axis = df[key]

        # Interpolate
        df[key] = sp.interpolate.interp1d(x_axis, y_axis)(point)
