import logging
from threading import Thread

from pagos.modulos.pagos.infraestructura.consumidores import (
    LiquidacionFinalizadaSuscripcion,
    SuscriptorSolicitarPago,
    LiquidacionFallidaSuscripcion,
)
from pagos.modulos.pagos.infraestructura.despachadores import (
    PagoSolicitadoDispatcher,
    PagoPagadoDispatcher,
    PagoRechazadoDispatcher,
)
from pagos.modulos.sagas.infraestructura.consumidores import SagaEvent, SagaCommand
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
    Thread(
        target=escuchar_mensaje, args=(SuscriptorSolicitarPago(),), daemon=True
    ).start()

    # Eventos
    Thread(
        target=escuchar_mensaje, args=(LiquidacionFinalizadaSuscripcion(),), daemon=True
    ).start()
    Thread(
        target=escuchar_mensaje, args=(LiquidacionFallidaSuscripcion(),), daemon=True
    ).start()

    # Sagas
    Thread(
        target=escuchar_mensaje,
        args=(SagaCommand.create("comandos-solicitar-pago"),),
        daemon=True,
    ).start()

    events_topics = [
        "eventos-pago-solicitado",
        "eventos-programa-completado",
        "eventos-liquidacion-finalizada",
        "eventos-liquidacion-fallida",
        "eventos-pago-pagado",
        "eventos-pago-rechazado",
        "eventos-programa-completado",
        "eventos-programa-reabierto",
    ]
    for topic in events_topics:
        saga = SagaEvent.create(topic)
        Thread(target=escuchar_mensaje, args=(saga,), daemon=True).start()
