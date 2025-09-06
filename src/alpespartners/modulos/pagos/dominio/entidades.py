"""Entidades del dominio de pagos

En este archivo usted encontrará las entidades del dominio de pagos
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field

from alpespartners.seedwork.dominio.entidades import AgregacionRaiz

from .eventos import PagoSolicitado
from .objetos_valor import Monto


@dataclass
class Pago(AgregacionRaiz):
    id_influencer: uuid.UUID = field(hash=True, default=None)
    monto: Monto = field(default_factory=Monto)

    def solicitar(self, pago: Pago):
        self.id_influencer = pago.id_influencer
        self.monto = pago.monto
        self.agregar_evento(PagoSolicitado(id_pago=self.id))
