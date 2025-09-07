""" Excepciones del dominio de liquidacion

En este archivo usted encontrará los Excepciones relacionadas
al dominio de liquidacion

"""

from alpespartners.seedwork.dominio.excepciones import ExcepcionFabrica


class LiquidaRechazadaExcepcion(ExcepcionFabrica):
    def __init__(self, id_liquidacion, mensaje='La liquidación ha sido rechazada.'):
        self.id_liquidacion = id_liquidacion
        self.__mensaje = mensaje

    def __str__(self):
        return str(f'Liquidación {self.id_liquidacion}: {self.__mensaje}')
