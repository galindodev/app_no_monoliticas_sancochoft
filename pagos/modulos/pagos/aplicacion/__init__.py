from pydispatch import dispatcher

from pagos.modulos.pagos.dominio.eventos import PagoSolicitado

from .handlers import HandlerPagoDominio


dispatcher.connect(HandlerPagoDominio.handle_pago_solicitado, signal=f'{PagoSolicitado.__name__}Dominio')
