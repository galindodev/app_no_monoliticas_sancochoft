from dataclasses import dataclass, field
from atribuciones.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class AtribucionDTO(DTO):
    estado: str = field(default_factory=str)
    evento: str = field(default_factory=str)
    monto: float = field(default_factory=float)
    moneda: str = field(default_factory=str)
