import gevent
from abc import ABC
import pulsar, _pulsar
from pulsar.schema import AvroSchema
import logging

from atribuciones.api import create_app
from atribuciones.seedwork.infraestructura import utils


class Subscriptor(ABC):
    def subscribe(self):
        raise NotImplementedError

    def process_message(self):
        raise NotImplementedError

    def unsubscribe(self):
        raise NotImplementedError


class CommandSubscriptor(Subscriptor, ABC):
    topic: str
    sub_name: str
    schema: object
    client: pulsar.Client

    def __init__(self):
        self.client = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        self.logInfo(f"📥 Cliente Pulsar creado para tópico: '{self.topic}'")

    def subscribe(self):
        for data in self.suscribirse_a_mensajes():
            self.process_message(data)

    def process_message(self, _):
        raise NotImplementedError()

    def unsubscribe(self):
        try:
            self.logInfo(f"Cerrando cliente Pulsar para tópico '{self.topic}'...")
            self.client.close()
        except Exception as error:
            self.logError("Error cerrando cliente Pulsar:", error)

    def suscribirse_a_mensajes(self):
        app = create_app("Atribuciones")
        self.logInfo(f"⏱️ Suscribiendo a tópico '{self.topic}'...")
        try:
            consumer = self.client.subscribe(
                topic=self.topic,
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name=self.sub_name,
                schema=AvroSchema(self.schema),
                negative_ack_redelivery_delay_ms=5000,
            )
            self.logInfo(f"Suscrito a tópico: '{self.topic}' con subscripción '{self.sub_name}'")
        except Exception as error:
            self.logError(f"Error suscribiéndose al tópico '{self.topic}':", error)

            while True:
                self.logInfo(f"Esperando mensajes en tópico '{self.topic}'...")
                try:
                    message = consumer.receive(timeout_millis=1000)
                    if message:
                        data = message.value().data
                        self.logInfo(f"Llegó en tópico '{self.topic}': {data}")
                        with app.app_context():
                            try:
                                yield data
                                consumer.acknowledge(message)
                            except Exception as error:
                                self.logError(f"Error al procesar el mensaje en {self.topic}: {error}")
                                consumer.negative_acknowledge(message)
                except _pulsar.Timeout:
                    pass
                gevent.sleep(0)

    def logInfo(self, message: str):
        logging.info("=================================")
        logging.info(f"============= {message}")
        logging.info("=================================")

    def logError(self, message: str):
        logging.error("=================================")
        logging.error(message)
        logging.error("=================================")


class EventSubscriptor(Subscriptor, ABC):
    topic: str
    sub_name: str
    client: pulsar.Client

    def __init__(self):
        self.client = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        self.logInfo(f"📥 Cliente Pulsar creado para tópico: '{self.topic}'")

    def subscribe(self):
        self.logInfo(f"⏱️ Suscribiéndose al tópico '{self.topic}'...")
        for data in self.suscribirse_a_mensajes():
            self.process_message(data)

    def process_message(self, _):
        raise NotImplementedError()

    def unsubscribe(self):
        try:
            self.logInfo(f"Cerrando cliente Pulsar para tópico '{self.topic}'...")
            self.client.close()
        except Exception as error:
            self.logError("Error cerrando cliente Pulsar:", error)

    def suscribirse_a_mensajes(self):
        app = create_app("Atribuciones")

        schema = f"public/default/{self.topic}"
        try:
            json_schema = utils.consultar_schema_registry(schema)
            avro_schema = utils.obtener_schema_avro_de_diccionario(json_schema)

            self.logInfo(f"⏱️ Suscribiendo a tópico '{self.topic}'...")

            consumer = self.client.subscribe(
                topic=self.topic,
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name=self.sub_name,
                schema=avro_schema,
                negative_ack_redelivery_delay_ms=5000,
            )
            self.logError(f"Suscrito a tópico: '{self.topic}' con subscripción '{self.sub_name}'")
        except Exception as error:
            self.logError(f"Error suscribiéndose al tópico '{self.topic}':", error)

        while True:
            self.logInfo(f"Esperando mensajes en tópico '{self.topic}'...")
            try:
                message = consumer.receive(timeout_millis=1000)
                if message:
                    data = message.value().data
                    self.logInfo(f"Llegó en tópico '{self.topic}': {data}")
                    with app.app_context():
                        try:
                            yield data
                            consumer.acknowledge(message)
                        except Exception as error:
                            self.logError(f"Error al procesar el mensaje en {self.topic}: {error}")
                            consumer.negative_acknowledge(message)
            except _pulsar.Timeout:
                pass
            gevent.sleep(0)

    def logInfo(self, message: str):
        logging.info("=================================")
        logging.info(f"============= {message}")
        logging.info("=================================")

    def logError(self, message: str):
        logging.error("=================================")
        logging.error(message)
        logging.error("=================================")
