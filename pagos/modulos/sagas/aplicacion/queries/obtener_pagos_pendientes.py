from dataclasses import dataclass

from pagos.seedwork.aplicacion.queries import ejecutar_query as query

from pagos.modulos.sagas.infraestructura.fabricas import FabricaRepositorio
from pagos.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado


@dataclass
class ObtenerTransaccionesPago(Query):
    id_correlacion: str


class ObtenerTransaccionesPagoHandler(QueryHandler):
    def __init__(self):
        self.repositorio = FabricaRepositorio().crear_objeto()

    def handle(self, query: ObtenerTransaccionesPago) -> QueryResultado:
        transacciones = self.repositorio.obtener_por_id(query.id_correlacion)
        resultado = [
            dict(
                id_correlacion=t.id_correlacion,
                nombre=t.nombre,
                tipo_mensaje=t.tipo_mensaje,
            )
            for t in transacciones
        ]
        return QueryResultado(resultado=resultado)


@query.register(ObtenerTransaccionesPago)
def ejecutar_query_obtener_transacciones_pago(query: ObtenerTransaccionesPago):
    handler = ObtenerTransaccionesPagoHandler()
    return handler.handle(query)
