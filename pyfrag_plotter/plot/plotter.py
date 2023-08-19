from __future__ import annotations
import os
from os.path import join as opj
from typing import List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from attrs import define, field

from pyfrag_plotter.config_handler import config
from pyfrag_plotter.plot.plot_details import set_figure_details, set_axes_details
from pyfrag_plotter.pyfrag_object import PyFragResultsObject


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

    def _standard_plot_routine(self, type: str, keys: Sequence[str], ax: Optional[plt.Axes] = None):
        """The plot routine for the EDA, ASM and extra strain plots

        Args:
            type (str): The type of plot to make (eda, asm or extra_strain)
           
            keys (list[str]): The keys to plot that should match the keys in the corresponding dictionary type (asm, eda or extra_strain)
        """
        ax = plt.gca() if ax is None else ax
        x_axes = [obj.get_x_axis(self.plot_info.irc_coord) for obj in self.objects]

        for i, (line_style, term) in enumerate(zip(self.plot_info.line_styles, keys)):
            for x_axis, colour, obj in zip(x_axes, self.plot_info.colours, self.objects):
                standard_block = obj.__getattribute__(type)  # eda, asm or extra_strain
                term_data = standard_block[term]
                
                # Plot the data
                if i == 0:
                    ax.plot(x_axis, term_data, label=obj.name, color=colour, linestyle=line_style)

                    if self.plot_info.peak_type is not None:
                        peak_index, peak_value = obj.get_peak_of_key(key=term, peak=self.plot_info.peak_type)
                        ax.scatter(x_axis[peak_index], peak_value, color=colour, s=50)
                        continue

                ax.plot(x_axis, term_data, color=colour, linestyle=line_style)

    def plot_asm(self, keys: Optional[List[str]] = None, **kwargs):
        """ Plots the activation strain model terms. The user can specify which terms to plot, otherwise all of them are plotted

        Args:
            keys (Optional[List[str]], optional): Keys that are plotted. Defaults to None (plot all keys).
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            asm_keys: List[str] = config["config"].get("ASM", "ASM_keys")
        else:
            asm_keys = keys

        self._standard_plot_routine("asm", asm_keys, ax)

        # Set the key-specific plot details
        set_axes_details(ax=ax, x_label=self.plot_info.irc_coord_label)
        set_figure_details(fig=fig,
                         title=f"ASM_{'_'.join(asm_keys)}",
                         savefig=opj(self.path, f"ASM_{'_'.join(asm_keys)}.png",)
                        )
        return fig, ax
        
    def plot_eda(self, keys: Optional[List[str]] = None):
        """ Plots the energy decomposition terms. The user can specify which terms to plot, otherwise all of them are plotted

        Args:
            keys (Optional[List[str]], optional): Keys that are plotted. Defaults to None (plot all keys).
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            eda_keys: List[str] = config["config"].get("EDA", "EDA_keys")
        else:
            eda_keys = keys

        self._standard_plot_routine("eda", eda_keys)

        # Set the key-specific plot details
        set_axes_details(ax=ax, x_label=self.plot_info.irc_coord_label)
        set_figure_details(fig=fig,
                         title=f"EDA_{'_'.join(eda_keys)}",
                         savefig=opj(self.path, f"ASM_{'_'.join(eda_keys)}.png",)
                        )

    def plot_extra_strain(self, keys: Optional[List[str]] = None):
        """ Plots the extra strain terms. The user can specify which terms to plot, otherwise all of them are plotted

        Args:
            keys (Optional[List[str]], optional): Keys that are plotted. Defaults to None (plot all keys).
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            extra_keys: List[str] = config["config"].get("ASM", "ASM_strain_keys")
        else:
            extra_keys = keys

        self._standard_plot_routine("extra_strain", extra_keys)

        # Set the key-specific plot details
        set_axes_details(ax=ax, x_label=self.plot_info.irc_coord_label)
        set_figure_details(fig=fig,
                         title=f"Strain_{'_'.join(extra_keys)}",
                         savefig=opj(self.path, f"ASM_{'_'.join(extra_keys)}.png",)
                        )


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


    def plot_multiple_graphs(self, plot_instances: Sequence[Plotter], type: str, keys: Sequence[str], path_to_images: Optional[Sequence[str]] = None, **kwargs):
        num_figs = len(plot_instances)
        num_rows = (num_figs - 1) // 3 + 1
        num_cols = min(num_figs, 3)
        image_paths: Sequence[str] = [] if path_to_images is None else path_to_images
        
        fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(num_cols * 5, num_rows * 3), sharey="row", sharex="col", squeeze=False)
        
        for i, (plot_instance, ax, image_path) in enumerate(zip(plot_instances, axes.flatten(), image_paths)):
            y_label = ""
            x_label = ""
            if i % num_cols == 0:
                y_label = "\u0394$\it{E}$ / kcal mol$^{-1}$"
                
            if i // num_cols == num_rows - 1:
                x_label = self.plot_info.irc_coord_label
            
            plot_instance._standard_plot_routine(type, keys, ax)
            set_axes_details(ax=ax, x_label=x_label, y_label=y_label)
            # ax.set_title(plot_instance.path.split("/")[-1])
            
            # Add the image to the top right corner of the subplot
            img = plt.imread(image_path)
            imagebox = OffsetImage(img, zoom=0.065)
            ab = AnnotationBbox(imagebox, xy=(0.70, 0.80), xycoords='axes fraction', frameon=False, zorder=5)
            ax.add_artist(ab)            
           
        # Remove overlapping keys from kwargs
        overlapping_keys = set(kwargs.keys()) & set(['fig', 'title', 'tight_layout'])
        [kwargs.pop(key) for key in overlapping_keys]   
                
        # Set the key-specific plot details
        set_figure_details(fig=fig,
                        title=f"Combined_{'_'.join(keys)}",
                        tight_layout=False,
                        **kwargs
                        )