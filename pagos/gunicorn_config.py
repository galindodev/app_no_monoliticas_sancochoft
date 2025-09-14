import gevent
import logging
from gevent import monkey

from pagos.seedwork.infraestructura.consumidores import Subscriptor

monkey.patch_all()

from pagos.modulos.pagos.infraestructura.consumidores import SubscriptorLiquidacionFinalizada, SuscriptorSolicitarPago


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
        gevent.spawn(escuchar_mensaje, SuscriptorSolicitarPago()),

        # Events
        gevent.spawn(escuchar_mensaje, SubscriptorLiquidacionFinalizada()),
    ])


def worker_exit(_, __):
    for greenlet in greenlets:
        greenlet.kill()
        greenlet.join(timeout=15)

    for subscriptor in subscriptors:
        subscriptor.unsubscribe()
