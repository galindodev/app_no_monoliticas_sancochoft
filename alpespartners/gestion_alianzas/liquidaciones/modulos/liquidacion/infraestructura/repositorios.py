""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from uuid import UUID

from liquidaciones.config.db import db

from liquidaciones.modulos.liquidacion.dominio.entidades import Liquidacion
from liquidaciones.modulos.liquidacion.dominio.repositorios import RepositorioLiquidacion
from liquidaciones.modulos.liquidacion.dominio.fabricas import FabricaLiquidacion

from .mapeadores import MapeadorLiquidacion


class RepositorioLiquidacionesSQLAlchemy(RepositorioLiquidacion):
    def __init__(self):
        self.fabrica_liquidacion: FabricaLiquidacion = FabricaLiquidacion()

    def agregar(self, liquidacion: Liquidacion):
        liquidacion_dto = self.fabrica_liquidacion.crear_objeto(liquidacion, MapeadorLiquidacion())
        db.session.add(liquidacion_dto)

    def actualizar(self, liquidacion: Liquidacion):
        raise NotImplementedError

    def obtener_por_id(self, id: UUID) -> Liquidacion:
        raise NotImplementedError

    def obtener_todos(self) -> list[Liquidacion]:
        raise NotImplementedError

    def eliminar(self, id_liquidacion: UUID):
        raise NotImplementedError
