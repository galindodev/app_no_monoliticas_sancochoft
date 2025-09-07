""" Interfaces para los repositorios del dominio de liquidacion

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de liquidacion

"""

from abc import ABC
from alpespartners.seedwork.dominio.repositorios import Repositorio


class RepositorioLiquidacion(Repositorio, ABC):
    ...
