from pydispatch import dispatcher

from pagos.modulos.pagos.dominio.eventos import PagoSolicitado, PagoPagado, PagoRechazado

from .handlers import HandlerPagoIntegracion


dispatcher.connect(HandlerPagoIntegracion.handle_pago_solicitado, signal=f'{PagoSolicitado.__name__}Dominio')

dispatcher.connect(HandlerPagoIntegracion.handle_pago_pagado, signal=f'{PagoPagado.__name__}Dominio')

dispatcher.connect(HandlerPagoIntegracion.handle_pago_rechazado, signal=f'{PagoRechazado.__name__}Dominio')
