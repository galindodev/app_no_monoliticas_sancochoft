from pydispatch import dispatcher

from atribuciones.modulos.atribucion.dominio.eventos import AtribucionAgregada

from .handlers import HandlerAtribucionDominio


dispatcher.connect(HandlerAtribucionDominio.handle_atribucion_agregada, signal=f'{AtribucionAgregada.__name__}Dominio')
