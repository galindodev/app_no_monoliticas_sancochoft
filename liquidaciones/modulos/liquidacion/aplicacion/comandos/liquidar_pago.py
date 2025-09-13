import logging
from random import random
from dataclasses import dataclass

from liquidaciones.modulos.liquidacion.dominio.excepciones import LiquidaRechazadaExcepcion
from liquidaciones.seedwork.aplicacion.comandos import Comando
from liquidaciones.seedwork.aplicacion.comandos import ComandoHandler
from liquidaciones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from liquidaciones.seedwork.aplicacion.comandos import ejecutar_commando as comando

from liquidaciones.modulos.liquidacion.aplicacion.dto import LiquidacionDTO
from liquidaciones.modulos.liquidacion.dominio.entidades import Liquidacion
from liquidaciones.modulos.liquidacion.aplicacion.mapeadores import MapeadorLiquidacion

from liquidaciones.modulos.liquidacion.dominio.fabricas import FabricaLiquidacion
from liquidaciones.modulos.liquidacion.dominio.repositorios import RepositorioLiquidacion
from liquidaciones.modulos.liquidacion.infraestructura.fabricas import FabricaRepositorio


@dataclass
class LiquidarPago(Comando):
    id_pago: str
    id_influencer: str
    monto: float


class LiquidarPagoHandler(ComandoHandler):
    def __init__(self):
        self.fabrica_liquidacion = FabricaLiquidacion()
        self.fabrica_repositorio = FabricaRepositorio()

    def handle(self, comando: LiquidarPago):
        logging.info(comando)
        liquidacion_dto = LiquidacionDTO(
                id_pago = comando.id_pago,
                id_influencer=comando.id_influencer,
                monto=comando.monto)

        liquidacion: Liquidacion = self.fabrica_liquidacion.crear_objeto(liquidacion_dto, MapeadorLiquidacion())

        if not self.simular_pago():
            raise LiquidaRechazadaExcepcion(str(liquidacion.id))

        liquidacion.liquidar_pago(liquidacion)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioLiquidacion.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, liquidacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

    def simular_pago(self):
        ''' Simula la aprobacion o rechazo del pago. Retorna True si se aprueba, False si se rechaza.'''
        return random() > 0.5


@comando.register(LiquidarPago)
def ejecutar_comando_liquidar_pago(comando: LiquidarPago):
    handler = LiquidarPagoHandler()
    handler.handle(comando)
