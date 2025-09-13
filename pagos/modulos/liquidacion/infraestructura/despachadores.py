import pulsar
from pulsar.schema import *

from pagos.modulos.liquidacion.infraestructura.fabricas import FabricaEventosDominio
from pagos.seedwork.infraestructura import utils

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
        raise NotImplementedError

    def publicar_evento(self, evento, topico):
        evento_infra = FabricaEventosDominio.crear_evento(evento)
        self._publicar_mensaje(evento_infra, topico, AvroSchema(type(evento_infra)))
