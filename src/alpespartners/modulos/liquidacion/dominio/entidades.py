"""Entidades del dominio de liquidacion

En este archivo usted encontrará las entidades del dominio de liquidacion
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field

from alpespartners.seedwork.dominio.entidades import AgregacionRaiz

from .objetos_valor import Monto
from .eventos import LiquidacionFinalizada


@dataclass
class Liquidacion(AgregacionRaiz):
    id_pago: uuid.UUID = field(hash=True, default=None)
    id_influencer: uuid.UUID = field(hash=True, default=None)
    monto: Monto = field(default_factory=Monto)

    def liquidar_pago(self, liquidacion: Liquidacion):
        self.id_pago = liquidacion.id_pago
        self.id_influencer = liquidacion.id_influencer
        self.monto = liquidacion.monto

        evento = LiquidacionFinalizada(id_pago=self.id_pago, id_liquidacion=self.id, pagado=True)
        self.agregar_evento(evento)
