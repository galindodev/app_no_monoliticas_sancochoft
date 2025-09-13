import gevent
import logging
from gevent import monkey

monkey.patch_all()


greenlets = []
pulsar_clients = []

logger = logging.getLogger("gunicorn.error")


class PulsarClient:
    def __init__(self, name):
        logger.info(f"Cliente Pulsar {name} creado")

    def receive(self):
        logger.info("Escuchando en Pulsar...")

    def close(self): ...


def escuchar_comando(topic, sub_name, schema):
    client = PulsarClient(f"{topic}-{sub_name}")
    pulsar_clients.append(client)

    while True:
        client.receive()
        gevent.sleep(5)


def post_fork(_, __):
    g1 = gevent.spawn(escuchar_comando, "topico-1", "sub1", "schema1")

    greenlets.extend([g1])


def worker_exit(_, __):
    for greenlet in greenlets:
        greenlet.kill()

    for cliente in pulsar_clients:
        try:
            cliente.close()
        except Exception as error:
            logger.error("Error cerrando cliente Pulsar:", error)
