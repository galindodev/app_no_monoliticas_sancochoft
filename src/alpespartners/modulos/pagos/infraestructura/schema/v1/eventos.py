from pulsar.schema import *
from alpespartners.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class SolicitarPagoPayload(Record):
    id_pago = String()
    id_influencer = String()
    monto = Float()

class EventoSolicitarPago(EventoIntegracion):
    data = SolicitarPagoPayload()
