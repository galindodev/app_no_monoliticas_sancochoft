from dataclasses import dataclass

from alpespartners.seedwork.aplicacion.comandos import Comando
from alpespartners.seedwork.aplicacion.comandos import ComandoHandler
from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando as comando

from alpespartners.modulos.pagos.aplicacion.dto import PagoDTO
from alpespartners.modulos.pagos.dominio.entidades import Pago
from alpespartners.modulos.pagos.aplicacion.mapeadores import MapeadorPago

from alpespartners.modulos.pagos.dominio.fabricas import FabricaPagos
from alpespartners.modulos.pagos.dominio.repositorios import RepositorioPagos
from alpespartners.modulos.pagos.infraestructura.fabricas import FabricaRepositorio


@dataclass
class SolicitarPago(Comando):
    id_influencer: str
    monto: float


class SolicitarPagoHandler(ComandoHandler):
    def __init__(self):
        self.fabrica_pagos = FabricaPagos()
        self.fabrica_repositorio = FabricaRepositorio()

    def handle(self, comando: SolicitarPago):
        pago_dto = PagoDTO(
                id_influencer=comando.id_influencer,
                monto=comando.monto)

        pago: Pago = self.fabrica_pagos.crear_objeto(pago_dto, MapeadorPago())
        pago.solicitar(pago)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPagos.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, pago)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(SolicitarPago)
def ejecutar_comando_solicitar_pago(comando: SolicitarPago):
    handler = SolicitarPagoHandler()
    handler.handle(comando)
