from atribuciones.modulos.atribucion.dominio.eventos import ProgramaCompletado, ProgramaReabierto
from atribuciones.modulos.atribucion.infraestructura.despachadores import ProgramaCompletadoDispatcher, ProgramaReabiertoDispatcher
from atribuciones.seedwork.aplicacion.handlers import Handler


class HandlerProgramaIntegracion(Handler):
    @staticmethod
    def handle_programa_completado(evento: ProgramaCompletado):
        ProgramaCompletadoDispatcher.handle(evento)

    @staticmethod
    def handle_programa_reabierto(evento: ProgramaReabierto):
        ProgramaReabiertoDispatcher.handle(evento)
