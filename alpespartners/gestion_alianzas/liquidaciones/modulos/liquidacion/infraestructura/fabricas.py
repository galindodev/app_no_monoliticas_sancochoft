""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de liquidacion

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de liquidacion

"""

from __future__ import annotations
from dataclasses import dataclass

from liquidaciones.seedwork.dominio.fabricas import Fabrica
from liquidaciones.seedwork.dominio.repositorios import Repositorio

from liquidaciones.modulos.liquidacion.dominio.repositorios import RepositorioLiquidacion

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioLiquidacionesSQLAlchemy


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type) -> Repositorio:
        if obj == RepositorioLiquidacion.__class__:
            return RepositorioLiquidacionesSQLAlchemy()
        else:
            raise ExcepcionFabrica()
