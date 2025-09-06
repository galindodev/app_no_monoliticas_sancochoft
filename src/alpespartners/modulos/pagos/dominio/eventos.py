from __future__ import annotations
import uuid
from dataclasses import dataclass


from alpespartners.seedwork.dominio.eventos import EventoDominio


@dataclass
class PagoSolicitado(EventoDominio):
    id_pago: uuid.UUID = None
    id_influencer: uuid.UUID = None
    monto: float = None
