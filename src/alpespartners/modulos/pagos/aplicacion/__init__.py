from pydispatch import dispatcher

from alpespartners.modulos.pagos.dominio.eventos import PagoSolicitado
from alpespartners.modulos.liquidacion.dominio.eventos import LiquidacionFinalizada

from .handlers import HandlerPagoDominio, HandlerLiquidacionDominio


dispatcher.connect(HandlerPagoDominio.handle_pago_solicitado, signal=f'{PagoSolicitado.__name__}Dominio')

dispatcher.connect(HandlerLiquidacionDominio.handle_liquidacion_finalizada, signal=f'{LiquidacionFinalizada.__name__}Dominio')
