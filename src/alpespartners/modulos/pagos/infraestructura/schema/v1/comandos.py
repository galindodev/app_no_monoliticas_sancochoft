from pulsar.schema import *
from alpespartners.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)


class ComandoSolicitarPagoPayload(ComandoIntegracion):
    id_influencer = String()
    monto = Float()


class ComandoSolicitarPago(ComandoIntegracion):
    data = ComandoSolicitarPagoPayload()
