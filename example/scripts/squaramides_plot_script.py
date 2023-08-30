# Plots the figures for the squaramides paper (dimer and trimer)

import os
from typing import List, Sequence, Optional
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from pyfrag_plotter.config_handler import initialize_pyfrag_plotter
from pyfrag_plotter.helper_funcs import get_pyfrag_files
from pyfrag_plotter.input.read_inputfile import read_inputfile
from pyfrag_plotter.input.read_resultsfile import read_data
from pyfrag_plotter.processing_funcs import trim_data, remove_dispersion_term
from pyfrag_plotter.pyfrag_object import create_pyfrag_object
from pyfrag_plotter.plot.plotter import Plotter
from pyfrag_plotter.plot.plot_details import set_figure_details, set_axes_details


# ------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------- Functions ---------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------- #


def create_plot_instances(systems: dict[str, List[str]]) -> List[Plotter]:
    """ Creates the plot instances for the given systems """
    plot_instances = []

    # Get the pyfrag input file and pyfrag output file
    pyfrag_dirs = {name: [os.path.join(base_results_path, dir) for dir in dirs] for name, dirs in systems.items()}
    pyfrag_files = {name: get_pyfrag_files(pyfrag_dir) for name, pyfrag_dir in pyfrag_dirs.items()}

    # Make the plot instances
    for name, pyfrag_file_list in pyfrag_files.items():
        print(f"Making plot instance for {name}")
        input_files, results_files = zip(*pyfrag_file_list)
        input_contents = [read_inputfile(input_file) for input_file in input_files]
        output_contents = [read_data(results_file) for results_file in results_files]

        # Process output contents
        output_contents = [trim_data(output_content) for output_content in output_contents]
        output_contents = [remove_dispersion_term(output_content) for output_content in output_contents]

        # Next, make the pyfrag objects
        objs = [create_pyfrag_object(output_content, input_content) for output_content, input_content in zip(output_contents, input_contents)]

        # Next, make the Plotter
        plot_instances.append(Plotter(name, plot_dir, objs, irc_coord))

    return plot_instances


def plot_individual_graphs(plot_instances: Sequence[Plotter]):
    plot_key = "asm"
    for plot_instance in plot_instances:
        plot_instance.plot_asm([plot_key])  # ["EnergyTotal"]
        plt.show()


def plot_dimer_graph(plot_instances: Sequence[Plotter],
                     savefig: str,
                     path_to_images: Optional[Sequence[str]] = None):
    """ Plots the dimer graphs for the squaramides paper"""

    plot_type = "asm"
    plot_keys = ["Int"]
    x_label: str = "r$_{X \cdot\cdot\cdot H}$ / Å"
    y_label: str = "\u0394$\it{E}$ / kcal mol$^{-1}$"

    num_figs = len(plot_instances)
    num_rows = (num_figs - 1) // 3 + 1
    num_cols = min(num_figs, 3)
    image_paths: Sequence[str] = [] if path_to_images is None else path_to_images

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(num_cols * 5, num_rows * 3), sharey="row", sharex="col", squeeze=False)

    for i, (plot_instance, ax, image_path) in enumerate(zip(plot_instances, axes.flatten(), image_paths)):
        plot_y_label = ""
        plot_x_label = ""
        if i % num_cols == 0:
            plot_y_label = y_label

        if i // num_cols == num_rows - 1:
            plot_x_label = x_label

        plot_instance._standard_plot_routine(plot_type, plot_keys, ax)
        set_axes_details(ax=ax, x_label=plot_x_label, y_label=plot_y_label, n_max_y_ticks=6, y_lim=(-25.0, 25.0))
        # ax.set_title(plot_instance.path.split("/")[-1])

        # Add the image to the top right corner of the subplot
        img = plt.imread(image_path)
        imagebox = OffsetImage(img, zoom=0.065)
        ab = AnnotationBbox(imagebox, xy=(0.70, 0.80), xycoords='axes fraction', frameon=False, zorder=0)
        ax.add_artist(ab)

    # Set the key-specific plot details
    set_figure_details(fig=fig,
                       title=f"Combined_{'_'.join(plot_keys)}",
                       tight_layout=False,
                       savefig=savefig,
                       )


def plot_trimer_graph(plot_instances: Sequence[Plotter],
                      savefig: str,
                      path_to_images: Optional[Sequence[str]] = None):
    """ Plots the dimer graphs for the squaramides paper"""

    plot_type = "asm"
    plot_keys = ["Int"]
    x_label: str = "r$_{X \cdot\cdot\cdot H}$ / Å"
    y_label: str = "\u0394$\it{E}$ / kcal mol$^{-1}$"

    num_figs = len(plot_instances)
    num_rows = (num_figs - 1) // 3 + 1
    num_cols = min(num_figs, 3)
    image_paths: Sequence[str] = [] if path_to_images is None else path_to_images

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(num_cols * 5, num_rows * 3), sharey="row", sharex="col", squeeze=False)

    for i, (plot_instance, ax, image_path) in enumerate(zip(plot_instances, axes.flatten(), image_paths)):
        plot_y_label = ""
        plot_x_label = ""
        if i % num_cols == 0:
            plot_y_label = y_label

        if i // num_cols == num_rows - 1:
            plot_x_label = x_label

        plot_instance._standard_plot_routine(plot_type, plot_keys, ax)
        set_axes_details(ax=ax, x_label=plot_x_label, y_label=plot_y_label, n_max_y_ticks=4, y_lim=(-30.0, 30.0))
        # ax.set_title(plot_instance.path.split("/")[-1])

        # Add the image to the top right corner of the subplot
        img = plt.imread(image_path)
        imagebox = OffsetImage(img, zoom=0.092)
        ab = AnnotationBbox(imagebox, xy=(0.70, 0.80), xycoords='axes fraction', frameon=False, zorder=0)
        ax.add_artist(ab)

    # Set the key-specific plot details
    set_figure_details(fig=fig,
                       title=f"Combined_{'_'.join(plot_keys)}",
                       tight_layout=False,
                       savefig=savefig,
                       )


# ------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- Path parameters ------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------- #

base_results_path = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Projects/Squaramides/pyfrag_results"
# base_results_path = r"C:\Users\siebb\VU_PhD\PhD\Projects\Squaramides\pyfrag_results"

plot_dir = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Projects/Squaramides/Plots"
# plot_dir = r"C:\Users\siebb\VU_PhD\PhD\Projects\Squaramides\Plots"

# irc_coord = ("bondlength_1", "r - r$_{eq}$ / Å")
# irc_coord = ("bondlength_2", "r$_{cm}$ / Å")
# irc_coord = ("bondlength_3", "$\Delta$r$_{X \cdot\cdot\cdot H}$ / Å")
irc_coord = ("bondlength_4", "r$_{X \cdot\cdot\cdot H}$ / Å")

path_to_images = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Projects/Squaramides/Pics&Coords/png_without_border"
# path_to_images = r"C:\Users\siebb\VU_PhD\PhD\Projects\Squaramides\pyfrag_results"


# -------------------------------------------- Dimer Data ---------------------------------------------------- #

dimer_systems: dict[str, List[str]] = {
    "O_di_ureas": ["ureas_di_O_Cs_all", "ureas_di_O_Cs_sigma", "ureas_di_O_Cs_pi"],
    "S_di_ureas": ["ureas_di_S_Cs_all", "ureas_di_S_Cs_sigma", "ureas_di_S_Cs_pi"],
    "Se_di_ureas": ["ureas_di_Se_Cs_all", "ureas_di_Se_Cs_sigma", "ureas_di_Se_Cs_pi"],
    "O_di_deltamides": ["deltamides_di_O_Cs_all", "deltamides_di_O_Cs_sigma", "deltamides_di_O_Cs_pi"],
    "S_di_deltamides": ["deltamides_di_S_Cs_all", "deltamides_di_S_Cs_sigma", "deltamides_di_S_Cs_pi"],
    "Se_di_deltamides": ["deltamides_di_Se_Cs_all", "deltamides_di_Se_Cs_sigma", "deltamides_di_Se_Cs_pi"],
    "O_di_squaramides": ["squaramides_di_O_Cs_all", "squaramides_di_O_Cs_sigma", "squaramides_di_O_Cs_pi"],
    "S_di_squaramides": ["squaramides_di_S_Cs_all", "squaramides_di_S_Cs_sigma", "squaramides_di_S_Cs_pi"],
    "Se_di_squaramides": ["squaramides_di_Se_Cs_all", "squaramides_di_Se_Cs_sigma", "squaramides_di_Se_Cs_pi"],
}

dimer_images = [
    "urea_di_O", "urea_di_S", "urea_di_Se",
    "deltamide_di_O", "deltamide_di_S", "deltamide_di_Se",
    "squaramide_di_O", "squaramide_di_S", "squaramide_di_Se",
]

# -------------------------------------------- Trimer Data ---------------------------------------------------- #

trimer_systems: dict[str, List[str]] = {
    "O_tri_ureas": ["ureas_tri_O_Cs_all", "ureas_tri_O_Cs_sigma", "ureas_tri_O_Cs_pi"],
    "S_tri_ureas": ["ureas_tri_S_Cs_all", "ureas_tri_S_Cs_sigma", "ureas_tri_S_Cs_pi"],
    "Se_tri_ureas": ["ureas_tri_Se_Cs_all", "ureas_tri_Se_Cs_sigma", "ureas_tri_Se_Cs_pi"],
    "O_tri_deltamides": ["deltamides_tri_O_Cs_all", "deltamides_tri_O_Cs_sigma", "deltamides_tri_O_Cs_pi"],
    "S_tri_deltamides": ["deltamides_tri_S_Cs_all", "deltamides_tri_S_Cs_sigma", "deltamides_tri_S_Cs_pi"],
    "Se_tri_deltamides": ["deltamides_tri_Se_Cs_all", "deltamides_tri_Se_Cs_sigma", "deltamides_tri_Se_Cs_pi"],
    "O_tri_squaramides": ["squaramides_tri_O_Cs_all", "squaramides_tri_O_Cs_sigma", "squaramides_tri_O_Cs_pi"],
    "S_tri_squaramides": ["squaramides_tri_S_Cs_all", "squaramides_tri_S_Cs_sigma", "squaramides_tri_S_Cs_pi"],
    "Se_tri_squaramides": ["squaramides_tri_Se_Cs_all", "squaramides_tri_Se_Cs_sigma", "squaramides_tri_Se_Cs_pi"],
}

trimer_images = [
    "urea_tri_O", "urea_tri_S", "urea_tri_Se",
    "deltamide_tri_O", "deltamide_tri_S", "deltamide_tri_Se",
    "squaramide_tri_O", "squaramide_tri_S", "squaramide_tri_Se",
]


# ------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- Main Routine - ------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------- #

# Initialize the pyfrag plotter module (deals with config settings)
initialize_pyfrag_plotter()

dimer_instances = create_plot_instances(dimer_systems)
trimer_instances = create_plot_instances(trimer_systems)

# print("Plotting the individual graphs")
# plot_individual_graphs(plot_instances=plot_instances)

print("Plotting the dimer graph")
plot_dimer_graph(plot_instances=dimer_instances,
                 savefig=os.path.join(plot_dir, "dimer_graph.png"),
                 path_to_images=[os.path.join(path_to_images, f"{image}.png") for image in dimer_images]
                 )

print("Plotting the trimer graph")
plot_trimer_graph(plot_instances=trimer_instances,
                  savefig=os.path.join(plot_dir, "trimer_graph.png"),
                  path_to_images=[os.path.join(path_to_images, f"{image}.png") for image in trimer_images]
                  )

plt.show()
