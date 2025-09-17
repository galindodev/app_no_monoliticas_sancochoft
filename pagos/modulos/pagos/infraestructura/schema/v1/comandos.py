from pulsar.schema import String, Float
from pagos.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)


class ComandoSolicitarPagoPayload(ComandoIntegracion):
    id_influencer = String()
    monto = Float()
    id_programa = String()
    id_correlacion = String()


class ComandoSolicitarPago(ComandoIntegracion):
    data = ComandoSolicitarPagoPayload()
