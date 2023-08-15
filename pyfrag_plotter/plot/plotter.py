import os
from os.path import join as opj
from typing import List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
from attrs import define, field
from scipy.interpolate import BSpline, make_interp_spline
import numpy as np

from pyfrag_plotter.config_handler import config
from pyfrag_plotter.plot.plot_details import set_plot_details
from pyfrag_plotter.pyfrag_object import PyFragResultsObject


def interpolate_plot(x_axis, y_axis) -> Tuple[BSpline, BSpline]:
    """ Function that aims to interpolate the data to a finer grid for plotting purposes using the scipy spline library"""
    X_Y_Spline = make_interp_spline(x_axis, y_axis)

    # Returns evenly spaced numbers over a specified interval.
    X_ = np.linspace(x_axis.min(), x_axis.max(), 100)
    Y_ = X_Y_Spline(X_)
    return X_, Y_

@define
class PlotInfo:
    irc_coord: str
    irc_coord_label: str
    colours: List[str] = field(factory=lambda: config["config"].get("SHARED", "colours"))
    line_styles: List[str] = field(factory=lambda: config["config"].get("SHARED", "line_styles"))
    peak_type: Optional[str] = field(factory=lambda: config["config"].get("SHARED", "stat_point_type") if config.get("SHARED", "stat_point_type") != "none" else None)


class Plotter:
    def __init__(self, name: str, plot_dir: str, pyfrag_objects: Sequence[PyFragResultsObject], irc_coord: Sequence[str]):
        self.objects = pyfrag_objects
        self.path = opj(plot_dir, name)
        self.plot_info = PlotInfo(irc_coord=irc_coord[0], irc_coord_label=irc_coord[1])
        self._check_output_dir()

    def _check_output_dir(self):
        """ Checks if the directory exists, if not, creates it (and any parent directories)"""

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

# ------------------------------------------------------------------------------------------------------------- #
# ------------------------------ ASM, EDA and ASM extra strain plotting routines ------------------------------ #
# ------------------------------------------------------------------------------------------------------------- #

    def _standard_plot_routine(self, type: str, keys: list[str]):
        """The plot routine for the EDA, ASM and extra strain plots

        Args:
            type (str): The type of plot to make (eda, asm or extra_strain)
            keys (list[str]): The keys to plot that should match the keys in the corresponding dictionary type (asm, eda or extra_strain)
        """

        x_axes = [obj.get_x_axis(self.plot_info.irc_coord) for obj in self.objects]

        for i, (line_style, term) in enumerate(zip(self.plot_info.line_styles, keys)):
            for x_axis, colour, obj in zip(x_axes, self.plot_info.colours, self.objects):
                standard_block = obj.__getattribute__(type)  # eda, asm or extra_strain
                term_data = standard_block[term]
                
                # Interpolate the data (smoothening the plot)
                interpolated_x_axis, interpolated_term_data = interpolate_plot(x_axis, term_data)
                
                # Plot the data
                if i == 0:
                    plt.plot(interpolated_x_axis, interpolated_term_data, label=obj.name, color=colour, linestyle=line_style)

                    if self.plot_info.peak_type is not None:
                        peak_index, peak_value = obj.get_peak_of_key(key=term, peak=self.plot_info.peak_type)
                        plt.scatter(x_axis[peak_index], peak_value, color=colour, s=50)
                        continue

                plt.plot(interpolated_x_axis, interpolated_term_data, color=colour, linestyle=line_style)

    def plot_asm(self, keys: Optional[List[str]] = None):
        """ Plots the activation strain model terms. The user can specify which terms to plot, otherwise all of them are plotted

        Args:
            keys (Optional[List[str]], optional): Keys that are plotted. Defaults to None (plot all keys).
        """

        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            asm_keys: List[str] = config["config"].get("ASM", "ASM_keys")
        else:
            asm_keys = keys

        self._standard_plot_routine("asm", asm_keys)

        # Set the key-specific plot details
        set_plot_details(savefig=opj(self.path, f"ASM_{'_'.join(asm_keys)}.png"),
                         title=f"ASM_{len(asm_keys)}",
                         x_label=self.plot_info.irc_coord_label)

    def plot_eda(self, keys: Optional[List[str]] = None):
        """ Plots the energy decomposition terms. The user can specify which terms to plot, otherwise all of them are plotted

        Args:
            keys (Optional[List[str]], optional): Keys that are plotted. Defaults to None (plot all keys).
        """
        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            eda_keys: List[str] = config["config"].get("EDA", "EDA_keys")
        else:
            eda_keys = keys

        self._standard_plot_routine("eda", eda_keys)

        # Set the key-specific plot details
        set_plot_details(savefig=opj(self.path, f"EDA_{'_'.join(eda_keys)}.png"),
                         title=f"EDA_{len(eda_keys)}",
                         x_label=self.plot_info.irc_coord_label)

    def plot_extra_strain(self, keys: Optional[List[str]] = None):
        """ Plots the extra strain terms. The user can specify which terms to plot, otherwise all of them are plotted

        Args:
            keys (Optional[List[str]], optional): Keys that are plotted. Defaults to None (plot all keys).
        """
        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            extra_keys: List[str] = config["config"].get("ASM", "ASM_strain_keys")
        else:
            extra_keys = keys

        self._standard_plot_routine("extra_strain", extra_keys)

        # Set the key-specific plot details
        set_plot_details(savefig=opj(self.path, f"Strain_{'_'.join(extra_keys)}.png"),
                         title=f"ASM_extra_{len(extra_keys)}",
                         x_label=self.plot_info.irc_coord_label)

# ------------------------------------------------------------------------------------------------------------- #
# ------------------------------ Population and Orbital Energy plotting routines ------------------------------ #
# ------------------------------------------------------------------------------------------------------------- #

    def plot_population(self, keys: Optional[Tuple[List[str]]] = None):
        """ Plots the population of the orbitals """
        raise NotImplementedError("This function is not implemented yet")

        # Plots the keys by doing the folowwing: if no keys are specified, it plots all of them in pairs of two
        # Otherwise, it plots the specified keys in the format: [list_of_first_object[specified indices], list_of_second_object[specified indices], ...]

        # # Get the keys to plot. If none are specified, plot all of them in pairs of two
        # if keys is None:
        #     keys = [(self.objects[i].population.keys(), self.objects[i+1].population.keys()) for i in range(0, len(self.objects), 2)]
        # else:
        #     keys = [tuple(self.objects[i].population.keys() if j in indices else [] for i in range(len(self.objects))) for j, indices in enumerate(keys)]

        # # Plot the keys
        # for key_pair in keys:
        #     x_axes = [obj.get_x_axis(self.plot_info.irc_coord) for obj in self.objects]
        #     for i, (line_style, term) in enumerate(zip(self.plot_info.line_styles, key_pair)):
        #         for x_axis, colour, obj in zip(x_axes, self.plot_info.colours, self.objects):
        #             term_data = obj.population[term]
        #             # Plot the data
        #             if i == 0:
        #                 plt.plot(x_axis, term_data, label=obj.name, color=colour, linestyle=line_style)
        #             else:
        #                 plt.plot(x_axis, term_data, color=colour, linestyle=line_style)

        # # Set the plot details
        # set_plot_details(savefig=opj(self.path, "population.png"),
        #                 title="Population",
        #                 x_label=self.plot_info.irc_coord_label)
