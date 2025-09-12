from pulsar.schema import *
from pagos.seedwork.infraestructura.schema.v1.eventos import EventoDominio

class EventoDominioLiquidacionFinalizadaPayload(Record):
    id_pago = String()
    id_liquidacion = String()
    pagado = Boolean()


class EventoDominioLiquidacionFinalizada(EventoDominio):
    data = EventoDominioLiquidacionFinalizadaPayload()
