from pulsar.schema import *
from alpespartners.seedwork.infraestructura.schema.v1.eventos import EventoDominio

class EventoDominioPagoSolicitadoPayload(Record):
    id_pago = String()
    id_influencer = String()
    monto = Float()


class EventoDominioPagoSolicitado(EventoDominio):
    data = EventoDominioPagoSolicitadoPayload()
