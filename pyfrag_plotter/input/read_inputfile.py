# from os.path import join as opj
import re
import os
from typing import Any, Callable, Dict, List, Sequence, Tuple, Union
from pyfrag_plotter.file_func import get_pyfrag_files

from pyfrag_plotter.errors import PyFragInputError


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


def _check_line_length(line: str, input_key: str, limits: Sequence[int]) -> List[str]:
    """Checks if the line has the correct length for reading the specified input key. Raises an error if the line does not have the correct length.
    Returns a list containing the values of the line.

    :param line: line containing the keyword and the values
    :type line: str
    :param input_key: keyword to be read
    :type input_key: str
    :param limits: limits of the length of the line such as (3, 4) for bondlength and angle
    :type limits: Sequence[int]
    :raises PyFragInputError: if the line does not have the correct length
    :return: list containing the values of the line
    :rtype: List[str]
    """
    line_content: list[str] = re.split(r"\s+", line.strip())

    if len(line_content) not in limits:
        raise PyFragInputError(f"Length of the {input_key} not correct. Make sure to specify the correct format", input_key)
    return line_content


def _read_bondlength_line(line: str) -> Tuple[int, int, float]:
    """Reads the line containing the "bondlength" keyword. Correct format is:

    bondlength atom1 atom2 [bondlength] (optional).

    :param line: line to be read with the bondlength keyword
    :type line: str
    :return: Tuple containing the atom indices and the bondlength
    :rtype: Tuple[int, int, float]
    """
    line_content: List[str] = _check_line_length(line, "bondlength", (3, 4))

    # Bondlength has not been specified
    if len(line_content) == 3:
        atom1, atom2 = line_content[1:]
        return int(atom1), int(atom2), 0.0

    # Bondlength has been specified
    atom1, atom2, bondlength = line_content[1:]
    return int(atom1), int(atom2), float(bondlength)


def _read_bondangle_line(line: str) -> Tuple[int, int, float]:
    """Reads the line containing the "angle" keyword. Correct format is:

    angle atom1 atom2 [angle] (optional).

    :param line: line to be read with the angle keyword
    :type line: str
    :return: Tuple containing the atom indices and the bond angle
    :rtype: Tuple[int, int, float]
    """
    line_content: List[str] = _check_line_length(line, "angle", (3, 4))

    # Two atoms without angle
    if len(line_content) == 3:
        atom1, atom2 = line_content[1:]
        return int(atom1), int(atom2), 0.0

    # Two atoms with angle
    atom1, atom2, angle = line_content[1:]
    return int(atom1), int(atom2), float(angle)


def _read_dihedral_angle(line: str) -> Tuple[int, int, int, float]:
    """Reads the line containing the "dihedral" keyword. Correct format is:

    dihedral atom1 atom2 atom3 [dihedral_angle] (optional)

    :param line: line to be read with the dihedral keyword
    :type line: str
    :return: Tuple containing the atom indices and the dihedral angle
    :rtype: Tuple[int, int, int, float]
    """
    line_content: List[str] = _check_line_length(line, "dihedral", (4, 5))

    # Three atoms without angle
    if len(line_content) == 4:
        atom1, atom2, atom3 = line_content[1:]
        return int(atom1), int(atom2), int(atom3), 0.0

    # Three atoms with angle
    atom1, atom2, atom3, dihedral_angle = line_content[1:]
    return int(atom1), int(atom2), int(atom3), float(dihedral_angle)


def _read_overlap_line(line: str) -> Union[Tuple[str, str, str, str, str, str], Tuple[str, str, str, str]]:
    """Reads the line containing the "overlap" keyword. Correct formats are:

    overlap frag1 HOMO frag2 LUMO
    overlap frag1 HOMO-1 frag2 LUMO+3
    overlap S frag1 5 AA frag2 4

    :param line: line to be read with the population keyword
    :type line: str
    :return: tuple containing the MOs specified by the fragment, MO, and irrep (optional)
    :rtype: Union[Tuple[str, str, str, str, str, str], Tuple[str, str, str, str]]
    """
    line_content: List[str] = _check_line_length(line, "overlap", (5, 7))

    # Two fragments, two MOs (HOMO/LUMO kind), no irreps
    if len(line_content) == 5:
        frag1, MO1, frag2, MO2 = line_content[1:5]
        # Check if the fragments are strings and are named frag1 and frag2
        assert frag1 == "frag1" and frag2 == "frag2"
        return str(frag1), str(MO1), str(frag2), str(MO2)

    irrep1, frag1, index1, irrep2, frag2, index2 = line_content[1:]
    return str(irrep1), str(frag1), str(index1), str(irrep2), str(frag2), str(index2)


def _read_population_line(line: str) -> Union[Tuple[str, str], Tuple[str, str, str]]:
    """Reads the line containing the "population" keyword. Correct formats are:

    population frag1 HOMO
    population frag2 HOMO-1
    population AA frag2 5

    :param line: line to be read with the population keyword
    :type line: str
    :return: tuple containign the fragment, MO, and irrep (optional)
    :rtype: Union[Tuple[str, str], Tuple[str, str, str]]
    """
    line_content: List[str] = _check_line_length(line, "population", (3, 4))

    # Two fragments, two MOs (HOMO/LUMO kind), no irreps
    if len(line_content) == 3:
        frag1, MO1,  = line_content[1:3]
        return str(frag1), str(MO1)

    irrep1, frag1, index1 = line_content[1:]
    return str(irrep1), str(frag1), str(index1)


def _read_orbitalenergy_line(line: str) -> Union[Tuple[str, str], Tuple[str, str, str]]:
    """Reads the line containing the "orbitalenergy" keyword. Correct formats are:

    orbitalenergy frag1 HOMO
    orbitalenergy frag1 HOMO-2
    orbitalenergy AA frag2 5

    :param line: line to be read with the orbitalenergy keyword
    :type line: str
    :return: tuple containign the fragment, MO, and irrep (optional)
    :rtype: Union[Tuple[str, str], Tuple[str, str, str]]
    """
    line_content: List[str] = _check_line_length(line, "orbitalenergy", (3, 4))

    # Two fragments, two MOs (HOMO/LUMO kind), no irreps
    if len(line_content) == 3:
        frag1, MO1,  = line_content[1:3]
        return str(frag1), str(MO1)

    irrep1, frag1, index1 = line_content[1:]
    return str(irrep1), str(frag1), str(index1)


def _read_vdd_line(line: str) -> List[int]:
    """Reads the line containing the "vdd" keyword. Correct formats are:

    vdd 1 2 3 4
    vdd 3 6 8

    :param line: line to be read with the vdd keyword
    :type line: str
    :raises PyFragInputError: when the entries (atom indices) are not integers
    :return: list containing the atom indices
    :rtype: list[int]
    """
    line_content: list[str] = line.split()

    try:
        all([int(atom_index) for atom_index in line_content[1:]])
    except ValueError:
        raise PyFragInputError("Make sure to specify the vdd charges with spaces in between the indices", "vdd")

    return [int(atom_index) for atom_index in line_content[1:]]


def _read_irrep_line(line: str) -> str:
    """Reads the line containing the "irrep" keyword. Correct formats are:

    irrepOI AA
    irrepOI E1:1

    :param line: line to be read with the vdd keyword
    :type line: str
    :return: str containing the irrep
    :rtype: str
    """
    line_content: List[str] = _check_line_length(line, "orbitalenergy", (2, 2))

    irrep = line_content[1]
    return irrep


read_functions: Dict[str, Callable] = {
    "bondlength": _read_bondlength_line,
    "angle": _read_bondangle_line,
    "dihedral": _read_dihedral_angle,
    "overlap": _read_overlap_line,
    "population": _read_population_line,
    "orbitalenergy": _read_orbitalenergy_line,
    "vdd": _read_vdd_line,
    "irrep": _read_irrep_line,
}


def read_inputfile(inputfile: str) -> Dict[str, Any]:
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

    # Remove "_1" suffix from the keys if there is only one entry (to match the resultsfile.txt)
    # Should not be necessary if the inputfile and resultsfile have matching formats
    new_input_keys = {}
    for key, value in input_keys.items():
        if "_1" in key and counter[key.split("_")[0]] == 1:
            new_key = key.split("_")[0]
            new_input_keys[new_key] = value
        else:
            new_input_keys[key] = value
    input_keys = new_input_keys

    # Add the name of the inputfile to the dictionary if it is not specified in the inputfile
    if "name" not in input_keys:
        input_keys["name"] = os.path.splitext(os.path.basename(inputfile))[0]

    return input_keys


def main():
    # path_to_pyfrag_results = r"C:\Users\siebb\VU_PhD\PhD\Scripting\local_packages\pyfrag_plotter\example\pyfrag_files"
    path_to_pyfrag_results = r"/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Scripting/local_packages/pyfrag_plotter/example/ureas_di_O_Cs_all"

    inp = get_pyfrag_files(path_to_pyfrag_results)
    for inputfile, txtfile in inp:
        processed_input = read_inputfile(inputfile)
        print(processed_input)


if __name__ == "__main__":
    main()
