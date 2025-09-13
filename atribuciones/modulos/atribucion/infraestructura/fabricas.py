""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de atribucion

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de atribucion

"""

from __future__ import annotations
from dataclasses import dataclass

from atribuciones.seedwork.dominio.fabricas import Fabrica
from atribuciones.seedwork.dominio.repositorios import Repositorio

from atribuciones.modulos.atribucion.dominio.repositorios import RepositorioProgramaAtribucion

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioProgramaAtribucionSQLAlchemy


@dataclass
class ProgramaFabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type) -> Repositorio:
        if obj == RepositorioProgramaAtribucion.__class__:
            return RepositorioProgramaAtribucionSQLAlchemy()
        else:
            raise ExcepcionFabrica()
