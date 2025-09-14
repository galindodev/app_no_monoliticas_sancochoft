from uuid import UUID
from dataclasses import dataclass

from pagos.seedwork.aplicacion.comandos import Comando
from pagos.seedwork.aplicacion.comandos import ComandoHandler
from pagos.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from pagos.seedwork.aplicacion.comandos import ejecutar_commando as comando

from pagos.modulos.pagos.dominio.entidades import Pago

from pagos.modulos.pagos.dominio.fabricas import FabricaPagos
from pagos.modulos.pagos.dominio.repositorios import RepositorioPagos
from pagos.modulos.pagos.infraestructura.fabricas import FabricaRepositorio


@dataclass
class FinalizarPago(Comando):
    id_pago: str
    pagado: bool


class FinalizarPagoHandler(ComandoHandler):
    def __init__(self):
        self.fabrica_pagos = FabricaPagos()

        fabrica_repositorio = FabricaRepositorio()
        self.repositorio = fabrica_repositorio.crear_objeto(RepositorioPagos.__class__)

    def handle(self, comando: FinalizarPago):
        pago: Pago = self.repositorio.obtener_por_id(UUID(comando.id_pago))

        pago.finalizar()

        UnidadTrabajoPuerto.registrar_batch(self.repositorio.actualizar, pago)
        UnidadTrabajoPuerto.savepoint()


@comando.register(FinalizarPago)
def ejecutar_comando_finalizar_pago(comando: FinalizarPago):
    handler = FinalizarPagoHandler()
    handler.handle(comando)
