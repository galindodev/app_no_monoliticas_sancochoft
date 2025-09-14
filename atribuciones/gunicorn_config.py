import logging
from threading import Thread

from atribuciones.modulos.atribucion.infraestructura.consumidores import SuscriptorAgregarAtribucion
from atribuciones.seedwork.infraestructura.consumidores import Subscriptor


logger = logging.getLogger("gunicorn.error")
logging.basicConfig(level=logger.level)


def escuchar_mensaje(subscriptor: Subscriptor):
    subscriptor.subscribe()


def post_fork(_, __):
    # Comandos
    Thread(target=escuchar_mensaje, args=(SuscriptorAgregarAtribucion(),), daemon=True).start()
