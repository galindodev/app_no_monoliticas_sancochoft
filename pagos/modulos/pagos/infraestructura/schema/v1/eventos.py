from pulsar.schema import Record, String, Float
from pagos.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class EventoPagoSolicitadoPayload(Record):
    id_pago = String()
    id_influencer = String()
    id_programa = String()
    monto = Float()


class EventoPagoSolicitado(EventoIntegracion):
    data = EventoPagoSolicitadoPayload()


class EventoPagoPagadoPayload(Record):
    id_pago = String()
    id_influencer = String()
    id_programa = String()


class EventoPagoPagado(EventoIntegracion):
    data = EventoPagoPagadoPayload()


class EventoPagoRechazadoPayload(Record):
    id_pago = String()
    id_influencer = String()
    id_programa = String()


class EventoPagoRechazado(EventoIntegracion):
    data = EventoPagoRechazadoPayload()
