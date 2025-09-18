""" Excepciones del dominio de atribuciones
"""

from atribuciones.seedwork.dominio.excepciones import ExcepcionFabrica


class ProgramaNoEncontradoExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='El programa no fue encontrado.'):
        self.__mensaje = mensaje

    def __str__(self):
        return self.__mensaje
