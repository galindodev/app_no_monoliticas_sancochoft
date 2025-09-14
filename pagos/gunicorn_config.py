
import logging
from threading import Thread

from pagos.modulos.pagos.infraestructura.consumidores import SubscriptorLiquidacionFinalizada, SuscriptorSolicitarPago
from pagos.seedwork.infraestructura.consumidores import Subscriptor  # noqa: E402


logger = logging.getLogger("gunicorn.error")
logging.basicConfig(level=logger.level)


def escuchar_mensaje(subscriptor: Subscriptor):
    subscriptor.subscribe()


def post_fork(_, __):
    # Comandos
    Thread(target=escuchar_mensaje, args=(SuscriptorSolicitarPago(),), daemon=True).start()

    # Eventos
    Thread(target=escuchar_mensaje, args=(SubscriptorLiquidacionFinalizada(),), daemon=True).start()
