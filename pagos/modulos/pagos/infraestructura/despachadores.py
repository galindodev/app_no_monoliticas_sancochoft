from flask import current_app

from pagos.modulos.pagos.dominio.eventos import PagoPagado, PagoRechazado, PagoSolicitado
from pagos.modulos.pagos.infraestructura.schema.v1.eventos import (
    EventoPagoPagado,
    EventoPagoPagadoPayload,
    EventoPagoSolicitado,
    EventoPagoSolicitadoPayload,
    EventoPagoRechazado,
    EventoPagoRechazadoPayload,
)

from pagos.seedwork.infraestructura.despachadores import BaseDispatcher


class PagoSolicitadoDispatcher(BaseDispatcher):
    topic = "eventos-pago-solicitado"
    schema = EventoPagoSolicitado

    def map_event(self, evento: PagoSolicitado):
        return EventoPagoSolicitado(
            data=EventoPagoSolicitadoPayload(
                id_pago=str(evento.id_pago),
                id_influencer=str(evento.id_influencer),
                monto=evento.monto,
                id_programa=str(evento.id_programa),
                id_correlacion=current_app.config['id_correlacion'],
            )
        )


class PagoPagadoDispatcher(BaseDispatcher):
    topic = "eventos-pago-pagado"
    schema = EventoPagoPagado

    def map_event(self, evento: PagoPagado):
        return EventoPagoPagado(
            data=EventoPagoPagadoPayload(
                id_pago=str(evento.id_pago),
                id_influencer=str(evento.id_influencer),
                id_programa=str(evento.id_programa),
                id_correlacion=current_app.config['id_correlacion'],
            )
        )


class PagoRechazadoDispatcher(BaseDispatcher):
    topic = "eventos-pago-rechazado"
    schema = EventoPagoRechazado

    def map_event(self, evento: PagoRechazado):
        return EventoPagoRechazado(
            data=EventoPagoRechazadoPayload(
                id_pago=str(evento.id_pago),
                id_influencer=str(evento.id_influencer),
                id_programa=str(evento.id_programa),
                id_correlacion=current_app.config['id_correlacion'],
            )
        )
