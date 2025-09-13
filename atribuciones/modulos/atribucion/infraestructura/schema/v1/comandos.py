from pulsar.schema import String, Float
from atribuciones.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)


# TODO: Cambiar por Agregar Atribucion
class ComandoSolicitarPagoPayload(ComandoIntegracion):
    id_influencer = String()
    monto = Float()


class ComandoSolicitarPago(ComandoIntegracion):
    data = ComandoSolicitarPagoPayload()
