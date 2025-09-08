""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from uuid import UUID

from alpespartners.config.db import db

from alpespartners.modulos.pagos.dominio.entidades import Pago
from alpespartners.modulos.pagos.dominio.objetos_valor import EstadoPago
from alpespartners.modulos.pagos.dominio.repositorios import RepositorioPagos
from alpespartners.modulos.pagos.dominio.fabricas import FabricaPagos

from .mapeadores import MapeadorPago
from .dto import Pago as PagoDTO


class RepositorioReservasSQLAlchemy(RepositorioPagos):
    def __init__(self):
        self.fabrica_pagos: FabricaPagos = FabricaPagos()

    def obtener_por_id(self, id: UUID) -> Pago:
        result = db.session.query(PagoDTO).filter_by(id=str(id)).one()
        return self.fabrica_pagos.crear_objeto(result, MapeadorPago())

    def obtener_todos(self, estado: EstadoPago) -> list[Pago]:
        results = db.session.query(PagoDTO).filter_by(estado=estado).all()
        return self.fabrica_pagos.create_muchos_objetos(results, MapeadorPago())

    def agregar(self, pago: Pago):
        pago_dto = self.fabrica_pagos.crear_objeto(pago, MapeadorPago())
        db.session.add(pago_dto)

    def actualizar(self, pago: Pago):
        pago_dto: PagoDTO = self.fabrica_pagos.crear_objeto(pago, MapeadorPago())
        db.session.merge(pago_dto)

    def eliminar(self, reserva_id: UUID):
        raise NotImplementedError
