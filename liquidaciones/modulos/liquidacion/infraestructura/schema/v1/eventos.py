from pulsar.schema import Record, String, Boolean

from liquidaciones.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class EventoLiquidacionFinalizadaPayload(Record):
    id_pago = String()
    id_liquidacion = String()
    pagado = Boolean()
    id_correlacion = String()


class EventoLiquidacionFinalizada(EventoIntegracion):
    data = EventoLiquidacionFinalizadaPayload()


class EventoLiquidacionFallidaPayload(Record):
    id_pago = String()
    id_liquidacion = String()
    id_correlacion = String()


class EventoLiquidacionFallida(EventoIntegracion):
    data = EventoLiquidacionFallidaPayload()
