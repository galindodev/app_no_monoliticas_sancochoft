from alpespartners.seedwork.dominio.reglas import ReglaNegocio
from .objetos_valor import Monto


class MontoPositivo(ReglaNegocio):
    monto: Monto

    def __init__(self, monto, mensaje='El monto debe ser positivo'):
        super().__init__(mensaje)
        self.monto = monto

    def es_valido(self) -> bool:
        return self.monto.valor > 0
