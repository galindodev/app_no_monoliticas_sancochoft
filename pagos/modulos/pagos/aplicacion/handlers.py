from pagos.modulos.pagos.dominio.eventos import PagoSolicitado
from pagos.modulos.pagos.infraestructura.despachadores import Despachador
from pagos.seedwork.aplicacion.handlers import Handler


class HandlerPagoDominio(Handler):
    @staticmethod
    def handle_pago_solicitado(evento: PagoSolicitado):
        print("============= Despachando evento PagoSolicitado =============")
        despachador = Despachador()
        despachador.publicar_evento(evento, topico='eventos-pagos')
