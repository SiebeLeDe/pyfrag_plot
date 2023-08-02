from typing import Optional, Tuple
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from pyfrag_plotter.config_handler import config
import math


def set_plot_details(
    x_label: str = "\u0394r / \u00c5",
    y_label: str = "\u0394$\it{E}$ / kcal mol$^{-1}$",  # type: ignore # noqa: W605 since it is a LaTeX string
    title: Optional[str] = None,
    savefig: Optional[str] = None,
    clear: Optional[bool] = True,
    y_lim: Optional[Tuple[float, float]] = None,
    show_plot: Optional[bool] = False,
):
    """
    Function that specifies plot options for making a shorter and cleaner code
    """
    ax = plt.gca()

    if title is not None:
        plt.title(title, pad=10)

    # Plot labels
    plt.xlabel(x_label, labelpad=20)
    plt.ylabel(y_label, labelpad=20)

    # Specfies the y limits
    if y_lim is None:
        default_y_lim = config["config"].get("SHARED", "y_lim")
        plt.ylim(default_y_lim[0], default_y_lim[1])
    else:
        plt.ylim(y_lim[0], y_lim[1])

    # Plot x limits
    x_lim = config["config"].get("SHARED", "x_lim")
    plt.xlim(x_lim[0], x_lim[1])

    # Reverses the plot direction by reversing the x-axis
    reverse_x_axis = config.get("SHARED", "reverse_x_axis")
    if reverse_x_axis:
        ax.set_xlim(ax.get_xlim()[::-1])

    # Draws a vertical line at the specified point
    # First check for user input, else check for config file input
    vline = config["config"].get("SHARED", "vline")
    if not math.isclose(vline, 0.0):
        plt.vlines(
            vline,
            ax.get_ylim()[0],
            ax.get_ylim()[1],
            colors=["grey"],
            linestyles="dashed",
        )

    # Draws a horizontal line at y=0 (indicating the 'zero line')
    plt.hlines(0, ax.get_xlim()[0], ax.get_xlim()[1], colors=["grey"], linewidth=0.2)

    # Axes adjustments: tick markers and number of ticks
    ax.tick_params(which="both", width=2)
    ax.tick_params(which="major", length=7)
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(5))

    # Removes the top en right border of the graph
    right_side = ax.spines["top"]
    top_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side.set_visible(False)

    # Makes the x and y axis wider
    ax.spines["left"].set_linewidth(2)
    ax.spines["bottom"].set_linewidth(2)

    # Fixes the large padding between the axes and the labels of the axes
    plt.tight_layout()

    # Adds more spacing between ticks and the labels
    ax.tick_params(pad=10)

    # Plots the legend at the right side of the plot
    # ax.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand")
    ax.legend(frameon=False)

    # Saves the figure in standard .png format.
    plt.savefig(savefig, dpi=250)

    if show_plot:
        plt.show()

    # Clears the plot if specified
    if clear:
        plt.clf()
