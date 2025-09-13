from pagos.modulos.pagos.dominio.eventos import PagoSolicitado
from pagos.modulos.pagos.infraestructura.despachadores import PagoSolicitadoDispatcher
from pagos.seedwork.aplicacion.handlers import Handler


class HandlerPagoIntegracion(Handler):
    @staticmethod
    def handle_pago_solicitado(evento: PagoSolicitado):
        dispatcher = PagoSolicitadoDispatcher()
        dispatcher.handle(evento)
