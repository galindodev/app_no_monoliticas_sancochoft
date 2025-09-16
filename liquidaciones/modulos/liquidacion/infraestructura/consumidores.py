from liquidaciones.modulos.liquidacion.aplicacion.comandos.liquidar_pago import LiquidarPago
from liquidaciones.seedwork.aplicacion.comandos import ejecutar_commando
from liquidaciones.seedwork.infraestructura.consumidores import EventSubscriptor


class PagoSolicitadoSuscripcion(EventSubscriptor):
    topic = "eventos-pago-solicitado"
    sub_name = "eventos-pagos-a-liquidaciones"
    enable_dlq = True

    def process_message(self, data):
        self.logInfo(f"📥 Evento de pago solicitado recibido: {data}")
        liquidar_pago = LiquidarPago(
            id_pago=data.id_pago,
            id_influencer=data.id_influencer,
            monto=data.monto
        )
        ejecutar_commando(liquidar_pago)
