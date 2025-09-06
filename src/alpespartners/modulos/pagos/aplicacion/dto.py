from dataclasses import dataclass, field
from alpespartners.seedwork.aplicacion.dto import DTO
from alpespartners.modulos.pagos.dominio.objetos_valor import EstadoPago

@dataclass(frozen=True)
class PagoDTO(DTO):
    id_influencer: str = field(default_factory=str)
    monto: float = field(default_factory=float)
    estado: str = field(default_factory=str)
