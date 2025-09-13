""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de pagos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de pagos

"""

from __future__ import annotations
from dataclasses import dataclass

from pagos.seedwork.dominio.fabricas import Fabrica
from pagos.seedwork.dominio.repositorios import Repositorio

from pagos.modulos.pagos.dominio.repositorios import RepositorioPagos

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioPagosSQLAlchemy


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type) -> Repositorio:
        if obj == RepositorioPagos.__class__:
            return RepositorioPagosSQLAlchemy()
        else:
            raise ExcepcionFabrica()
