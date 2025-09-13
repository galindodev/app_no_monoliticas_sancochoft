"""Objetos valor del dominio de liquidacion

En este archivo usted encontrará los objetos valor del dominio de liquidacion

"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field

from atribuciones.seedwork.dominio.objetos_valor import ObjetoValor


@dataclass(frozen=True)
class Dinero(ObjetoValor):
    monto: float = field(default_factory=float)
    moneda: str = field(default_factory=str)


class EstadoAtribucion(str, Enum):
    PENDIENTE = "PENDIENTE"
    VALIDADA = "VALIDADA"


class EventoAtribucion(str, Enum):
    CLIC = "CLIC"
    LEAD = "LEAD"
    PARTICIPACION = "PARTICIPACION"
