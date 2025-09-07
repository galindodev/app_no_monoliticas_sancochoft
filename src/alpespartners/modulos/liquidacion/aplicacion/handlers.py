from alpespartners.modulos.liquidacion.aplicacion.comandos.liquidar_pago import LiquidarPago
from alpespartners.modulos.pagos.dominio.eventos import PagoSolicitado
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando
from alpespartners.seedwork.aplicacion.handlers import Handler


class HandlerLiquidacionDominio(Handler):
    @staticmethod
    def handle_pago_solicitado(evento: PagoSolicitado):
        print("============= Manejando evento PagoSolicitado > LiquidarPago =============")
        comando = LiquidarPago(
            id_pago=str(evento.id_pago),
            id_influencer=str(evento.id_influencer),
            monto=evento.monto,
        )
        ejecutar_commando(comando)
