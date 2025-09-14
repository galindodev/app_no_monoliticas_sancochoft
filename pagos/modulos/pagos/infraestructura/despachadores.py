from pagos.modulos.pagos.dominio.eventos import PagoSolicitado
from pagos.modulos.pagos.infraestructura.schema.v1.eventos import (
    EventoIntegracionPagoSolicitado,
    EventoIntegracionPagoSolicitadoPayload,
)

from pagos.seedwork.infraestructura.despachadores import BaseDispatcher


class PagoSolicitadoDispatcher(BaseDispatcher):
    topic = "eventos-pago-solicitado"
    schema = EventoIntegracionPagoSolicitado

    def map_event(self, evento: PagoSolicitado):
        return EventoIntegracionPagoSolicitado(
            data=EventoIntegracionPagoSolicitadoPayload(
                id_pago=str(evento.id_pago),
                id_influencer=str(evento.id_influencer),
                monto=evento.monto,
            )
        )
