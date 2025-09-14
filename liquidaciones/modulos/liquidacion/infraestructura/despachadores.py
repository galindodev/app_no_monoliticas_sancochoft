

from liquidaciones.modulos.liquidacion.dominio.eventos import LiquidacionFinalizada
from liquidaciones.modulos.liquidacion.infraestructura.schema.v1.eventos import EventoLiquidacionFinalizada, EventoLiquidacionFinalizadaPayload
from liquidaciones.seedwork.infraestructura.despachadores import BaseDispatcher


class LiquidacionFinalizadaDispatcher(BaseDispatcher):
    topic = "eventos-liquidacion-finalizada"
    schema = EventoLiquidacionFinalizada

    def map_event(self, evento: LiquidacionFinalizada):
        return EventoLiquidacionFinalizada(
            data=EventoLiquidacionFinalizadaPayload(
                id_pago=str(evento.id_pago),
                id_liquidacion=str(evento.id_liquidacion),
                pagado=evento.pagado
            )
        )
