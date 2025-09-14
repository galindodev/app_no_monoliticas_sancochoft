from dataclasses import dataclass

from atribuciones.modulos.atribucion.aplicacion.dto import ProgramaAtribucionDTO
from atribuciones.modulos.atribucion.aplicacion.mapeadores import MapeadorProgramaAtribucion
from atribuciones.modulos.atribucion.dominio.repositorios import RepositorioProgramaAtribucion
from atribuciones.seedwork.aplicacion.comandos import Comando
from atribuciones.seedwork.aplicacion.comandos import ComandoHandler
from atribuciones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from atribuciones.seedwork.aplicacion.comandos import ejecutar_commando as comando

from atribuciones.modulos.atribucion.dominio.entidades import ProgramaAtribucion

from atribuciones.modulos.atribucion.dominio.fabricas import FabricaProgramaAtribucion
from atribuciones.modulos.atribucion.infraestructura.fabricas import ProgramaFabricaRepositorio


@dataclass
class AgregarPrograma(Comando):
    id_socio: str


class AgregarProgramaHandler(ComandoHandler):
    def __init__(self):
        self.fabrica_programa_atribucion = FabricaProgramaAtribucion()
        self.fabrica_repositorio = ProgramaFabricaRepositorio()
        self.repositorio: RepositorioProgramaAtribucion = self.fabrica_repositorio.crear_objeto(ProgramaFabricaRepositorio.__class__)

    def handle(self, comando: AgregarPrograma):
        programa_dto = ProgramaAtribucionDTO(id_socio=comando.id_socio, atribuciones=[])
        programa: ProgramaAtribucion = self.fabrica_programa_atribucion.crear_objeto(programa_dto, MapeadorProgramaAtribucion())

        UnidadTrabajoPuerto.registrar_batch(self.repositorio.agregar, programa)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        return str(programa.id)


@comando.register(AgregarPrograma)
def ejecutar_comando_agregar_programa(comando: AgregarPrograma):
    handler = AgregarProgramaHandler()
    return handler.handle(comando)
