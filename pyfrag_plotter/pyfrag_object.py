""" Module that combines the data from inputfile and outputfile into a PyFragResultsObject object """
from typing import Annotated, Any, Dict, Literal, Optional, TypeVar, Callable, List, Tuple
from pyfrag_plotter.errors import PyFragResultsObjectError
from pyfrag_plotter.config_handler import config
import numpy as np
import numpy.typing as npt
import pandas as pd
from attrs import define, field
from collections import OrderedDict

# Type alias for 1D numpy array with variable length but with a fixed dtype (np.float64)
DType = TypeVar("DType", bound=np.generic)
Array1D = Annotated[npt.NDArray[DType], Literal[1]]


@define(slots=True)
class Bondlength:
    atom1: int
    atom2: int
    bondlength: float
    data: Array1D[np.float64]


@define(slots=True)
class BondAngle:
    atom1: int
    atom2: int
    bondangle: float
    data: Array1D[np.float64]


@define(slots=True)
class DihedralAngle:
    atom1: int
    atom2: int
    atom3: int
    dihedralangle: float
    data: Array1D[np.float64]


@define(slots=True)
class Overlap:
    frag1_orb: str
    frag2_orb: str
    data: Array1D[np.float64]
    frag1_irrep: Optional[str] = None
    frag2_irrep: Optional[str] = None


@define(slots=True)
class Population:
    orbital: float
    frag: int
    data: Array1D[np.float64]
    irrep: Optional[str] = None


@define(slots=True)
class OrbitalEnergy:
    orbital: float
    frag: int
    data: Array1D[np.float64]
    irrep: Optional[str] = None


@define(slots=True)
class VDD:
    atom: int
    data: Array1D[np.float64]


@define(slots=True)
class Irrep:
    irrep: str
    data: Array1D[np.float64]


@define(slots=True)
class PyFragResultsObject:
    """
    Dataclass containing all the data of *one* pyfrag calculation
    """
    name: str
    eda: OrderedDict[str, Array1D[np.float64]] = field(factory=dict)
    asm: OrderedDict[str, Array1D[np.float64]] = field(factory=dict)
    extra_strain: OrderedDict[str, Array1D[np.float64]] = field(factory=dict)
    bondlength: List[Bondlength] = field(factory=list)
    angle: List[BondAngle] = field(factory=list)
    dihedral: List[DihedralAngle] = field(factory=list)
    overlap: List[Overlap] = field(factory=list)
    population: List[Population] = field(factory=list)
    orbitalenergy: List[OrbitalEnergy] = field(factory=list)
    vdd: List[VDD] = field(factory=list)
    irrep: List[Irrep] = field(factory=list)

    def get_x_axis(self, irc_coord: str) -> Array1D[np.float64]:
        """ Returns the x-axis data for the specified IRC coordinate."""
        try:
            irc_coord, index = irc_coord.split("_")
        except ValueError:
            index = 1
        return self.__getattribute__(irc_coord)[int(index)-1].data

    def get_peak_of_key(self, key: str, peak: str = "max") -> Tuple[int, float]:
        """ Returns the index and corresponding peak value of the specified key. The peak can be either the maximum or minimum value. """
        if key in ["bondlength", "angle", "dihedral", "overlap", "population", "orbitalenergy", "vdd", "irrep"]:
            try:
                key, index = key.split("_")
                data: Array1D[np.float64] = self.__getattribute__(key)[int(index)-1].data
            except ValueError:
                data: Array1D[np.float64] = self.__getattribute__(key)[1].data
        elif key in {**self.eda, **self.asm, **self.extra_strain}.keys():
            merged_dicts = {**self.eda, **self.asm, **self.extra_strain}
            data = merged_dicts[key]
        else:
            raise PyFragResultsObjectError(f"Key '{key}' not found in any attribute of PyFragResultsObject")

        if peak == "max":
            return int(data.argmax()), data.max()
        return int(data.argmin()), data.min()


def _add_bondlength(obj: PyFragResultsObject, data: Array1D[np.float64], *bond_info) -> None:
    bondlength_obj = Bondlength(atom1=bond_info[0], atom2=bond_info[1], bondlength=bond_info[2], data=data)
    obj.bondlength.append(bondlength_obj)


def _add_bondangle(obj: PyFragResultsObject, data: Array1D[np.float64], *bondangle_info) -> None:
    bondangle_obj = BondAngle(atom1=bondangle_info[0], atom2=bondangle_info[1], bondangle=bondangle_info[2], data=data)
    obj.angle.append(bondangle_obj)


def _add_dihedralangle(obj: PyFragResultsObject, data: Array1D[np.float64], *dihedralangle_info) -> None:
    dihedral_obj = DihedralAngle(atom1=dihedralangle_info[0],
                                 atom2=dihedralangle_info[1],
                                 atom3=dihedralangle_info[2],
                                 dihedralangle=dihedralangle_info[3], data=data)
    obj.dihedral.append(dihedral_obj)


def _add_overlap(obj: PyFragResultsObject, data: Array1D[np.float64], *overlap_info) -> None:
    """ Adds an Overlap object to the PyFragResultsObject object. Two possible formats:
    1. frag1 HOMO frag2 LUMO
    1. S frag1 5 AA frag2 4

    Args:
        obj (PyFragResultsObject): instance to which the overlap is appended to
        data (Array1D[np.float64]): the results from the PyFrag calculation along the IRC path for this overlap key
        overlap_info: frag1 and frag2 with the orbital index and optionally the irrep.

    Returns:
        None
    """
    if len(overlap_info) == 4:
        overlap_obj = Overlap(frag1_orb=overlap_info[1],
                              frag2_orb=overlap_info[3],
                              data=data)

    else:
        overlap_obj = Overlap(frag1_irrep=overlap_info[0],
                              frag1_orb=overlap_info[2],
                              frag2_irrep=overlap_info[3],
                              frag2_orb=overlap_info[5],
                              data=data)
    obj.overlap.append(overlap_obj)
    return


def _add_population(obj: PyFragResultsObject, data: Array1D[np.float64], *population_info):
    """ Adds an Population object to the PyFragResultsObject object. Two possible formats:
    1. frag1 HOMO
    1. S frag1 5

    Args:
        obj (PyFragResultsObject): instance to which the population is appended to
        data (Array1D[np.float64]): the results from the PyFrag calculation along the IRC path for this population key
        population_info: frag1 and frag2 with the orbital index and optionally the irrep.

    Returns:
        None
    """
    if len(population_info) == 2:
        pop_obj = Population(frag=population_info[0], orbital=population_info[1], data=data)
    else:
        pop_obj = Population(frag=population_info[1],
                             orbital=population_info[0],
                             irrep=population_info[2],
                             data=data)
    obj.population.append(pop_obj)
    return


def _add_orbitalenergy(obj: PyFragResultsObject, data: Array1D[np.float64], *orbenergy_info):
    """ Adds an OrbitalEnergy object to the PyFragResultsObject object. Two possible formats:
    1. frag1 HOMO
    1. S frag1 5

    Args:
        obj (PyFragResultsObject): instance to which the population is appended to
        data (Array1D[np.float64]): the results from the PyFrag calculation along the IRC path for this orbitalenergy key
        orbenergy_info: frag1 and frag2 with the orbital index and optionally the irrep.

    Returns:
        None
    """
    if len(orbenergy_info) == 2:
        orb_energy_obj = OrbitalEnergy(frag=orbenergy_info[0], orbital=orbenergy_info[1], data=data)
    else:
        orb_energy_obj = OrbitalEnergy(frag=orbenergy_info[1],
                                       orbital=orbenergy_info[0],
                                       irrep=orbenergy_info[2],
                                       data=data)
    obj.orbitalenergy.append(orb_energy_obj)
    return


def _add_vdd(obj: PyFragResultsObject, data: Array1D[np.float64], vdd_index: str):
    """ Adds an OrbitalEnergy object to the PyFragResultsObject object.

    Args:
        obj (PyFragResultsObject): instance to which the population is appended to
        data (Array1D[np.float64]): the results from the PyFrag calculation along the IRC path for this vdd key
        vdd_index: the atom index to which the VDD data belongs to

    Returns:
        None
    """
    vdd_obj = VDD(atom=int(vdd_index), data=data)
    obj.vdd.append(vdd_obj)
    return


def _add_irrep(obj: PyFragResultsObject, data: Array1D[np.float64], irrep: str):
    """ Adds an OrbitalEnergy object to the PyFragResultsObject object.

    Args:
        obj (PyFragResultsObject): instance to which the population is appended to
        data (Array1D[np.float64]): the results from the PyFrag calculation along the IRC path for this vdd key
        vdd_index: the atom index to which the VDD data belongs to

    Returns:
        None
    """
    irrep_obj = Irrep(irrep=irrep, data=data)
    obj.irrep.append(irrep_obj)
    return


key_to_func_mapping: dict[str, Callable[..., None]] = {
    "bondlength": _add_bondlength,
    "angle": _add_bondangle,
    "dihedral": _add_dihedralangle,
    "overlap": _add_overlap,
    "population": _add_population,
    "orbitalenergy": _add_orbitalenergy,
    "vdd": _add_vdd,
    "irrep": _add_irrep,
}


def create_pyfrag_object(results_data: pd.DataFrame, inputfile_data: Dict[str, Any]) -> PyFragResultsObject:
    """_summary_

    Args:
        results_data (pd.DataFrame): the data from the output file (i.e., the pyfrag_*.txt file)
        inputfile_data (Dict[str, Any]): the keys from the input file such as bondlength, overlap, orbitalenergy, and more

    Returns:
        PyFragResultsObject: the dataclass containing all the data of *one* pyfrag calculation
    """
    obj = PyFragResultsObject(inputfile_data.pop("name"))

    # The EDA , ASM, and ExtraStrain are always present in the output file
    for key in config["config"].get("EDA", "EDA_keys"):
        if key not in results_data:
            continue
        obj.eda[key] = results_data[key].to_numpy()

    for key in config["config"].get("ASM", "ASM_keys"):
        obj.asm[key] = results_data[key].to_numpy()

    for key in config["config"].get("ASM", "ASM_strain_keys"):
        obj.extra_strain[key] = results_data[key].to_numpy()

    for key, value in inputfile_data.items():
        data = results_data[key].to_numpy()

        try:
            key = key.split("_")[0]
        except Exception:
            pass

        if key in key_to_func_mapping:
            key_to_func_mapping[key](obj, data, *value)

    return obj


def main():
    from pyfrag_plotter.config_handler import initialize_pyfrag_plotter
    initialize_pyfrag_plotter()

    from pyfrag_plotter.input.read_inputfile import read_inputfile
    from pyfrag_plotter.input.read_resultsfile import read_data
    from pyfrag_plotter.helper_funcs import get_pyfrag_files
    from pyfrag_plotter.processing_funcs import trim_data
    # Next, specify the path to the pyfrag output directory and read in the input file and the output file
    pyfrag_dir = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Scripting/local_packages/pyfrag_plotter/example/CGeN_Ethy"

    inputfile, results_file = get_pyfrag_files([pyfrag_dir])[0]

    # Read the input file
    input_content = read_inputfile(inputfile)

    # Read the output file
    output_content = read_data(results_file)
    output_content = trim_data(output_content)

    obj = create_pyfrag_object(output_content, input_content)
    print(obj)


if __name__ == "__main__":
    main()
