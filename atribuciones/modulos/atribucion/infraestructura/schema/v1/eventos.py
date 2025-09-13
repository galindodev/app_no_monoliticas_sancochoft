from pulsar.schema import *
from atribuciones.seedwork.infraestructura.schema.v1.eventos import EventoDominio

# TODO: reusar
class EventoDominioAtribucionFinalizadaPayload(Record):
    id_pago = String()
    id_influencer = String()
    monto = Float()


class EventoDominioAtribucionFinalizada(EventoDominio):
    data = EventoDominioAtribucionFinalizadaPayload()
