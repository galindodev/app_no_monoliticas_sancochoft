from pulsar.schema import String, Float
from atribuciones.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)


class ComandoAgregarAtribucionPayload(ComandoIntegracion):
    id_programa = String()
    evento = String()
    monto = Float()
    moneda = String()


class ComandoAgregarAtribucion(ComandoIntegracion):
    data = ComandoAgregarAtribucionPayload()
