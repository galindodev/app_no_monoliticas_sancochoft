"""Objetos valor del dominio de liquidacion

En este archivo usted encontrará los objetos valor del dominio de liquidacion

"""

from __future__ import annotations

from dataclasses import dataclass, field

from pagos.seedwork.dominio.objetos_valor import ObjetoValor


# TODO: Revisar si se puede mover al seedwork
@dataclass(frozen=True)
class Monto(ObjetoValor):
    valor: float = field(default_factory=float)
