"""Entidades del dominio de pagos

En este archivo usted encontrará las entidades del dominio de pagos

"""
import uuid
from __future__ import annotations
from dataclasses import dataclass, field

import alpespartners.modulos.vuelos.dominio.objetos_valor as ov
from alpespartners.modulos.vuelos.dominio.eventos import ReservaCreada, ReservaAprobada, ReservaCancelada, ReservaPagada
from alpespartners.seedwork.dominio.entidades import Locacion, AgregacionRaiz, Entidad


@dataclass
class Pago(AgregacionRaiz):
    id_influencer: uuid.UUID = field(hash=True, default=None)

    def crear_solicitud(self, reserva: Pago):
        self.id_influencer = reserva.id_influencer
        # TODO: agregar evento
