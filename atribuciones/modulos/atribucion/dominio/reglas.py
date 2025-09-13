from atribuciones.seedwork.dominio.reglas import ReglaNegocio

from .objetos_valor import Dinero


class DineroPositivo(ReglaNegocio):
    dinero: Dinero

    def __init__(self, dinero, mensaje='El dinero debe ser positivo'):
        super().__init__(mensaje)
        self.dinero = dinero

    def es_valido(self) -> bool:
        return self.dinero.monto > 0
