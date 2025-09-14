import logging

import pulsar
from pulsar.schema import AvroSchema

from pagos.seedwork.dominio.eventos import EventoDominio
from pagos.seedwork.infraestructura import utils


class BaseDispatcher:
    topic: str
    schema: object

    def handle(self, evento: EventoDominio):
        name = evento.__class__.__name__
        message = self.map_event(evento)
        self._publicar_mensaje(mensaje=message, topico=self.topic, schema=type(message))
        logging.info(f"============= Evento '{name}' despachado 🚀 =============")

    def map_event(self, _):
        raise NotImplementedError

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publicador = cliente.create_producer(topico, schema=AvroSchema(schema))
        publicador.send(mensaje)
        cliente.close()
