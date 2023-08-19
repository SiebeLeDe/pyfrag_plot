from typing import Optional, Tuple, Sequence
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import matplotlib.figure
import math
from scipy.interpolate import BSpline, make_interp_spline
import numpy as np

from pyfrag_plotter.config_handler import config
from pyfrag_plotter.helper_funcs import replace_overlapping_keys

def interpolate_plot(x_axis: np.ndarray, y_axis: np.ndarray, x_range: Optional[Sequence[float]] = None) -> Tuple[np.ndarray, BSpline]:
    """ Function that aims to interpolate the data to a finer grid for plotting purposes using the scipy spline library"""
    if x_range is None:
        x_min, x_max = x_axis.min(), x_axis.max() 
    else:
        x_min, x_max = x_range[0], x_range[1]

    mask = (x_axis >= x_min) & (x_axis <= x_max)
    x_filtered = x_axis[mask]
    y_filtered = y_axis[mask]
    X_Y_Spline = make_interp_spline(x_filtered, y_filtered)

    # Returns evenly spaced numbers over a specified interval.
    X_ = np.linspace(x_min, x_max, 100)
    Y_ = X_Y_Spline(X_)
    return X_, Y_

@replace_overlapping_keys
def set_figure_details(
    fig: Optional[matplotlib.figure.Figure] = None,
    title: Optional[str] = None,
    savefig: Optional[str] = None,
    show_plot: Optional[bool] = False,
    clear_plot: Optional[bool] = False,
    tight_layout: Optional[bool] = True,
):
    """
    Function that specifies figure options for making a shorter and cleaner code
    """
    fig = plt.gcf() if fig is None else fig

    # Fixes the large padding between the axes and the labels of the axes
    if tight_layout:
        fig.tight_layout()

    if title is not None:
        fig.suptitle(title, fontweight='bold', y=1.00)

    # Saves the figure in standard .png format.
    if savefig is not None:
        fig.savefig(savefig, dpi=600)

    if show_plot:
        plt.show()
        
    if clear_plot:
        plt.clf()

@replace_overlapping_keys
def set_axes_details(
    ax: Optional[plt.Axes] = None,
    x_label: str = "\u0394r / \u00c5",
    y_label: str = "\u0394$\it{E}$ / kcal mol$^{-1}$",  # type: ignore # noqa: W605 since it is a LaTeX string
    y_lim: Optional[Tuple[float, float]] = None,
):
    """
    Function that specifies axes options for making a shorter and cleaner code
    """
    ax = plt.gca() if ax is None else ax

    # Plot labels
    ax.set_xlabel(x_label, labelpad=20)
    ax.set_ylabel(y_label, labelpad=20)

    # Specfies the y limits
    if y_lim is None:
        default_y_lim = config["config"].get("SHARED", "y_lim")
        ax.set_ylim(default_y_lim[0], default_y_lim[1])
    else:
        ax.set_ylim(y_lim[0], y_lim[1])

    # Plot x limits
    x_lim = config["config"].get("SHARED", "x_lim")
    ax.set_xlim(x_lim[0], x_lim[1])

    # Reverses the plot direction by reversing the x-axis
    reverse_x_axis = config["config"].get("SHARED", "reverse_x_axis")
    if reverse_x_axis:
        ax.set_xlim(ax.get_xlim()[::-1])
        
    # Smoothens the plots in the specified range (x_lim) by interpolating the data using the scipy spline library
    for line in ax.lines:
        x, y = line.get_data()
        X_, Y_ = interpolate_plot(x, y, x_lim)
        line.set_data(X_, Y_)
    
    # Draws a vertical line at the specified point
    # First check for user input, else check for config file input
    vline = config["config"].get("SHARED", "vline")
    if not math.isclose(vline, 0.0):
        ax.vlines(
            vline,
            ax.get_ylim()[0],
            ax.get_ylim()[1],
            colors=["grey"],
            linestyles="dashed",
        )

    # Draws a horizontal line at y=0 (indicating the 'zero line')
    ax.hlines(0, ax.get_xlim()[0], ax.get_xlim()[1], colors=["grey"], linewidth=0.2)

    # Set the y-axis formatter to round to one decimal place
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    # Axes adjustments: tick markers and number of ticks
    ax.tick_params(which="both", width=1.5)
    ax.tick_params(which="major", length=7)
    ax.xaxis.set_major_locator(MaxNLocator(6))
    ax.yaxis.set_major_locator(MaxNLocator(5))

    # Removes the top en right border of the graph
    right_side = ax.spines["top"]
    top_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side.set_visible(False)

    # Makes the x and y axis wider
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)

    # Adds more spacing between ticks and the labels
    ax.tick_params(pad=7)

    # Plots the legend at the right side of the plot
    # ax.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand")
    # ax.legend(frameon=False)