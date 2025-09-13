from dataclasses import dataclass
from uuid import UUID

from atribuciones.seedwork.aplicacion.comandos import Comando
from atribuciones.seedwork.aplicacion.comandos import ComandoHandler
from atribuciones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from atribuciones.seedwork.aplicacion.comandos import ejecutar_commando as comando

from atribuciones.modulos.atribucion.aplicacion.dto import AtribucionDTO
from atribuciones.modulos.atribucion.dominio.entidades import Atribucion, ProgramaAtribucion
from atribuciones.modulos.atribucion.dominio.objetos_valor import EstadoAtribucion
from atribuciones.modulos.atribucion.aplicacion.mapeadores import MapeadorAtribucion

from atribuciones.modulos.atribucion.dominio.fabricas import FabricaAtribucion
from atribuciones.modulos.atribucion.dominio.repositorios import RepositorioProgramaAtribucion
from atribuciones.modulos.atribucion.infraestructura.fabricas import ProgramaFabricaRepositorio


@dataclass
class AgregarAtribucion(Comando):
    id_programa: str
    evento: str
    monto: float
    moneda: str


class AgregarAtribucionHandler(ComandoHandler):
    def __init__(self):
        self.fabrica_atribucion = FabricaAtribucion()
        self.fabrica_repositorio = ProgramaFabricaRepositorio()
        self.repositorio: RepositorioProgramaAtribucion = self.fabrica_repositorio.crear_objeto(ProgramaFabricaRepositorio.__class__)

    def handle(self, comando: AgregarAtribucion):
        atribucion_dto = AtribucionDTO(
                evento=comando.evento,
                monto=comando.monto,
                moneda=comando.moneda,
                estado=EstadoAtribucion.PENDIENTE.value)

        atribucion: Atribucion = self.fabrica_atribucion.crear_objeto(atribucion_dto, MapeadorAtribucion())

        programa: ProgramaAtribucion = self.repositorio.obtener_por_id(UUID(comando.id_programa))

        programa.agregar(atribucion)

        UnidadTrabajoPuerto.registrar_batch(self.repositorio.actualizar, programa)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(AgregarAtribucion)
def ejecutar_comando_agregar_atribucion(comando: AgregarAtribucion):
    handler = AgregarAtribucionHandler()
    handler.handle(comando)
