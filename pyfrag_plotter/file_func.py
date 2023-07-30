import os
from typing import List, Tuple, Union


def get_pyfrag_files(dirs: Union[list[str], str]) -> List[Tuple[str, str]]:
    """Searches for pyfrag input files and pyfrag txt files in the given folders and returns a list of tuples containing the absolute path to the pyfrag input file and the pyfrag txt file

    Args:
        *args (str): absolute paths to the folders containing the pyfrag input files

    Raises:
        FileNotFoundError: when the pyfrag input file or pyfrag txt file could not be found in the same folder
        FileNotFoundError: when the returned list is empty

    Returns:
        pyfrag_files (list of tuples(str, str)): list of tuples containing the absolute path to the pyfrag input file and the pyfrag txt file
    """
    if isinstance(dirs, str):
        dirs = [dirs]

    pyfrag_files: List[Tuple[str, str]] = []
    for folder_path in dirs:
        files = os.listdir(folder_path)

        # Search for pyfrag input file and pyfrag txt file
        pyfrag_input_file = ""
        pyfrag_txt_file = ""
        for file in files:
            if file.endswith('.in'):
                pyfrag_input_file = os.path.join(folder_path, file)
            if file.startswith('pyfrag') and file.endswith('.txt'):
                pyfrag_txt_file = os.path.join(folder_path, file)

        # Check if both files were found
        if not (pyfrag_input_file and pyfrag_txt_file):
            raise FileNotFoundError(f"Could not find pyfrag input file or pyfrag txt file in {folder_path}")

        # Add the files to the list as a tuple
        pyfrag_files.append((pyfrag_input_file, pyfrag_txt_file))

    if not pyfrag_files:
        raise FileNotFoundError(f"Could not find pyfrag input file or pyfrag txt file in {dirs}")

    return pyfrag_files
