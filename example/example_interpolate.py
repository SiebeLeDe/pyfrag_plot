from pathlib import Path

import pandas as pd

from pyfrag_plotter import initialize_pyfrag_plotter
from pyfrag_plotter.interpolate import interpolate_data
from pyfrag_plotter.pyfrag_object import create_pyfrag_object_from_dir

# ------- User Input -------

# Specify variables and parameters such as the current directory, the directory containing the pyfrag results, the directory to save the plots to, and the config file.
current_dir_path = Path(__file__).resolve().parent
pyfrag_dir = current_dir_path
interpolate_dir = current_dir_path / "interpolated_data"
config_file = current_dir_path / "example_config.ini"

# Specify the directories (that are in the pyfrag_dir) containing the pyfrag results
result_dirs = ["ureas_di_O_Cs_all", "ureas_di_O_Cs_pi", "ureas_di_O_Cs_sigma"]

# Create the full paths to the directories containing the pyfrag results
pyfrag_dirs = [pyfrag_dir / directory for directory in result_dirs]

# ------- Running the script -------

# First, initialize the config file
initialize_pyfrag_plotter(user_config_file=str(config_file))

# Create the pyfrag objects. These objects contain all the information about the pyfrag results.
objs = [create_pyfrag_object_from_dir(str(pyfrag_dir)) for pyfrag_dir in pyfrag_dirs]

# Create an empty DataFrame
dfs = []

# Interpolate objects and append data to the DataFrame
for obj in objs:
    data = interpolate_data(obj, "bondlength_1", 0.29)
    data.insert(0, "Name", obj.name)
    dfs.append(data)

df = pd.concat(dfs)
df.set_index("Name", inplace=True)

# Print the DataFrame
print(df)
