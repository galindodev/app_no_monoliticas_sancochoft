import logging
from gevent import monkey

monkey.patch_all()

from atribuciones.seedwork.infraestructura.consumidores import Subscriptor


greenlets = []
subscriptors: list[Subscriptor] = []

logger = logging.getLogger("gunicorn.error")
logging.basicConfig(level=logger.level)


def escuchar_mensaje(subscriptor: Subscriptor):
    subscriptors.append(subscriptor)
    subscriptor.subscribe()


def post_fork(_, __):
    greenlets.extend([
        # Commands
        # gevent.spawn(escuchar_mensaje, ...),
        # Events
    ])


def worker_exit(_, __):
    for greenlet in greenlets:
        greenlet.kill()

    for subscriptor in subscriptors:
        subscriptor.unsubscribe()
