from alpespartners.modulos.liquidacion.dominio.eventos import LiquidacionFinalizada
from alpespartners.modulos.pagos.aplicacion.comandos.finalizar_pago import FinalizarPago
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando
from alpespartners.seedwork.aplicacion.handlers import Handler


class HandlerPagoDominio(Handler):
    @staticmethod
    def handle_liquidacion_finalizada(evento: LiquidacionFinalizada):
        print("============= Manejando evento LiquidacionFinalizada > FinalizarPago =============")
        # comando = FinalizarPago(id_pago=str(evento.id_pago))
        # ejecutar_commando(comando)
