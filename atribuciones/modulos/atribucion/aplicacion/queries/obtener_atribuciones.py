from dataclasses import dataclass
from uuid import UUID

from atribuciones.modulos.atribucion.dominio.excepciones import ProgramaNoEncontradoExcepcion
from atribuciones.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado, ejecutar_query as query

from atribuciones.modulos.atribucion.dominio.entidades import ProgramaAtribucion
from atribuciones.modulos.atribucion.aplicacion.mapeadores import MapeadorProgramaAtribucion

from atribuciones.modulos.atribucion.dominio.fabricas import FabricaAtribucion
from atribuciones.modulos.atribucion.dominio.repositorios import RepositorioProgramaAtribucion
from atribuciones.modulos.atribucion.infraestructura.fabricas import ProgramaFabricaRepositorio


@dataclass
class ObtenerAtribuciones(Query):
    id_programa: str


class ObtenerAtribucionesHandler(QueryHandler):
    def __init__(self):
        self.fabrica_atribucion = FabricaAtribucion()
        self.fabrica_repositorio = ProgramaFabricaRepositorio()
        self.repositorio: RepositorioProgramaAtribucion = self.fabrica_repositorio.crear_objeto(ProgramaFabricaRepositorio.__class__)

    def handle(self, consulta: ObtenerAtribuciones):
        programa: ProgramaAtribucion = self.repositorio.obtener_por_id(UUID(consulta.id_programa))
        if not programa:
            raise ProgramaNoEncontradoExcepcion()
        programa_dto = self.fabrica_atribucion.crear_objeto(programa, MapeadorProgramaAtribucion())
        return QueryResultado(resultado=programa_dto)



@query.register(ObtenerAtribuciones)
def ejecutar_query_obtener_atribuciones(consulta: ObtenerAtribuciones):
    handler = ObtenerAtribucionesHandler()
    return handler.handle(consulta)
