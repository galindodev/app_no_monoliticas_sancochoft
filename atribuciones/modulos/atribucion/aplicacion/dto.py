from dataclasses import dataclass, field
from atribuciones.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class AtribucionDTO(DTO):
    estado: str = field(default_factory=str)
    evento: str = field(default_factory=str)
    monto: float = field(default_factory=float)
    moneda: str = field(default_factory=str)


@dataclass(frozen=True)
class ProgramaAtribucionDTO(DTO):
    id_programa: str = field(default_factory=str)
    atribuciones: list[AtribucionDTO] = field(default_factory=list)


@dataclass(frozen=True)
class ProgramaAtribucionCompletadoDTO(DTO):
    id_programa: str = field(default_factory=str)
    id_socio: str = field(default_factory=str)
