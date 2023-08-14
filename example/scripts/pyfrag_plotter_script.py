import os
from pyfrag_plotter.config_handler import initialize_pyfrag_plotter
from pyfrag_plotter.file_func import get_pyfrag_files
from pyfrag_plotter.input.read_inputfile import read_inputfile
from pyfrag_plotter.input.read_resultsfile import read_data
from pyfrag_plotter.processing_funcs import trim_data, remove_dispersion_term
from pyfrag_plotter.pyfrag_object import create_pyfrag_object
from pyfrag_plotter.plot.plotter import Plotter

# ------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------- Main routine ------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------- #

base_results_path = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Projects/Squaramides/pyfrag_results"
plot_dir = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Scripting/testing/dimers"
irc_coord = ("bondlength", "r - r$_{eq}$ / Å")

systems = {
    "plot_all_O_di_ureas": ["ureas_di_O_Cs_all", "ureas_di_O_Cs_sigma", "ureas_di_O_Cs_pi"],
    # "plot_all_S_di_ureas": ["ureas_di_S_Cs_all", "ureas_di_S_Cs_sigma", "ureas_di_S_Cs_pi"],
    # "plot_all_Se_di_ureas": ["ureas_di_Se_Cs_all", "ureas_di_Se_Cs_sigma", "ureas_di_Se_Cs_pi"],
    # "plot_all_O_di_deltamides": ["deltamides_di_O_Cs_all", "deltamides_di_O_Cs_sigma", "deltamides_di_O_Cs_pi"],
    # "plot_all_S_di_deltamides": ["deltamides_di_S_Cs_all", "deltamides_di_S_Cs_sigma", "deltamides_di_S_Cs_pi"],
    # "plot_all_Se_di_deltamides": ["deltamides_di_Se_Cs_all", "deltamides_di_Se_Cs_sigma", "deltamides_di_Se_Cs_pi"],
    # "plot_all_O_di_squaramides": ["squaramides_di_O_Cs_all", "squaramides_di_O_Cs_sigma", "squaramides_di_O_Cs_pi"],
    # "plot_all_S_di_squaramides": ["squaramides_di_S_Cs_all", "squaramides_di_S_Cs_sigma", "squaramides_di_S_Cs_pi"],
    # "plot_all_Se_di_squaramides": ["squaramides_di_Se_Cs_all", "squaramides_di_Se_Cs_sigma", "squaramides_di_Se_Cs_pi"],
}

pyfrag_dirs = {name: [os.path.join(base_results_path, dir) for dir in dirs] for name, dirs in systems.items()}

# Initialize the pyfrag plotter module (deals with config settings)
initialize_pyfrag_plotter("/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Scripting/local_packages/theochem/tests/fixtures/extra_config.ini")

# Get the pyfrag input file and pyfrag output file
pyfrag_files = {name: get_pyfrag_files(pyfrag_dir) for name, pyfrag_dir in pyfrag_dirs.items()}
for name, pyfrag_file_list in pyfrag_files.items():
    input_files, results_files = zip(*pyfrag_file_list)
    input_contents = [read_inputfile(input_file) for input_file in input_files]
    output_contents = [read_data(results_file) for results_file in results_files]

    # Process output contents
    output_contents = [trim_data(output_content) for output_content in output_contents]
    output_contents = [remove_dispersion_term(output_content) for output_content in output_contents]

    # Next, make the pyfrag objects
    objs = [create_pyfrag_object(output_content, input_content) for output_content, input_content in zip(output_contents, input_contents)]

    # Next, make the Plotter
    plot_inst = Plotter(name, plot_dir, objs, irc_coord)
    plot_inst.plot_asm(["Int"])  # ["EnergyTotal"]
