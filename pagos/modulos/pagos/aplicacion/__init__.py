from pydispatch import dispatcher

from pagos.modulos.pagos.dominio.eventos import PagoSolicitado

from .handlers import HandlerPagoIntegracion


dispatcher.connect(HandlerPagoIntegracion.handle_pago_solicitado, signal=f'{PagoSolicitado.__name__}Dominio')
