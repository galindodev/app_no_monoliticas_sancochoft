
import logging
from threading import Thread

from pagos.modulos.pagos.infraestructura.consumidores import LiquidacionFinalizadaSuscripcion, SuscriptorSolicitarPago
from pagos.modulos.pagos.infraestructura.despachadores import PagoSolicitadoDispatcher, PagoPagadoDispatcher, PagoRechazadoDispatcher
from pagos.seedwork.infraestructura.consumidores import Subscriptor
from pagos.seedwork.infraestructura.utils import register_esquemas


logger = logging.getLogger("gunicorn.error")
logging.basicConfig(level=logger.level)


def escuchar_mensaje(subscriptor: Subscriptor):
    subscriptor.subscribe()


def post_fork(_, __):
    # Publicar los esquemas generados por este servicio
    register_esquemas(SuscriptorSolicitarPago())
    register_esquemas(PagoSolicitadoDispatcher())
    register_esquemas(PagoPagadoDispatcher())
    register_esquemas(PagoRechazadoDispatcher())

    # Comandos
    Thread(target=escuchar_mensaje, args=(SuscriptorSolicitarPago(),), daemon=True).start()

    # Eventos
    Thread(target=escuchar_mensaje, args=(LiquidacionFinalizadaSuscripcion(),), daemon=True).start()
