import os
from os.path import join as opj
from typing import List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
from attrs import define, field

from pyfrag_plotter.config_handler import config
from pyfrag_plotter.plot.plot_details import set_figure_details, set_axes_details
from pyfrag_plotter.pyfrag_object import PyFragResultsObject


@define
class PlotInfo:
    """Class to hold information about the plot to be generated.

    Attributes:
        irc_coord (str): The IRC coordinate to plot on the x-axis.
        irc_coord_label (str): The label for the x-axis.
        colours (List[str]): The list of colours to use for the plot.
        line_styles (List[str]): The list of line styles to use for the plot.
        peak_type (Optional[str]): The type of peak to plot, if any.

    """
    irc_coord: str
    irc_coord_label: str
    colours: List[str] = field(factory=lambda: config["config"].get("SHARED", "colours"))
    line_styles: List[str] = field(factory=lambda: config["config"].get("SHARED", "line_styles"))
    peak_type: Optional[str] = field(factory=lambda: config["config"].get("SHARED", "stat_point_type") if config.get("SHARED", "stat_point_type") != "none" else None)


class Plotter:
    """Main class for plotting the results of the PyFrag calculations.

    Attributes:
        objects (Sequence[PyFragResultsObject]): A list of PyFragResultsObject objects.
        path (str): The directory to save the plots to.
        plot_info (PlotInfo): An instance of the PlotInfo class.

    Methods:
        __init__(self, name: str, plot_dir: str, pyfrag_objects: Sequence[PyFragResultsObject], irc_coord: Sequence[str]):
            Initializes a new Plotter object with the given name, output directory, PyFragResultsObject objects, and IRC coordinate.
        _check_output_dir(self):
            Checks if the directory exists, if not, creates it (and any parent directories).
        standard_plot_routine(self, type: str, keys: Sequence[str], ax: Optional[plt.Axes] = None):
            The plot routine for the EDA, ASM and extra strain plots.
        plot_asm(self, keys: Optional[List[str]] = None, **kwargs):
            Plots the activation strain model terms. The user can specify which terms to plot, otherwise all of them are plotted.
        plot_eda(self, keys: Optional[List[str]] = None):
            Plots the energy decomposition terms. The user can specify which terms to plot, otherwise all of them are plotted.
        plot_extra_strain(self, keys: Optional[List[str]] = None):
            Plots the extra strain terms. The user can specify which terms to plot, otherwise all of them are plotted.
        plot_population(self, keys: Optional[Tuple[List[str]]] = None):
            Plots the population of the orbitals.

    """

    def __init__(self, name: str, plot_dir: str, pyfrag_objects: Sequence[PyFragResultsObject], irc_coord: Sequence[str]):
        """Initializes a new Plotter object with the given name, output directory, PyFragResultsObject objects, and IRC coordinate.

        Args:
            name (str): The name of the plotter object.
            plot_dir (str): The directory to save the plots to.
            pyfrag_objects (Sequence[PyFragResultsObject]): A list of PyFragResultsObject objects.
            irc_coord (Sequence[str]): The IRC coordinate to plot on the x-axis and the label for the x-axis.

        """
        self.objects = pyfrag_objects
        self.path = opj(plot_dir, name)
        self.plot_info = PlotInfo(irc_coord=irc_coord[0], irc_coord_label=irc_coord[1])
        self._check_output_dir()

    def _check_output_dir(self):
        """Checks if the directory exists, if not, creates it (and any parent directories)."""

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

# ------------------------------------------------------------------------------------------------------------- #
# ------------------------------ ASM, EDA and ASM extra strain plotting routines ------------------------------ #
# ------------------------------------------------------------------------------------------------------------- #

    def standard_plot_routine(self, type: str, keys: Sequence[str], ax: Optional[plt.Axes] = None):
        """The plot routine for the EDA, ASM and extra strain plots.

        Args:
            type (str): The type of plot to make (eda, asm or extra_strain).
            keys (list[str]): The keys to plot that should match the keys in the corresponding dictionary type (asm, eda or extra_strain).
            ax (Optional[plt.Axes], optional): The axes to plot on. Defaults to None.

        """
        ax = plt.gca() if ax is None else ax
        x_axes = [obj.get_x_axis(self.plot_info.irc_coord) for obj in self.objects]

        for i, (line_style, term) in enumerate(zip(self.plot_info.line_styles, keys)):
            for x_axis, colour, obj in zip(x_axes, self.plot_info.colours, self.objects):
                standard_block = obj.__getattribute__(type)  # eda, asm or extra_strain
                term_data = standard_block[term]

                # Plot the data
                if i == 0:
                    ax.plot(x_axis, term_data, label=obj.name, color=colour, linestyle=line_style, zorder=1)

                    if self.plot_info.peak_type is not None:
                        peak_index, peak_value = obj.get_peak_of_key(key=term, peak=self.plot_info.peak_type)
                        ax.scatter(x_axis[peak_index], peak_value, color=colour, s=45, zorder=2)
                        continue

                ax.plot(x_axis, term_data, color=colour, linestyle=line_style, zorder=1)

    def plot_asm(self, keys: Optional[List[str]] = None, **kwargs):
        """Plots the activation strain model terms. The user can specify which terms to plot, otherwise all of them are plotted.

        Args:
            keys (Optional[List[str]], optional): Keys that are plotted. Defaults to None (plot all keys).
            **kwargs: Additional keyword arguments to pass to the function.

        Returns:
            fig (plt.Figure): The figure object.
            ax (plt.Axes): The axes object.

        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            asm_keys: List[str] = config["config"].get("ASM", "ASM_keys")
        else:
            asm_keys = keys

        self.standard_plot_routine("asm", asm_keys, ax)

        # Set the key-specific plot details
        set_axes_details(ax=ax, x_label=self.plot_info.irc_coord_label)
        set_figure_details(fig=fig,
                           title=f"ASM_{'_'.join(asm_keys)}",
                           savefig=opj(self.path, f"ASM_{'_'.join(asm_keys)}.png",)
                           )
        return fig, ax

    def plot_eda(self, keys: Optional[List[str]] = None):
        """Plots the energy decomposition terms. The user can specify which terms to plot, otherwise all of them are plotted.

        Args:
            keys (Optional[List[str]], optional): Keys that are plotted. Defaults to None (plot all keys).

        Returns:
            fig (plt.Figure): The figure object.
            ax (plt.Axes): The axes object.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            eda_keys: List[str] = config["config"].get("EDA", "EDA_keys")
        else:
            eda_keys = keys

        self.standard_plot_routine("eda", eda_keys)

        # Set the key-specific plot details
        set_axes_details(ax=ax, x_label=self.plot_info.irc_coord_label)
        set_figure_details(fig=fig,
                           title=f"EDA_{'_'.join(eda_keys)}",
                           savefig=opj(self.path, f"ASM_{'_'.join(eda_keys)}.png",)
                           )
        return fig, ax

    def plot_extra_strain(self, keys: Optional[List[str]] = None):
        """Plots the extra strain terms. The user can specify which terms to plot, otherwise all of them are plotted.

        Args:
            keys (Optional[List[str]], optional): Keys that are plotted. Defaults to None (plot all keys).

        Returns:
            fig (plt.Figure): The figure object.
            ax (plt.Axes): The axes object.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            extra_keys: List[str] = config["config"].get("ASM", "ASM_strain_keys")
        else:
            extra_keys = keys

        self.standard_plot_routine("extra_strain", extra_keys)

        # Set the key-specific plot details
        set_axes_details(ax=ax, x_label=self.plot_info.irc_coord_label)
        set_figure_details(
            fig=fig,
            title=f"Strain_{'_'.join(extra_keys)}",
            savefig=opj(self.path, f"ASM_{'_'.join(extra_keys)}.png",)
        )
        return fig, ax

# ------------------------------------------------------------------------------------------------------------- #
# ------------------------------ Population and Orbital Energy plotting routines ------------------------------ #
# ------------------------------------------------------------------------------------------------------------- #

    def plot_population(self, keys: Optional[Tuple[List[str]]] = None):
        """Plots the population of the orbitals.

        Args:
            keys (Optional[Tuple[List[str]]], optional): The keys to plot. Defaults to None.

        Raises:
            NotImplementedError: This function is not implemented yet.

        """
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
