import logging
from dataclasses import dataclass
from uuid import UUID

from atribuciones.modulos.atribucion.dominio.repositorios import RepositorioProgramaAtribucion
from atribuciones.seedwork.aplicacion.comandos import Comando
from atribuciones.seedwork.aplicacion.comandos import ComandoHandler
from atribuciones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from atribuciones.seedwork.aplicacion.comandos import ejecutar_commando as comando

from atribuciones.modulos.atribucion.dominio.entidades import ProgramaAtribucion

from atribuciones.modulos.atribucion.dominio.fabricas import FabricaProgramaAtribucion
from atribuciones.modulos.atribucion.infraestructura.fabricas import ProgramaFabricaRepositorio


@dataclass
class CompletarPrograma(Comando):
    id_programa: str
    id_socio: str


class CompletarProgramaHandler(ComandoHandler):
    def __init__(self):
        self.fabrica_programa_atribucion = FabricaProgramaAtribucion()
        self.fabrica_repositorio = ProgramaFabricaRepositorio()
        self.repositorio: RepositorioProgramaAtribucion = self.fabrica_repositorio.crear_objeto(ProgramaFabricaRepositorio.__class__)

    def handle(self, comando: CompletarPrograma):
        logging.info(comando)
        programa: ProgramaAtribucion = self.repositorio.obtener_por_id(UUID(comando.id_programa))

        programa.completar(programa)

        UnidadTrabajoPuerto.registrar_batch(self.repositorio.actualizar, programa)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CompletarPrograma)
def ejecutar_comando_comnpletar_programa(comando: CompletarPrograma):
    handler = CompletarProgramaHandler()
    handler.handle(comando)
