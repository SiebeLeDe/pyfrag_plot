""" Module that contains the functions for initializing the config file and reading the config file. This module should be imported by any module that needs to read the config file. """
from __future__ import annotations
import os
import re
import configparser as cp
from typing import Optional, Dict, Callable, Any, List

# Global variable that contains the config file
config: Config = {}  # type: ignore because Config is not defined yet, but will be defined in the initialize_pyfrag_plotter function


def _get_str_key(config_parser: cp.ConfigParser, section: str, option: str) -> str:
    value = config_parser.get(section, option)
    return value.strip()


def _get_list_str_key(config_parser: cp.ConfigParser, section: str, option: str) -> List[str]:
    # Split the value string using a regular expression that matches any whitespace character
    value = re.split(r'\s*,\s*|\s+', config_parser.get(section, option))
    return [v for v in value if v]


def _get_float_key(config_parser: cp.ConfigParser, section: str, option: str) -> float:
    value = config_parser.getfloat(section, option)
    return value


def _get_list_float_key(config_parser: cp.ConfigParser, section: str, option: str) -> List[float]:
    value = re.split(r'\s*,\s*|\s+', config_parser.get(section, option))
    value = [float(v.strip()) for v in value]
    return value


def _get_int_key(config_parser: cp.ConfigParser, section: str, option: str) -> int:
    value = config_parser.getint(section, option)
    return value


def _get_boolean_key(config_parser: cp.ConfigParser, section: str, option: str) -> bool:
    value = config_parser.getboolean(section, option)
    return value


def _get_any_key(config_parser: cp.ConfigParser, section: str, option: str) -> Any:
    # First, try to get the value as an integer
    try:
        value = config_parser.getint(section, option)
    except ValueError:
        # If that fails, try to get the value as a float
        try:
            value = config_parser.getfloat(section, option)
        except Exception:
            # If that fails, get the value as a string
            value = config_parser.get(section, option)
            value = value.strip()
    return value


key_to_function_mapping: Dict[str, Callable[..., Any]] = {
    # Shared keys
    "x_lim": _get_list_float_key,
    "y_lim": _get_list_float_key,
    "colours": _get_list_str_key,
    "line_styles": _get_list_str_key,
    "outlier_threshold": _get_float_key,
    "plot_until": _get_any_key,
    "vline": _get_float_key,
    "trim_key": _get_str_key,
    "reverse_x_axis": _get_boolean_key,
    "stat_point_type": _get_str_key,

    # EDA keys
    "EDA_keys": _get_list_str_key,

    # ASM keys
    "ASM_keys": _get_list_str_key,
    "ASM_strain_keys": _get_list_str_key,

    # Matplotlib keys
    "fig_size": _get_list_float_key,
    "font": _get_str_key,
    "font_size": _get_int_key,
}


def get_config() -> Config:
    """ Returns the initiated config instance. """
    if config is None:
        raise ValueError("Config file has not been initialized. Please call initialize_pyfrag_plotter first.")
    return config


class Config:
    """ Interface for the config file. This class overloads the get method of the ConfigParses class to ensure that the correct type is returned. """

    def __init__(self, config_parser) -> None:
        self.config_parser: cp.ConfigParser = config_parser

    def get(self, section: str, option: str) -> Any:
        """ IMPORTANT: only this method should be called when trying to get values from the config instance.
        Returns the value of the option in the section.
        It returns the value with the correct type.

        """
        if option not in key_to_function_mapping:
            raise ValueError(f"Option '{option}' is not a valid option. Valid options are {list(key_to_function_mapping.keys())}.\nPlease check the config file.")

        if section not in self.config_parser:
            raise ValueError(f"Section '{section}' is not a valid section. Note that sections are case sensitive.")

        return key_to_function_mapping[option](self.config_parser, section, option)

    def sections(self) -> List[str]:
        """ Returns a list of the sections in the config file. """
        return self.config_parser.sections()


def initialize_pyfrag_plotter(user_config_file: Optional[str] = None) -> None:
    """
    Initializes the config file. Reads the standard config file provided in the module.
    May be overwritten by providing a config file.
    """
    # Get the absolute path of the directory one level above the current directory
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Construct the path to the configuration file
    config_file = os.path.join(current_dir, 'config.ini')

    # Read the config file
    config_parser = cp.ConfigParser()
    config_parser.read(config_file)

    # Read the user config file if provided and overwrite the config file
    if user_config_file is not None:
        config_parser.read(user_config_file)

    config = Config(config_parser)
    _initialize_plot_parameters()


def _initialize_plot_parameters() -> None:
    """
    Applies plot-specific parameters to matplotlib.
    """
    import matplotlib.pyplot as plt
    # mpl.use("Agg")

    # Get a list of available fonts of matplotlib
    # import matplotlib.font_manager
    # flist = matplotlib.font_manager.get_fontconfig_fonts()
    # names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist]
    # print(names)

    # mp.font_manager._rebuild()
    # font = fp.FontProperties(fname=r"C:\\Windows\\Fonts\\Helvetica Regulier.ttf")
    # print(font.get_name())

    # Figure size
    plt.rcParams["figure.figsize"] = config.get("MATPLOTLIB", "fig_size")

    # Font family
    plt.rcParams["font.family"] = config.get("MATPLOTLIB", "font")

    # Takes care of ticks starting at the edge of the screen
    plt.rcParams["axes.autolimit_mode"] = "round_numbers"
    plt.rcParams["axes.xmargin"] = 0.00
    plt.rcParams["axes.ymargin"] = 0.00

    font_size = config.get("MATPLOTLIB", "font_size")

    plt.rc("font", size=font_size)  # controls default text sizes
    plt.rc("axes", titlesize=font_size + 4)  # fontsize of the axes title
    plt.rc("axes", labelsize=font_size + 4)  # fontsize of the x and y labels
    plt.rc("xtick", labelsize=font_size)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=font_size)  # fontsize of the tick labels
    plt.rc("legend", fontsize=font_size - 4)  # legend fontsize
    plt.rc("figure", titlesize=font_size - 4)  # fontsize of the figure title


def main():
    path_to_extra_config = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Scripting/testing/extra_config.ini"
    initialize_pyfrag_plotter(path_to_extra_config)

    # eda = config.get("EDA", "EDA_keys")
    interpol = config.get("SHARED", "interpolation_method")  # type: ignore
    print(interpol)


if __name__ == "__main__":
    main()
