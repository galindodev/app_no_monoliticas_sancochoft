from atribuciones.modulos.atribucion.dominio.eventos import ProgramaCompletado, ProgramaReabierto
from atribuciones.modulos.atribucion.infraestructura.despachadores import ProgramaCompletadoDispatcher, ProgramaReabiertoDispatcher
from atribuciones.seedwork.aplicacion.handlers import Handler


class HandlerProgramaIntegracion(Handler):
    @staticmethod
    def handle_programa_completado(evento: ProgramaCompletado):
        dispatcher = ProgramaCompletadoDispatcher()
        dispatcher.handle(evento)

    @staticmethod
    def handle_programa_reabierto(evento: ProgramaReabierto):
        dispatcher = ProgramaReabiertoDispatcher()
        dispatcher.handle(evento)
