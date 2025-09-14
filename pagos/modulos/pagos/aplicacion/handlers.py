from pagos.modulos.pagos.dominio.eventos import PagoSolicitado, PagoPagado, PagoRechazado
from pagos.modulos.pagos.infraestructura.despachadores import PagoPagadoDispatcher, PagoSolicitadoDispatcher, PagoRechazadoDispatcher
from pagos.seedwork.aplicacion.handlers import Handler


class HandlerPagoIntegracion(Handler):
    @staticmethod
    def handle_pago_solicitado(evento: PagoSolicitado):
        dispatcher = PagoSolicitadoDispatcher()
        dispatcher.handle(evento)

    @staticmethod
    def handle_pago_pagado(evento: PagoPagado):
        dispatcher = PagoPagadoDispatcher()
        dispatcher.handle(evento)

    @staticmethod
    def handle_pago_rechazado(evento: PagoRechazado):
        dispatcher = PagoRechazadoDispatcher()
        dispatcher.handle(evento)
