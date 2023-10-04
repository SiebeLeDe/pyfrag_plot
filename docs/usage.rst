.. _Usage:

Usage
======

pyfrag_plotter is a Python package that can be used to make plots from PyFrag directories containing the .txt (resultsfile) and .in file (inputfile).

To use pyfragplotter, you need to have a config file and call the |init| function. The config file should contain the necessary information about the PyFrag directories and the plot settings. The function reads the config file and sets up the necessary variables for making the plots. For an exanple of the config file, see :ref:`../../pyfrag_plotter/config.ini`.

Here's an example of how to use pyfrag_plotter:

.. code-block:: python

    from pyfrag_plotter.config import initialize_pyfrag_plotter

    initialize_pyfrag_plotter('path_to_config_file')

Creating the PyFragResultsObject
================================

In this example, we first call |init| function with the path to the config file. This sets up the necessary variables for making the plots. We then create a PyFragResultsObject by specifying a directory containing the input (.in) and results (.txt) file. This function reads the .txt and .in files from the directory, processes the data such as triming, removing outliers, removing dispersion term, and more. The resulting object can now be used to generate plots. 

Note that you can customize the plot settings in the config file, such as the plot type, color scheme, and axis labels.

Generating Plots
================

Using the PyFragResultsObject, plots can be made. For this, the Plotter class is initialized through passing PyFragResultsObjects. Now plots can be made by calling plot.asm method for instance. 
