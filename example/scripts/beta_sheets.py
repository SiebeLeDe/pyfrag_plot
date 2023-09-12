from pyfrag_plotter.config_handler import initialize_pyfrag_plotter
from pyfrag_plotter.pyfrag_object import create_pyfrag_object_from_dir
from pyfrag_plotter.plot.plotter import Plotter

from os.path import join as opj

base_dir = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Scripting/local_packages/theochem/example/"
systems = ["ureas_di_O_Cs_all", "ureas_di_O_Cs_sigma", "ureas_di_O_Cs_pi"]
plot_dir = "/Users/siebeld/Desktop/plots"
config_file = "/Users/siebeld/Desktop/extra_config.ini"


initialize_pyfrag_plotter(config_file)

# Initialize the PyFragPlotter
objs = [create_pyfrag_object_from_dir(opj(base_dir, system)) for system in systems]
plotter = Plotter(name="legend_test", pyfrag_objects=objs, plot_dir=plot_dir, irc_coord=("bondlength_1", "Hbond distance / A"))
plotter.plot_asm(["EnergyTotal"])
plotter.plot_eda()
