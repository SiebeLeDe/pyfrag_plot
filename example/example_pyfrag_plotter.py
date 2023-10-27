import os
from pyfrag_plotter import initialize_pyfrag_plotter
from pyfrag_plotter.pyfrag_object import create_pyfrag_object_from_dir
from pyfrag_plotter.plot.plotter import Plotter

# ------- User Input -------

# Specify variables and parameters such as the current directory, the directory containing the pyfrag results, the directory to save the plots to, and the config file.
current_dir_path = os.path.dirname(os.path.abspath(__file__))
pyfrag_dir = current_dir_path
plot_dir = os.path.join(current_dir_path, "new_example_plots")
config_file = os.path.join(current_dir_path, "example_config.ini")

# Specify the directories (that are in the pyfrag_dir) containing the pyfrag results
result_dirs = ["ureas_di_O_Cs_all", "ureas_di_O_Cs_pi", "ureas_di_O_Cs_sigma"]

# Create the full paths to the directories containing the pyfrag results
pyfrag_dirs = [os.path.join(pyfrag_dir, directory) for directory in result_dirs]

# ------- Running the script -------

# First, initialize the config file
initialize_pyfrag_plotter(user_config_file=config_file)

# Create the pyfrag objects. These objects contain all the information about the pyfrag results.
objs = [create_pyfrag_object_from_dir(pyfrag_dir) for pyfrag_dir in pyfrag_dirs]

# Create the plotter object
plot_inst = Plotter(name="O_tri_ureas", plot_dir=plot_dir, pyfrag_objects=objs, irc_coord=("bondlength_1",  "r - r$_{eq}$ / Å"))

# Now the actual plotting starts. A Plotter instance has predefined functions to plot the results such as `plot_asm` and `plot_eda`.
# Check `set_figure_details` and `set_axis_details` in pyfrag_plotter/plot/plot_details.py for more options to pass on.
with plot_inst as plotter:
    plotter.plot_asm()
    plotter.plot_asm(["EnergyTotal"], plot_legend=False)
    plotter.plot_eda(["Int", "Pauli", "Elstat", "OI"])
    plotter.plot_eda(["Int"])
    plotter.plot_eda(["Elstat", "OI"])
    plotter.plot_eda(["OI"])


# Other results can also be plotted by using `plot_arbitrary_keys` and specifying the keys to plot.
with plot_inst as plotter:
    plotter.plot_arbitrary_keys(title="Arbitrary_plot", keys=["bondlength_1"], y_lim=[0, 0.5])
