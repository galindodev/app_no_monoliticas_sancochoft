from dataclasses import dataclass

from pagos.modulos.pagos.aplicacion.mapeadores import MapeadorPago
from pagos.modulos.pagos.dominio.fabricas import FabricaPagos
from pagos.modulos.pagos.dominio.objetos_valor import EstadoPago
from pagos.seedwork.aplicacion.queries import ejecutar_query as query

from pagos.modulos.pagos.dominio.repositorios import RepositorioPagos
from pagos.modulos.pagos.infraestructura.fabricas import FabricaRepositorio
from pagos.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado


@dataclass
class ObtenerPagosPendientes(Query):
    pass


class ObtenerPagosPendientesHandler(QueryHandler):
    def __init__(self):
        fabrica_repositorio = FabricaRepositorio()
        self.repositorio: RepositorioPagos = fabrica_repositorio.crear_objeto(RepositorioPagos.__class__)
        self.fabrica_pagos = FabricaPagos()

    def handle(self, _: ObtenerPagosPendientes) -> QueryResultado:
        pendientes = self.repositorio.obtener_todos(estado=EstadoPago.CREADO)
        dtos = self.fabrica_pagos.create_muchos_objetos(pendientes, MapeadorPago())
        return QueryResultado(resultado=dtos)


@query.register(ObtenerPagosPendientes)
def ejecutar_query_obtener_pagos_pendientes(query: ObtenerPagosPendientes):
    handler = ObtenerPagosPendientesHandler()
    return handler.handle(query)
