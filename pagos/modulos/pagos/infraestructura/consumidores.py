from pagos.seedwork.aplicacion.comandos import ejecutar_commando
from pagos.modulos.pagos.aplicacion.comandos.solicitar_pago import SolicitarPago
from pagos.modulos.pagos.infraestructura.schema.v1.comandos import ComandoSolicitarPago
from pagos.seedwork.infraestructura.consumidores import BaseSubscriptor


class SuscriptorSolicitarPago(BaseSubscriptor):
    topic = "comandos-pagos"
    sub_name = "alpespartners-pagos-sub-comandos"
    schema = ComandoSolicitarPago

    def process_message(self, data):
        solicitar_pago = SolicitarPago(id_influencer=data.id_influencer, monto=data.monto)
        ejecutar_commando(solicitar_pago)
