# Plots the figures for the squaramides paper (dimer and trimer)

import os
from typing import Any, List, Sequence
import matplotlib.pyplot as plt
from pyfrag_plotter.config_handler import initialize_pyfrag_plotter
from pyfrag_plotter.pyfrag_object import create_pyfrag_object_from_dir
from pyfrag_plotter.plot.plotter import Plotter

# ------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Path parameters ------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------- #


base_results_path = r"/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Projects/Squaramides/pyfrag_results"
# base_results_path = r"C:\Users\siebb\VU_PhD\PhD\Projects\Squaramides\pyfrag_results"

plot_dir = r"/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Projects/Squaramides/Plots"
# plot_dir = r"C:\Users\siebb\VU_PhD\PhD\Projects\Squaramides\Plots"

# irc_coord = ("bondlength_1", "r - r$_{eq}$ / Å")
# irc_coord = ("bondlength_2", "r$_{cm}$ / Å")
# irc_coord = ("bondlength_3", "$\Delta$r$_{X \cdot\cdot\cdot H}$ / Å")
irc_coord = ("bondlength_4", "r$_{X \cdot\cdot\cdot H}$ / Å")   # type: ignore # noqa: W605 since it is a LaTeX string

path_to_images = r"/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Projects/Squaramides/Pics&Coords/png_without_border"
# path_to_images = r"C:\Users\siebb\VU_PhD\PhD\Projects\Squaramides\Pics&Coords/png_without_border"

# ------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------- Functions ---------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------- #


def create_plot_instances(systems: dict[str, List[str]]) -> List[Plotter]:
    """ Creates the plot instances for the given systems """
    plot_instances = []

    # Get the pyfrag input file and pyfrag output file
    pyfrag_dirs = {name: [os.path.join(base_results_path, dir) for dir in dirs] for name, dirs in systems.items()}

    # Make the plot instances
    for name, folders in pyfrag_dirs.items():
        print(f"Making plot instance for {name}")

        # First, make the pyfrag objects with arguments for processing the functions (trimming data, removing dispersion term, and removing outliers)
        objs = [create_pyfrag_object_from_dir(folder, trim_option="x_lim", trim_key=irc_coord[0]) for folder in folders]

        # Next, make the Plotter
        plot_instances.append(Plotter(name, plot_dir, objs, irc_coord))

    return plot_instances


def plot_individual_graphs(plot_instances: Sequence[Plotter]):
    for plot_instance in plot_instances:
        plot_instance.plot_asm()  # ["EnergyTotal"]
        plot_instance.plot_eda()  # ["EnergyTotal"]
        plt.show()


dimer_systems: dict[str, List[str]] = {
    "urea_series": ["ureas_di_O_Cs_all", "ureas_di_S_Cs_all", "ureas_di_Se_Cs_all"],
}

# ------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- Main Routine - ------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------- #

# Initialize the pyfrag plotter module (deals with config settings)
initialize_pyfrag_plotter()

# Create the plot instances
dimer_instances = create_plot_instances(dimer_systems)


# print("Plotting the individual graphs")
# plot_individual_graphs(plot_instances=plot_instances)

shared_keywords: dict[str, Any] = {
    "plot_type": "asm",
    "plot_keys": ["Int"],
    "x_label": "r$_{X ••• H}$ / Å",  # type: ignore # noqa: W605 since it is a LaTeX string
    "y_label": "\u0394$\it{E}$ / kcal mol$^{-1}$",   # type: ignore # noqa: W605 since it is a LaTeX string
    "n_max_y_ticks": 4,
}

dimer_specific_keywords = {
    "y_lim": (-20.0, 20.0),
    "image_zoom": 0.065,
}

trimer_specific_keywords = {
    "y_lim": (-30.0, 30.0),
    "image_zoom": 0.092,
}

print("Plot directory: ", plot_dir)
plot_individual_graphs(dimer_instances)
