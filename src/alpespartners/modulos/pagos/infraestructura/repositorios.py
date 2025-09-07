""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from uuid import UUID

from alpespartners.config.db import db

from alpespartners.modulos.pagos.dominio.entidades import Pago
from alpespartners.modulos.pagos.dominio.repositorios import RepositorioPagos
from alpespartners.modulos.pagos.dominio.fabricas import FabricaPagos

from .mapeadores import MapeadorPago


class RepositorioReservasSQLAlchemy(RepositorioPagos):
    def __init__(self):
        self.fabrica_pagos: FabricaPagos = FabricaPagos()

    def obtener_por_id(self, id: UUID) -> Pago:
        raise NotImplementedError

    def obtener_todos(self) -> list[Pago]:
        raise NotImplementedError

    def agregar(self, pago: Pago):
        pago_dto = self.fabrica_pagos.crear_objeto(pago, MapeadorPago())
        db.session.add(pago_dto)

    def actualizar(self, pago: Pago):
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        raise NotImplementedError
