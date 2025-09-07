from alpespartners.modulos.pagos.dominio.eventos import PagoSolicitado
from alpespartners.modulos.pagos.infraestructura.despachadores import Despachador
from alpespartners.seedwork.aplicacion.handlers import Handler


class HandlerPagoDominio(Handler):
    @staticmethod
    def handle_pago_solicitado(evento: PagoSolicitado):
        print("============= Despachando evento PagoSolicitado =============")
        despachador = Despachador()
        despachador.publicar_evento(evento, topico='eventos-pagos')
