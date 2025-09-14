import time
from abc import ABC
import pulsar
import _pulsar
import logging
from pulsar.schema import AvroSchema

from pagos.api import configure_app
from pagos.seedwork.infraestructura import utils


class Subscriptor(ABC):
    def subscribe(self):
        raise NotImplementedError

    def process_message(self):
        raise NotImplementedError

    def unsubscribe(self):
        raise NotImplementedError


class EventSubscriptor(Subscriptor, ABC):
    topic: str
    sub_name: str
    client: pulsar.Client
    max_retries: int = 20

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
        app = configure_app()

        consumer = self.obtener_consumidor()
        self.logError(f"Suscrito a tópico: '{self.topic}' con subscripción '{self.sub_name}'")

        self.logInfo(f"Esperando mensajes en tópico '{self.topic}'...")
        while True:
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

    def obtener_consumidor(self):
        schema = f"public/default/{self.topic}"
        retries = 0
        while True:
            if retries >= self.max_retries:
                self.logError(f"No se pudo suscribir al tópico '{self.topic}' después de {self.max_retries} intentos.")
                raise Exception(f"No se pudo suscribir al tópico '{self.topic}' después de {self.max_retries} intentos.")
            retries += 1
            try:
                json_schema = utils.consultar_schema_registry(schema)
                avro_schema = utils.obtener_schema_avro_de_diccionario(json_schema)
                return self.client.subscribe(
                    topic=self.topic,
                    consumer_type=_pulsar.ConsumerType.Shared,
                    subscription_name=self.sub_name,
                    schema=avro_schema,
                    negative_ack_redelivery_delay_ms=5000,
                )
            except Exception as error:
                self.logError(f"Error suscribiéndose al tópico '{self.topic}'. Intento {retries}:", error)
            time.sleep(5)

    def logInfo(self, message: str):
        logging.info("=================================")
        logging.info(f"============= {message}")
        logging.info("=================================")

    def logError(self, message: str, error=None):
        logging.error("=================================")
        logging.error(f"{message} {error}")
        logging.error("=================================")


class CommandSubscriptor(Subscriptor, ABC):
    topic: str
    sub_name: str
    schema: object
    client: pulsar.Client
    max_retries: int = 20

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
            self.logError("Error cerrando cliente Pulsar", error)

    def suscribirse_a_mensajes(self):
        app = configure_app()
        consumer = self.obtener_consumidor()
        self.logError(f"Suscrito a tópico: '{self.topic}' con subscripción '{self.sub_name}'")

        self.logInfo(f"Esperando mensajes en tópico '{self.topic}'...")
        while True:
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

    def obtener_consumidor(self):
        retries = 0
        while True:
            if retries >= self.max_retries:
                self.logError(f"No se pudo suscribir al tópico '{self.topic}' después de {self.max_retries} intentos.")
                raise Exception(f"No se pudo suscribir al tópico '{self.topic}' después de {self.max_retries} intentos.")
            retries += 1
            try:
                return self.client.subscribe(
                    topic=self.topic,
                    consumer_type=_pulsar.ConsumerType.Shared,
                    subscription_name=self.sub_name,
                    schema=AvroSchema(self.schema),
                    negative_ack_redelivery_delay_ms=5000,
                )
            except Exception as error:
                self.logError(f"Error suscribiéndose al tópico '{self.topic}'. Intento {retries}:", error)
            time.sleep(5)

    def logInfo(self, message: str):
        logging.info("=================================")
        logging.info(f"============= {message}")
        logging.info("=================================")

    def logError(self, message: str, error=None):
        logging.error("=================================")
        logging.error(f"{message} {error}")
        logging.error("=================================")
