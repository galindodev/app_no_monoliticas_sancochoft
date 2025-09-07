from pydispatch import dispatcher

from alpespartners.modulos.liquidacion.dominio.eventos import LiquidacionFinalizada

from .handlers import HandlerPagoDominio


dispatcher.connect(HandlerPagoDominio.handle_liquidacion_finalizada, signal=f'{LiquidacionFinalizada.__name__}Dominio')
