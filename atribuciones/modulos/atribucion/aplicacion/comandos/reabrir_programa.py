import logging
from dataclasses import dataclass
from uuid import UUID

from atribuciones.modulos.atribucion.dominio.repositorios import RepositorioProgramaAtribucion
from atribuciones.modulos.atribucion.infraestructura.fabricas import ProgramaFabricaRepositorio
from atribuciones.seedwork.aplicacion.comandos import Comando
from atribuciones.seedwork.aplicacion.comandos import ComandoHandler
from atribuciones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from atribuciones.seedwork.aplicacion.comandos import ejecutar_commando as comando

from atribuciones.modulos.atribucion.dominio.entidades import ProgramaAtribucion

from atribuciones.modulos.atribucion.dominio.fabricas import FabricaProgramaAtribucion


@dataclass
class ReabrirPrograma(Comando):
    id_programa: str


class ReabrirProgramaHandler(ComandoHandler):
    def __init__(self):
        self.fabrica_programa_atribucion = FabricaProgramaAtribucion()
        self.fabrica_repositorio = ProgramaFabricaRepositorio()
        self.repositorio: RepositorioProgramaAtribucion = self.fabrica_repositorio.crear_objeto(ProgramaFabricaRepositorio.__class__)

    def handle(self, comando: ReabrirPrograma):
        logging.info(comando)
        programa: ProgramaAtribucion = self.repositorio.obtener_por_id(UUID(comando.id_programa))
        if not programa:
            logging.error(f"❌ ReabrirProgramaHandler - No se encontró el programa de atribución con ID {comando.id_programa}")
            return

        programa.reabrir()

        UnidadTrabajoPuerto.registrar_batch(self.repositorio.actualizar, programa)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(ReabrirPrograma)
def ejecutar_comando_reabrir_programa(comando: ReabrirPrograma):
    handler = ReabrirProgramaHandler()
    handler.handle(comando)

