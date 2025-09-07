import pulsar
from pulsar.schema import *

from alpespartners.modulos.pagos.infraestructura.schema.v1.comandos import ComandoSolicitarPago, ComandoSolicitarPagoPayload
from alpespartners.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoSolicitarPagoPayload(id_influencer=comando.id_influencer, monto=comando.monto)
        comando_integracion = ComandoSolicitarPago(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoSolicitarPago))

    def publicar_evento(self, evento, topico):
        raise NotImplementedError
