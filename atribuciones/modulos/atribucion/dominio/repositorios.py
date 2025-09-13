""" Interfaces para los repositorios del dominio de atribucion

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de atribucion

"""

from abc import ABC

from atribuciones.seedwork.dominio.repositorios import Repositorio


class RepositorioProgramaAtribucion(Repositorio, ABC):
    ...
