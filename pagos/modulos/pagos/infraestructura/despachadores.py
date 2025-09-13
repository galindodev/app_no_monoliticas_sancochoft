import pulsar
from pulsar.schema import AvroSchema

from pagos.modulos.pagos.dominio.eventos import PagoSolicitado
from pagos.modulos.pagos.infraestructura.schema.v1.comandos import (
    ComandoSolicitarPago,
    ComandoSolicitarPagoPayload,
)
from pagos.modulos.pagos.infraestructura.schema.v1.eventos import (
    EventoIntegracionPagoSolicitado,
    EventoIntegracionPagoSolicitadoPayload,
)
from pagos.seedwork.infraestructura import utils

import datetime

from pagos.seedwork.infraestructura.despachadores import BaseDispatcher

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


# TODO: deprecated
class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoSolicitarPagoPayload(
            id_influencer=comando.id_influencer, monto=comando.monto
        )
        comando_integracion = ComandoSolicitarPago(data=payload)
        self._publicar_mensaje(
            comando_integracion, topico, AvroSchema(ComandoSolicitarPago)
        )

class PagoSolicitadoDispatcher(BaseDispatcher):
    topic = "eventos-pagos"

    def map_event(self, evento: PagoSolicitado):
        return EventoIntegracionPagoSolicitado(
            data=EventoIntegracionPagoSolicitadoPayload(
                id_pago=str(evento.id_pago),
                id_influencer=str(evento.id_influencer),
                monto=evento.monto,
            )
        )
