import logging

from atribuciones.modulos.atribucion.dominio.eventos import AtribucionAgregada
from atribuciones.seedwork.aplicacion.handlers import Handler


class HandlerAtribucionDominio(Handler):
    @staticmethod
    def handle_atribucion_agregada(evento: AtribucionAgregada):
        # TODO: despachar evento
        logging.info("============= Despachando evento AtribucionAgregada =============")
