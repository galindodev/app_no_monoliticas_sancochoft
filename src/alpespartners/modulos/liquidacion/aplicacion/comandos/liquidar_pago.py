from dataclasses import dataclass

from alpespartners.modulos.liquidacion.dominio.excepciones import LiquidaRechazadaExcepcion
from alpespartners.seedwork.aplicacion.comandos import Comando
from alpespartners.seedwork.aplicacion.comandos import ComandoHandler
from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando as comando

from alpespartners.modulos.liquidacion.aplicacion.dto import LiquidacionDTO
from alpespartners.modulos.liquidacion.dominio.entidades import Liquidacion
from alpespartners.modulos.liquidacion.aplicacion.mapeadores import MapeadorLiquidacion

from alpespartners.modulos.liquidacion.dominio.fabricas import FabricaLiquidacion
from alpespartners.modulos.liquidacion.dominio.repositorios import RepositorioLiquidacion
from alpespartners.modulos.liquidacion.infraestructura.fabricas import FabricaRepositorio


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
        liquidacion_dto = LiquidacionDTO(
                id_pago = comando.id_pago,
                id_influencer=comando.id_influencer,
                monto=comando.monto)

        liquidacion: Liquidacion = self.fabrica_liquidacion.crear_objeto(liquidacion_dto, MapeadorLiquidacion())

        # TODO: Consumir servicio de pasarela de pagos
        pagado = True
        if not pagado:
            raise LiquidaRechazadaExcepcion(str(liquidacion.id))

        liquidacion.liquidar_pago(liquidacion)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioLiquidacion.__class__)


        repositorio.agregar(liquidacion)
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, liquidacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(LiquidarPago)
def ejecutar_comando_solicitar_pago(comando: LiquidarPago):
    handler = LiquidarPagoHandler()
    handler.handle(comando)
