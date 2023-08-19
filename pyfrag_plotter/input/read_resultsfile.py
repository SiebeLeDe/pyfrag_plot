import pandas as pd


def read_data(datafile: str) -> pd.DataFrame:
    """A simple function to read the pyfrag output file (with ".txt" extension)

    Args:
        datafile (str): path to the datafile

    Returns:
        pd.DataFrame: pandas dataframe containing the data with #IRC steps as index
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


def main():
    from pyfrag_plotter.helper_funcs import get_pyfrag_files
    from pyfrag_plotter.input.read_inputfile import read_inputfile

    path_to_pyfrag_calculation_folder = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Scripting/local_packages/pyfrag_plotter/example/CGeN_Ethy"
    inputfile, resultsfile = get_pyfrag_files(path_to_pyfrag_calculation_folder)[0]

    input_keys = read_inputfile(inputfile)
    [print(key, value) for key, value in input_keys.items()]
    results = read_data(resultsfile)
    print(results.head())


if __name__ == "__main__":
    main()
