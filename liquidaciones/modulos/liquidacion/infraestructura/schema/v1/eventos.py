from pulsar.schema import Record, String, Boolean

from liquidaciones.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class EventoLiquidacionFinalizadaPayload(Record):
    id_pago = String()
    id_liquidacion = String()
    pagado = Boolean()


class EventoLiquidacionFinalizada(EventoIntegracion):
    data = EventoLiquidacionFinalizadaPayload()
