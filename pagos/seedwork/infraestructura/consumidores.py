from abc import ABC
import pulsar, _pulsar
from pulsar.schema import AvroSchema
import logging

from pagos.api import configure_app
from pagos.seedwork.infraestructura import utils


class BaseSubscriptor(ABC):
    topic: str
    sub_name: str
    schema: object
    client: pulsar.Client

    def __init__(self):
        self.client = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        self.logInfo(f"Cliente Pulsar creado para tópico: '{self.topic}'")

    def subscribe(self):
        for data in self.suscribirse_a_comandos():
            self.process_command(data)

    def process_command(self, _):
        raise NotImplementedError()

    def unsubscribe(self):
        try:
            self.logInfo(f"Cerrando cliente Pulsar para tópico '{self.topic}'...")
            self.client.close()
        except Exception as error:
            self.logError("Error cerrando cliente Pulsar:", error)

    def suscribirse_a_comandos(self):
        app = configure_app()
        try:
            consumer = self.client.subscribe(
                topic=self.topic,
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name=self.sub_name,
                schema=AvroSchema(self.schema),
                negative_ack_redelivery_delay_ms=5000,
            )
            self.logError(f"Suscrito a tópico: '{self.topic}' con subscripción '{self.sub_name}'")
        except Exception as error:
            self.logError("Error suscribiéndose al tópico de comandos:", error)

        while True:
            self.logInfo(f" Esperando comandos en tópico '{self.topic}'...")
            message = consumer.receive()
            data = message.value().data
            self.logInfo(f"Comando llegó en tópico '{self.topic}': {data}")
            with app.app_context():
                try:
                    yield data
                    consumer.acknowledge(message)
                except Exception as error:
                    self.logError(f"Error al procesar el comando en {self.topic}: {error}")
                    consumer.negative_acknowledge(message)

    def logInfo(self, message: str):
        logging.info("=================================")
        logging.info(f"============= {message}")
        logging.info("=================================")

    def logError(self, message: str):
        logging.error("=================================")
        logging.error(message)
        logging.error("=================================")
