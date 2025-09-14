from pulsar.schema import Record, String, Float
from pagos.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class EventoPagoSolicitadoPayload(Record):
    id_pago = String()
    id_influencer = String()
    monto = Float()


class EventoPagoSolicitado(EventoIntegracion):
    data = EventoPagoSolicitadoPayload()
