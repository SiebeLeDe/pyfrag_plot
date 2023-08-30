import pandas as pd


def read_data(datafile: str) -> pd.DataFrame:
    """
    A function to read the pyfrag output file (with ".txt" extension) and return a pandas dataframe.

    Args:
        datafile (str): The path to the datafile.

    Returns:
        pd.DataFrame: A pandas dataframe containing the data with #IRC steps as index.
    """
    df = pd.read_csv(datafile, header=0, delim_whitespace=True, dtype=float, index_col=0)

    # if there is only one bondlength, rename it to bondlength_1
    if 'bondlength' in df.columns and not any(col.startswith('bondlength_') for col in df.columns):
        df = df.rename(columns={'bondlength': 'bondlength_1'})

    if 'angle' in df.columns and not any(col.startswith('angle_') for col in df.columns):
        df = df.rename(columns={'angle': 'angle_1'})

    if 'dihedral' in df.columns and not any(col.startswith('dihedral_') for col in df.columns):
        df = df.rename(columns={'dihedral': 'dihedral_1'})

    return df
