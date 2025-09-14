import logging
from threading import Thread

from atribuciones.modulos.atribucion.infraestructura.consumidores import SuscriptorAgregarAtribucion
from atribuciones.seedwork.infraestructura.consumidores import Subscriptor
from atribuciones.seedwork.infraestructura.utils import register_esquemas


logger = logging.getLogger("gunicorn.error")
logging.basicConfig(level=logger.level)


def escuchar_mensaje(subscriptor: Subscriptor):
    subscriptor.subscribe()


def post_fork(_, __):
    register_esquemas(SuscriptorAgregarAtribucion())

    # Comandos
    Thread(target=escuchar_mensaje, args=(SuscriptorAgregarAtribucion(),), daemon=True).start()
