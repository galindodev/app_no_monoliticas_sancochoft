from pydispatch import dispatcher

from .handlers import HandlerLiquidacionIntegracion

from liquidaciones.modulos.liquidacion.dominio.eventos import LiquidacionFinalizada

dispatcher.connect(HandlerLiquidacionIntegracion.handle_liquidacion_finalizada, signal=f'{LiquidacionFinalizada.__name__}Dominio')
