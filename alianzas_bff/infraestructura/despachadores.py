import pulsar
from pulsar.schema import *

from . import utils

class Despachador:
    def publicar_mensaje(self, mensaje, topico):
        schema = f"public/default/{topico}"
        json_schema = utils.consultar_schema_registry(schema)
        avro_schema = utils.obtener_schema_avro_de_diccionario(json_schema)

        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=avro_schema)
        publicador.send(mensaje)
        cliente.close()
