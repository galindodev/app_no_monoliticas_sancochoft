"""Objetos valor del dominio de pagos

En este archivo usted encontrará los objetos valor del dominio de pagos

"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field

from pagos.seedwork.dominio.objetos_valor import ObjetoValor


@dataclass(frozen=True)
class Monto(ObjetoValor):
    valor: float = field(default_factory=float)


class EstadoPago(str, Enum):
    CREADO = "CREADO"
    PAGADO = "PAGADO"
    RECHAZADO = "RECHAZADO"
