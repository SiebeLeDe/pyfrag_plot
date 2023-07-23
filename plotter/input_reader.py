from os.path import join as opj
from typing import Any, Callable, Optional, List, Dict, Tuple
from plotter.file_func import get_pyfrag_files
import re


def _extract_pyfrag_section(filename: str) -> List[str]:
    with open(filename, "r") as f:
        lines = f.readlines()

    start_index = -1
    end_index = -1

    for i, line in enumerate(lines):
        if re.match(r"^\s*PyFrag\s*$", line, re.IGNORECASE):
            start_index = i+1
        if re.match(r"^\s*PyFrag END\s*$", line, re.IGNORECASE):
            end_index = i-1
            break

    if any(index == -1 for index in (start_index, end_index)):
        raise ValueError("Could not find PyFrag section in file. Check if the lines 'PyFrag' and 'PyFrag END' are present in the file.")

    return lines[start_index:end_index+1]


def _read_bondlength_line(line: str) -> Tuple[int, int, Optional[float]]:
    line_content = line.split()

    if len(line_content) < 3 or len(line_content) > 4:
        raise ValueError("Bondlength is not valid. Make sure to specify two atom (integer) and optionally a bondlength")

    # Bondlength has not been specified
    if len(line_content) == 3:
        atom1, atom2 = line_content[1:]
        return int(atom1), int(atom2), None

    # Bondlength has been specified
    atom1, atom2, bondlength = line_content[1:]
    return int(atom1), int(atom2), float(bondlength)


def _read_angle_line(line: str):
    line_content = line.split()

    if len(line_content) < 3 or len(line_content) > 5:
        raise ValueError("Angle is not valid. Make sure to specify two atom to three atoms (integers) and optionally an angle")

    # Bondlength has not been specified
    if len(line_content) == 3:
        atom1, atom2 = line_content[1:]
        return int(atom1), int(atom2), None

    # Bondlength has been specified
    atom1, atom2, bondlength = line_content[1:]
    return int(atom1), int(atom2), float(bondlength)


def _read_overlap_line(line: str):
    raise NotImplementedError


def _read_population_line(line: str):
    raise NotImplementedError


def _read_orbitalenergy_line(line: str):
    raise NotImplementedError


def _read_vdd_line(line: str) -> Tuple[float, int, int]:
    raise NotImplementedError


def _read_irrep_line(line: str) -> str:
    raise NotImplementedError


read_functions: Dict[str, Callable] = {
    "bondlength": _read_bondlength_line,
    "angle": _read_angle_line,
    "overlap": _read_overlap_line,
    "population": _read_population_line,
    "orbitalenergy": _read_orbitalenergy_line,
    "vdd": _read_vdd_line,
    "irrep": _read_irrep_line,
}


def read_inputfile(inputfile: str, name: str) -> Dict[str, Any]:
    """
    Takes as argument the inputfile for the pyfrag calculation
    Extracts extra specifications such as orbitalenergy, overlap, population of a certain fragment and MO
    """
    input_keys: Dict[str, Any] = {}

    pyfrag_section: List[str] = _extract_pyfrag_section(inputfile)

    counter = {key: 0 for key in read_functions}
    for line in pyfrag_section:
        for key, func in read_functions.items():
            if key.lower() in line.lower():
                counter[key] += 1
                input_keys[f"{key}_{counter[key]}"] = func(line)

    return input_keys


# def read_data(datafile: str):
#     """
#     Creates a dictionary with with the keys specifying which data it represents (EDA term, energy, etc.)
#     Takes as argument the absolute path to the pyfrag output file
#     """
#     header = np.genfromtxt(datafile, max_rows=1, dtype=str, comments=None)  # type: ignore
#     steps = np.genfromtxt(datafile, usecols=[0], dtype=int)
#     data = np.genfromtxt(datafile, usecols=range(1, len(header)), dtype=float)

#     data = remove_outliers(data)

#     # Processes the data
#     datadic = {}
#     specialkeys = {}
#     datadic[header[0][1:]] = steps
#     for i, key in enumerate(header[1:]):
#         # Replaces uninformative headers like 'orbitalenergy_1' with for example 'orbitalenergy_A_CGeP_33'
#         if key in special_keys.keys():
#             new_key = f'{key[:-1]}{"_".join(special_keys[key])}'
#             datadic[new_key] = data[: max_steps + 1, i]
#             # Keeps track which keys are changed
#             if key[:3] not in specialkeys:
#                 specialkeys[key[:3]] = []
#                 specialkeys[key[:3]].append(new_key)
#             else:
#                 specialkeys[key[:3]].append(new_key)
#         else:
#             datadic[key] = data[: max_steps + 1, i]
#     # Makes a dictionary with the results at the peak (maximum of total energy/bond energy)
#     peakdic = {}
#     peakstep = determine_stationary_point(datadic["EnergyTotal"])
#     for key, array in datadic.items():
#         peakdic[key] = array[peakstep]

#     # for key,value in specialkeys.items():
#     #    print(key, value)

#     # for key,value in peakdic.items():
#     #    print(key, value)

def main():
    path_to_pyfrag_results = r"C:\Users\siebb\VU_PhD\PhD\Projects\Squaramides\pyfrag_results"
    system_name = "deltamides_di_O_Cs_all"

    pyfrag_result_files = get_pyfrag_files(opj(path_to_pyfrag_results, system_name))
    for pyfrag_input_file, pyfrag_txt_file in pyfrag_result_files:
        name = pyfrag_input_file.split("\\")[-1].split(".")[0]
        inp = read_inputfile(pyfrag_input_file, name)
        print(inp)


if __name__ == "__main__":
    main()
