from __future__ import annotations
from dataclasses import dataclass

from pagos.seedwork.dominio.fabricas import Fabrica

from .repositorios import RepositorioSagaAtribucionesSQLAlchemy


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self):
        return RepositorioSagaAtribucionesSQLAlchemy()
