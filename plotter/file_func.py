import os


def get_pyfrag_files(folder_path: str):
    pyfrag_files: list[tuple[str, str]] = []
    for root, _, files in os.walk(folder_path):
        # print(files)
        if root.count(os.sep) - folder_path.count(os.sep) > 2:
            # Only search up to two levels deep
            continue

        pyfrag_input_file = ""
        pyfrag_txt_file = ""
        for file in files:
            if file.endswith('.in'):
                pyfrag_input_file = os.path.join(root, file)
                print(pyfrag_input_file)
            if file.startswith('pyfrag') and file.endswith('.txt'):
                pyfrag_txt_file = os.path.join(root, file)
                print(pyfrag_txt_file)

        # Check if both files were found
        if not (pyfrag_input_file and pyfrag_txt_file):
            raise FileNotFoundError(f"Could not find pyfrag input file or pyfrag txt file in {root}")

        # Add the files to the list as a tuple
        pyfrag_files.append((pyfrag_input_file, pyfrag_txt_file))

    return pyfrag_files
