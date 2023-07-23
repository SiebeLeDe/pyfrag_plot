# Script that specifies general plot parameters used in the pyfrag_plotter.py file
from typing import List
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use("Agg")


def initialize_plot_parameters():
    """
    Applies plot-specific parameters for the the PlotClasses.py file
    """

    # Get a list of available fonts of matplotlib
    # import matplotlib.font_manager
    # flist = matplotlib.font_manager.get_fontconfig_fonts()
    # names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist]
    # print(names)

    # mp.font_manager._rebuild()
    # font = fp.FontProperties(fname=r"C:\\Windows\\Fonts\\Helvetica Regulier.ttf")
    # print(font.get_name())

    # Figure size
    plt.rcParams["figure.figsize"] = (10, 8)

    # Fontsize
    plt.rcParams["font.family"] = ["Arial"]

    # Takes care of ticks starting at the edge of the screen
    plt.rcParams["axes.autolimit_mode"] = "round_numbers"
    plt.rcParams["axes.xmargin"] = 0.00
    plt.rcParams["axes.ymargin"] = 0.00

    SMALL_SIZE = 20
    MEDIUM_SIZE = 25
    BIGGER_SIZE = 29

    plt.rc("font", size=MEDIUM_SIZE)  # controls default text sizes
    plt.rc("axes", titlesize=BIGGER_SIZE)  # fontsize of the axes title
    plt.rc("axes", labelsize=BIGGER_SIZE)  # fontsize of the x and y labels
    plt.rc("xtick", labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    plt.rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc("figure", titlesize=SMALL_SIZE)  # fontsize of the figure title


# Plot parameters
EDA_keys = ["Int", "Elstat", "OI", "Pauli", "Disp"]
EDA_names = ["Eint", "Velstat", "Eoi", "Epauli", "Edisp"]
EDA_styles = ["solid", "dashed", "dotted", "dashdot", " "]

ASM_keys = ['Int']
# ASM_keys = ["EnergyTotal", "Int", "StrainTotal", "frag1Strain", "frag2Strain"]
ASM_strain_keys = ["StrainTotal", "frag1Strain", "frag2Strain"]
ASM_names = [
    "\u0394Ebond",
    "\u0394Eint",
    "\u0394Estrain",
    "\u0394Estrain",
    "\u0394Estrain1",
    "\u0394Estrain2",
]
ASM_styles = ["solid", "dashed", "dotted", "dashdot"]

solo_col = [
    "black",
    "red",
    "blue",
    "orange",
    "green",
    "yellow",
    "lime",
    "gold",
    "brown",
    "fuchsia",
]
colors = {
    "chalcs": ["black", "red", "blue"],  # [(248/256, 37/256, 0/256), (213/256, 199/256, 17/256), (250/256, 165/256, 1/256)],
    "orbs": ["black", "red", "blue"],  # "orange", "green", "yellow", "lime", "gold"],
    "extra": ["black", "red", "blue"],  # "brown", "fuchsia"],
}

sub_colors = ["black", "blue", "red"]
styles = ["solid", "dashed", "dotted", "dashdot"]

# Unit conversion
har_eV_ratio = 27.211  # 1 hartree = 27.211 eV

# Outlier threshold for cleaning up data (outliers originate from a restricted calculation that should have been unrestricted)
outlier_threshold = 70  # kcal/mol

# y limits for all plots
ASM_ylim: List[float] = [-20, 20]  # [-80, 80]
strain_ylim: List[float] = [0, 50]
EDA_ylim: List[float] = [-20, 20]

# x limits for all plots
xlim: List[float] = [-0.5, 0.5]

# Determines if a vertical line should be plotted (mostly used for visualizing the interpolation line)
vline = None

# stationary point, searching for a minimum or maximum
stat_point = "min"
