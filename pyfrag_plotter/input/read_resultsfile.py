import pandas as pd


def read_data(datafile: str) -> pd.DataFrame:
    """A simple function to read the pyfrag output file (with ".txt" extension)

    Args:
        datafile (str): path to the datafile

    Returns:
        pd.DataFrame: pandas dataframe containing the data with #IRC steps as index
    """
    df = pd.read_csv(datafile, header=0, delim_whitespace=True, dtype=float, index_col=0)
    return df


def main():
    from pyfrag_plotter.file_func import get_pyfrag_files
    from pyfrag_plotter.input.read_inputfile import read_inputfile

    path_to_pyfrag_calculation_folder = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Scripting/local_packages/pyfrag_plotter/example/CGeN_Ethy"
    inputfile, resultsfile = get_pyfrag_files(path_to_pyfrag_calculation_folder)[0]

    input_keys = read_inputfile(inputfile, "CGeN_Ethy")
    # [print(key, value) for key, value in input_keys.items()]
    results = read_data(resultsfile)
    print(results.head())


if __name__ == "__main__":
    main()
