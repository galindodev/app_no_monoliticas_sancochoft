from __future__ import annotations
import uuid
from dataclasses import dataclass


from liquidaciones.seedwork.dominio.eventos import EventoDominio


@dataclass
class LiquidacionFinalizada(EventoDominio):
    id_pago: uuid.UUID = None
    id_liquidacion: uuid.UUID = None
    pagado: bool = None
