# Contains the pyfrag object (dataclass)
from attrs import define, field
from typing import Optional, Sequence, Annotated, Literal, TypeVar
import numpy as np
import numpy.typing as npt

# Type alias for 1D numpy array with variable length but with a fixed dtype (np.float64)
DType = TypeVar("DType", bound=np.generic)
Array1D = Annotated[npt.NDArray[DType], Literal[1]]


@define(slots=True)
class EDA:
    dEint: Array1D[np.float64]
    dVelstat: Array1D[np.float64]
    dEPauli: Array1D[np.float64]
    dEoi: Array1D[np.float64]
    dEdisp: Optional[Array1D[np.float64]]


@define(slots=True)
class ASM:
    dE: float
    dEint: float
    dEstrain: float


@define(slots=True)
class Overlap:
    frag1_orb: str
    frag1_irrep: Optional[str]
    frag2_orb: str
    frag2_irrep: Optional[str]


@define(slots=True)
class Population:
    orbital: float
    frag: int
    irrep: Optional[str]


@define(slots=True)
class OrbitalEnergy:
    orbital: float
    frag: int
    irrep: Optional[str]


@define(slots=True)
class VDD:
    charge: float
    atom1: int
    atom2: int


@define(slots=True)
class Irrep:
    energy: float
    irrep: str


@define(slots=True)
class PyFragResultsObject:
    """
    Dataclass containing all the data of *one* pyfrag calculation
    """
    name: str
    eda: EDA = field(init=False)
    asm: ASM = field(init=False)
    populations: Optional[Sequence[Population]] = None
    orb_energies: Optional[Sequence[OrbitalEnergy]] = None
    populations: Optional[Sequence[Population]] = None
    vdd: Optional[Sequence[VDD]] = None
    irrep: Optional[Sequence[Irrep]] = None
