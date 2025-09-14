from dataclasses import dataclass, field
from pagos.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class PagoDTO(DTO):
    id_influencer: str = field(default_factory=str)
    monto: float = field(default_factory=float)
    estado: str = field(default_factory=str)
    id_programa: str = field(default_factory=str)
