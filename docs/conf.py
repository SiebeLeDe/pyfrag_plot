# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'PyFragPlotter'
copyright = '2023, SiebeLeDe'
author = 'SiebeLeDe'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    'sphinx.ext.duration',
    "sphinx.ext.autosummary",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

modindex_common_prefix = ['pyfrag_plotter.']

html_theme_options = {
    "show_nav_level": 2,
    "navigation_depth": 2,
}


autodoc_default_options = {
    'show-inheritance': True,
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'pydata_sphinx_theme'


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Don't show the pyfrag_plotter module name in the documentation
add_module_names = True

# Replace function / class names with alias
rst_epilog = """
.. |init| replace:: :func:`pyfrag_plotter.initialize_pyfrag_plotter`
.. |validate| replace:: :func:`pyfrag_plotter.config_handler.validate_config`
.. |get| replace:: :func:`pyfrag_plotter.config_handler.get_config`
.. |process| replace:: :func:`pyfrag_plotter.processing_funcs.process_results_file`
.. |ax_details| replace:: :func:`pyfrag_plotter.plot.plot_details.set_axes_details`
.. |fig_details| replace:: :func:`pyfrag_plotter.plot.plot_details.set_figure_details`
.. |pyfrag_obj| replace:: :class:`pyfrag_plotter.pyfrag_object.PyFragResultsObject`
.. |obj_from_dir| replace:: :func:`pyfrag_plotter.pyfrag_object.create_pyfrag_object_from_dir`
"""
