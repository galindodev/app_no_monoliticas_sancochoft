import time
import os
import datetime
import requests
import json
from fastavro.schema import parse_schema
from pulsar.schema import AvroSchema

from .despachadores import BaseDispatcher


epoch = datetime.datetime.utcfromtimestamp(0)


def time_millis():
    return int(time.time() * 1000)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


def millis_a_datetime(millis):
    return datetime.datetime.fromtimestamp(millis / 1000.0)


def broker_host():
    return os.getenv("BROKER_HOST", default="localhost")


def consultar_schema_registry(topico: str) -> dict:
    response = requests.get(
        f"http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema"
    )
    response.raise_for_status()
    json_registry = response.json()
    return json.loads(json_registry.get("data", {}))


def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    definicion_schema = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=definicion_schema)


def register_esquemas(comando: BaseDispatcher):
    topic = comando.topic
    schema = comando.schema

    schema_info = AvroSchema(schema).schema_info()
    schema_json = schema_info.schema()

    url = f"http://{broker_host()}:8080/admin/v2/schemas/public/default/{topic}/schema"
    headers = {"Content-Type": "application/json"}
    payload = dict(type="AVRO", schema=schema_json)

    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()


def register_dlq_schema(topic: str):
    """ Registra el esquema del tópico original en el tópico DLQ asociado.
    """
    original_schema = consultar_schema_registry(f"public/default/{topic}")
    if not original_schema:
        raise ValueError(f"No se encontró el esquema para el tópico '{topic}'")

    dlq_topic = f"{topic}-DLQ"
    url = f"http://{broker_host()}:8080/admin/v2/schemas/public/default/{dlq_topic}/schema"
    headers = {"Content-Type": "application/json"}
    payload = dict(type="AVRO", schema=json.dumps(original_schema))
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
