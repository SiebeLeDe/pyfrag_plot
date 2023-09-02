.. _Usage:

Usage
=====

pyfrag_plotter is a Python package that can be used to make plots from PyFrag directories containing the .txt (resultsfile) and .in file (inputfile).

To use pyfragplotter, you need to have a config file and call the :func:`pyfrag_plotter.config.initialize_pyfrag_plotter` function. The config file should contain the necessary information about the PyFrag directories and the plot settings. The function reads the config file and sets up the necessary variables for making the plots. For an exanple of the config file, see :ref:`../../pyfrag_plotter/config.ini`.

Here's an example of how to use pyfrag_plotter:

.. code-block:: python

    from pyfragplotter import initialize_pyfrag_plotter, plot_pyfrag, plot_pyfrags

    initialize_pyfragplotter('config.ini')

    plot_pyfrag('pyfrag_1')

    plot_pyfrags(['pyfrag_1', 'pyfrag_2', 'pyfrag_3'])

In this example, we first call :func:`pyfrag_plotter.config.initialize_pyfrag_plotter` function with the path to the config file. This sets up the necessary variables for making the plots. We then call the plot_pyfrag function with the ID of the PyFrag directory we want to plot. This function reads the .txt and .in files from the PyFrag directory, extracts the necessary data, and makes the plot according to the settings specified in the config file.

Note that you can customize the plot settings in the config file, such as the plot type, color scheme, and axis labels. You can also plot multiple PyFrag directories at once by calling the plot_pyfrags function with a list of PyFrag IDs.
