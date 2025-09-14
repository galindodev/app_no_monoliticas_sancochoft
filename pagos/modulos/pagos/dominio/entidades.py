"""Entidades del dominio de pagos

En este archivo usted encontrará las entidades del dominio de pagos
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field

from pagos.seedwork.dominio.entidades import AgregacionRaiz

from .eventos import PagoSolicitado, PagoPagado, PagoRechazado
from .objetos_valor import Monto, EstadoPago


@dataclass
class Pago(AgregacionRaiz):
    id_influencer: uuid.UUID = field(hash=True, default=None)
    monto: Monto = field(default_factory=Monto)
    estado: EstadoPago = field(default=None)
    id_programa: uuid.UUID = field(default=None)

    def solicitar(self, pago: Pago):
        self.id_influencer = pago.id_influencer
        self.monto = pago.monto
        self.estado = pago.estado

        evento = PagoSolicitado(id_pago=self.id, id_influencer=self.id_influencer, monto=self.monto.valor)
        self.agregar_evento(evento)

    def finalizar(self, pagado: bool):
        if pagado:
            self._pagar()
        else:
            self._rechazar()

    def _pagar(self):
        self.estado = EstadoPago.PAGADO
        evento = PagoPagado(id_pago=self.id, id_influencer=self.id_influencer, id_programa=self.id_programa)
        self.agregar_evento(evento)

    def _rechazar(self):
        self.estado = EstadoPago.RECHAZADO
        evento = PagoRechazado(id_pago=self.id, id_influencer=self.id_influencer, id_programa=self.id_programa)
        self.agregar_evento(evento)
