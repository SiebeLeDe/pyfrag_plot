from pyfrag_plotter.config_handler import initialize_pyfrag_plotter
from pyfrag_plotter.pyfrag_object import create_pyfrag_object_from_dir
from pyfrag_plotter.plot.plotter import Plotter

from os.path import join as opj

base_dir = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Students/Saman/pyfrag_calcs"
systems = ["parallel", "antiparallel"]
plot_dir = "Plots"
config_file = "extra_config.ini"

config_path = opj(base_dir, config_file)
plot_dir = opj(base_dir, plot_dir)


# Initialize the PyFragPlotter program
initialize_pyfrag_plotter(config_file)

objs = [create_pyfrag_object_from_dir(opj(base_dir, system)) for system in systems]
plotter = Plotter(name="legend_test", pyfrag_objects=objs, plot_dir=plot_dir, irc_coord=("bondlength_1", "r$_{O \cdot\cdot\cdot H}$ / Å"))
plotter.plot_asm()
plotter.plot_eda(keys=["Int"], y_lim=[-100, 100])
plotter.plot_eda(keys=["Int", "Pauli"], y_lim=[-100, 100])
plotter.plot_eda(keys=["Int", "Elstat"], y_lim=[-100, 100])
plotter.plot_eda(keys=["Int", "OI"], y_lim=[-100, 100])
plotter.plot_eda(keys=["Int", "Disp"], y_lim=[-100, 100])
plotter.plot_eda(y_lim=[-100, 100])
