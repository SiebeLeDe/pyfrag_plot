# Contains the pyfrag object (dataclass)
from attrs import define


@define(slots=True)
class EDATerms:
    dEint: float = 0.0


@define(slots=True)
class ASMTerms:
    dEint: float = 0.0


@define(slots=True)
class OverlapTerms:
    dEint: float = 0.0


@define(slots=True)
class PopulationTerms:
    dEint: float = 0.0


@define(slots=True)
class OrbitalEnergyTerms:
    dEint: float = 0.0


@define(slots=True)
class PyFragObject:
    eda: EDATerms = EDATerms()
    asm: ASMTerms = ASMTerms()
    overlaps: OverlapTerms = OverlapTerms()
    orb_energies = OrbitalEnergyTerms()
    populations = PopulationTerms()
