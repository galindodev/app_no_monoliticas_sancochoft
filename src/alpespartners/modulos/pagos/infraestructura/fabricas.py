""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de pagos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de pagos

"""

from dataclasses import dataclass

from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.repositorios import Repositorio

from alpespartners.modulos.pagos.dominio.repositorios import RepositorioPagos

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioReservasSQLAlchemy


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type) -> Repositorio:
        if obj == RepositorioPagos.__class__:
            return RepositorioReservasSQLAlchemy()
        else:
            raise ExcepcionFabrica()
