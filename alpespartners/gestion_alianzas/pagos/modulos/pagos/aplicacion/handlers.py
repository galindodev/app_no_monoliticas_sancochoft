from pagos.modulos.pagos.aplicacion.comandos.finalizar_pago import FinalizarPago
from pagos.modulos.pagos.dominio.eventos import PagoSolicitado
from pagos.modulos.pagos.infraestructura.despachadores import Despachador
from pagos.seedwork.aplicacion.comandos import ejecutar_commando
from pagos.seedwork.aplicacion.handlers import Handler

from pagos.modulos.liquidacion.dominio.eventos import LiquidacionFinalizada


class HandlerPagoDominio(Handler):
    @staticmethod
    def handle_pago_solicitado(evento: PagoSolicitado):
        print("============= Despachando evento PagoSolicitado =============")
        despachador = Despachador()
        despachador.publicar_evento(evento, topico='eventos-pagos')


class HandlerLiquidacionDominio(Handler):
    @staticmethod
    def handle_liquidacion_finalizada(evento: LiquidacionFinalizada):
        comando = FinalizarPago(id_pago=evento.id_pago)
        ejecutar_commando(comando)
