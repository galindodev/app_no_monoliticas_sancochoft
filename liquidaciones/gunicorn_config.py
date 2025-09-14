
import logging
from threading import Thread

from liquidaciones.modulos.liquidacion.infraestructura.consumidores import PagoSolicitadoSuscripcion
from liquidaciones.modulos.liquidacion.infraestructura.despachadores import LiquidacionFinalizadaDispatcher
from liquidaciones.seedwork.infraestructura.utils import register_esquemas
from liquidaciones.seedwork.infraestructura.consumidores import Subscriptor


logger = logging.getLogger("gunicorn.error")
logging.basicConfig(level=logger.level)


def escuchar_mensaje(subscriptor: Subscriptor):
    subscriptor.subscribe()


def post_fork(_, __):
    # Publicar los esquemas generados por este servicio
    register_esquemas(LiquidacionFinalizadaDispatcher())

    # Eventos
    Thread(target=escuchar_mensaje, args=(PagoSolicitadoSuscripcion(),), daemon=True).start()
