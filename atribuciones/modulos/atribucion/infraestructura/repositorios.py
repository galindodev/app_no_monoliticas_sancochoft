""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from uuid import UUID

from atribuciones.config.db import db

from atribuciones.modulos.atribucion.dominio.entidades import ProgramaAtribucion
from atribuciones.modulos.atribucion.dominio.repositorios import RepositorioProgramaAtribucion
from atribuciones.modulos.atribucion.dominio.fabricas import FabricaProgramaAtribucion

from .mapeadores import MapeadorProgramaAtribucion
from .dto import ProgramaAtribucionesDTO


class RepositorioProgramaAtribucionSQLAlchemy(RepositorioProgramaAtribucion):
    def __init__(self):
        self.fabrica_programa = FabricaProgramaAtribucion()

    def obtener_por_id(self, id: UUID) -> ProgramaAtribucion:
        result = db.session.query(ProgramaAtribucionesDTO).filter_by(id=str(id)).one()
        return self.fabrica_programa.crear_objeto(result, MapeadorProgramaAtribucion())

    def obtener_todos(self) -> list[ProgramaAtribucion]:
        results = db.session.query(ProgramaAtribucionesDTO).all()
        return [self.fabrica_programa.crear_objeto(result, MapeadorProgramaAtribucion()) for result in results]

    def agregar(self, programa: ProgramaAtribucion):
        programa_dto = self.fabrica_programa.crear_objeto(programa, MapeadorProgramaAtribucion())
        db.session.add(programa_dto)

    def actualizar(self, programa: ProgramaAtribucion):
        programa_dto: ProgramaAtribucionesDTO = self.fabrica_programa.crear_objeto(programa, MapeadorProgramaAtribucion())
        db.session.merge(programa_dto)

    def eliminar(self, programa_id: UUID):
        programa_dto = db.session.query(ProgramaAtribucionesDTO).filter_by(id=str(programa_id)).one()
        db.session.delete(programa_dto)
