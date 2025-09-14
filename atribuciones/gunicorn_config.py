import gevent
import logging
from gevent import monkey

monkey.patch_all()

from atribuciones.modulos.atribucion.infraestructura.consumidores import SuscriptorAgregarAtribucion  # noqa: E402
from atribuciones.seedwork.infraestructura.consumidores import Subscriptor  # noqa: E402


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
        gevent.spawn(escuchar_mensaje, SuscriptorAgregarAtribucion()),
        # Events
    ])


def worker_exit(_, __):
    for greenlet in greenlets:
        greenlet.kill()
        greenlet.join(timeout=15)

    for subscriptor in subscriptors:
        subscriptor.unsubscribe()
