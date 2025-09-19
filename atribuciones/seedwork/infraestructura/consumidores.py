import time
from abc import ABC, abstractmethod
from types import SimpleNamespace
import pulsar
import _pulsar
import logging
from pulsar.schema import AvroSchema

from atribuciones.api import create_app
from atribuciones.seedwork.infraestructura import utils


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
    enable_dlq: bool = False
    emit_message: bool = False

    def __init__(self):
        self.client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        self.logInfo(f"📥 Cliente Pulsar creado para tópico: '{self.topic}'")

    def process_message(self, _):
        raise NotImplementedError()

    def unsubscribe(self):
        try:
            self.logInfo(f"Cerrando cliente Pulsar para tópico '{self.topic}'...")
            self.client.close()
        except Exception as error:
            self.logError("Error cerrando cliente Pulsar:", error)

    def subscribe(self):
        app = create_app("Atribuciones")

        consumer = self.obtener_consumidor()
        self.logInfo(
            f"Suscrito a tópico: '{self.topic}' con subscripción '{self.sub_name}'"
        )

        self.logInfo(f"Esperando mensajes en tópico '{self.topic}'...")
        while True:
            try:
                message = consumer.receive(timeout_millis=1000)
                if message:
                    value = message.value()
                    data = SimpleNamespace(**value["data"])
                    self.logInfo(f"Llegó en tópico '{self.topic}': {data}")
                    with app.app_context():
                        try:
                            self.process_message(data if not self.emit_message else message)
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
                    dead_letter_policy=self.get_dlq_policy(),
                )
            except Exception as error:
                self.logError(
                    f"Error suscribiéndose al tópico '{self.topic}'. Intento {retries}:",
                    error,
                )
            time.sleep(5)

    def get_dlq_policy(self):
        if not self.enable_dlq:
            return None
        return pulsar.ConsumerDeadLetterPolicy(
            max_redeliver_count=3,
            dead_letter_topic=f"{self.topic}-DLQ",
        )

    def logInfo(self, message: str):
        logging.info("=================================")
        logging.info(f"============= {message}")
        logging.info("=================================")

    def logError(self, message: str, error=None):
        logging.error("=================================")
        if error:
            logging.error(f"{message} {error}")
        else:
            logging.error(message)
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

    @abstractmethod
    def process_message(self, _):
        raise NotImplementedError()

    def unsubscribe(self):
        try:
            self.logInfo(f"Cerrando cliente Pulsar para tópico '{self.topic}'...")
            self.client.close()
        except Exception as error:
            self.logError("Error cerrando cliente Pulsar", error)

    def subscribe(self):
        app = create_app("Atribuciones")
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
                            self.process_message(data)
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
