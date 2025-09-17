from flask import current_app

from liquidaciones.modulos.liquidacion.dominio.eventos import (
    LiquidacionFallida,
    LiquidacionFinalizada,
)
from liquidaciones.modulos.liquidacion.infraestructura.schema.v1.eventos import (
    EventoLiquidacionFallidaPayload,
    EventoLiquidacionFinalizada,
    EventoLiquidacionFinalizadaPayload,
    EventoLiquidacionFallida,
)
from liquidaciones.seedwork.infraestructura.despachadores import BaseDispatcher


class LiquidacionFinalizadaDispatcher(BaseDispatcher):
    topic = "eventos-liquidacion-finalizada"
    schema = EventoLiquidacionFinalizada

    def map_event(self, evento: LiquidacionFinalizada):
        return EventoLiquidacionFinalizada(
            data=EventoLiquidacionFinalizadaPayload(
                id_pago=str(evento.id_pago),
                id_liquidacion=str(evento.id_liquidacion),
                pagado=evento.pagado,
                id_correlacion=current_app.config['id_correlacion'],
            )
        )


class LiquidacionFallidaDispatcher(BaseDispatcher):
    topic = "eventos-liquidacion-fallida"
    schema = EventoLiquidacionFallida

    def map_event(self, evento: LiquidacionFallida):
        return EventoLiquidacionFallida(
            data=EventoLiquidacionFallidaPayload(
                id_pago=evento.id_pago,
                id_correlacion=current_app.config['id_correlacion'],
            )
        )
