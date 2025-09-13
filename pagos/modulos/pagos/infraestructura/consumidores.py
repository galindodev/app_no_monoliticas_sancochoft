from pagos.modulos.pagos.aplicacion.comandos.finalizar_pago import FinalizarPago
from pagos.seedwork.aplicacion.comandos import ejecutar_commando
from pagos.modulos.pagos.aplicacion.comandos.solicitar_pago import SolicitarPago
from pagos.modulos.pagos.infraestructura.schema.v1.comandos import ComandoSolicitarPago
from pagos.seedwork.infraestructura.consumidores import CommandSubscriptor, EventSubscriptor


class SuscriptorSolicitarPago(CommandSubscriptor):
    topic = "comandos-pagos"
    sub_name = "alpespartners-pagos-sub-comandos"
    schema = ComandoSolicitarPago

    def process_message(self, data):
        solicitar_pago = SolicitarPago(id_influencer=data.id_influencer, monto=data.monto)
        ejecutar_commando(solicitar_pago)


class SubscriptorLiquidacionFinalizada(EventSubscriptor):
    topic = "eventos-liquidacion"
    sub_name = "eventos-pagos-a-liquidaciones"

    def process_message(self, data):
        self.logInfo(f"📥 Evento de liquidación finalizada recibido: {data}")
        finalizar_pago = FinalizarPago(id_pago=data.id_pago)
        ejecutar_commando(finalizar_pago)
