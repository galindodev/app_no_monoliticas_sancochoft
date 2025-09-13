import gevent
import logging
from gevent import monkey

from pagos.modulos.pagos.infraestructura.consumidores import SuscriptorSolicitarPago

monkey.patch_all()


greenlets = []
subscriptors = []

logger = logging.getLogger("gunicorn.error")
logging.basicConfig(level=logger.level)


def escuchar_comando(subscriptor):
    subscriptors.append(subscriptor)
    subscriptor.subscribe()


def post_fork(_, __):
    g1 = gevent.spawn(escuchar_comando, SuscriptorSolicitarPago())
    greenlets.extend([g1])


def worker_exit(_, __):
    for greenlet in greenlets:
        greenlet.kill()

    for subscriptor in subscriptors:
        subscriptor.unsubscribe()
