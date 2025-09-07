from pydispatch import dispatcher

from alpespartners.modulos.pagos.dominio.eventos import PagoSolicitado

from .handlers import HandlerLiquidacionDominio


dispatcher.connect(HandlerLiquidacionDominio.handle_pago_solicitado, signal=f'{PagoSolicitado.__name__}Dominio')

