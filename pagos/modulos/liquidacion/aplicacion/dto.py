from dataclasses import dataclass, field
from pagos.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class LiquidacionDTO(DTO):
    id_pago: str = field(default_factory=str)
    id_influencer: str = field(default_factory=str)
    monto: float = field(default_factory=float)
