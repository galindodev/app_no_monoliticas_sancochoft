import logging
from threading import Thread

from atribuciones.modulos.atribucion.infraestructura.consumidores import (
    SuscriptorAgregarAtribucion,
    SuscriptorPagoRechazado,
    SuscriptorPagoSolicitado,
)
from atribuciones.modulos.atribucion.infraestructura.despachadores import ProgramaCompletadoDispatcher, ProgramaReabiertoDispatcher
from atribuciones.seedwork.infraestructura.consumidores import Subscriptor
from atribuciones.seedwork.infraestructura.utils import register_esquemas


logger = logging.getLogger("gunicorn.error")
logging.basicConfig(level=logger.level)


def escuchar_mensaje(subscriptor: Subscriptor):
    subscriptor.subscribe()


def post_fork(_, __):
    # Publicar esquemas
    register_esquemas(SuscriptorAgregarAtribucion())
    register_esquemas(ProgramaCompletadoDispatcher())
    register_esquemas(ProgramaReabiertoDispatcher())

    # Comandos
    Thread(
        target=escuchar_mensaje, args=(SuscriptorAgregarAtribucion(),), daemon=True
    ).start()

    # Eventos
    Thread(
        target=escuchar_mensaje, args=(SuscriptorPagoSolicitado(),), daemon=True
    ).start()
    Thread(
        target=escuchar_mensaje, args=(SuscriptorPagoRechazado(),), daemon=True
    ).start()
