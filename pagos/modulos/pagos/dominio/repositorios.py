""" Interfaces para los repositorios del dominio de pagos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de pagos

"""

from abc import ABC
from pagos.seedwork.dominio.repositorios import Repositorio


class RepositorioPagos(Repositorio, ABC):
    ...
