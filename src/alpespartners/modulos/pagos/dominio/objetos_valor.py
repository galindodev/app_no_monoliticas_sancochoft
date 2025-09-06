"""Objetos valor del dominio de pagos

En este archivo usted encontrará los objetos valor del dominio de pagos

"""

from __future__ import annotations

from dataclasses import dataclass, field
from alpespartners.seedwork.dominio.objetos_valor import ObjetoValor


@dataclass(frozen=True)
class Monto(ObjetoValor):
    valor: float = field(default_factory=float)
