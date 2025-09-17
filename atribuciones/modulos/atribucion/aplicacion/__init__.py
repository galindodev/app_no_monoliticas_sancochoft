from pydispatch import dispatcher

from atribuciones.modulos.atribucion.dominio.eventos import ProgramaCompletado, ProgramaReabierto

from .handlers import HandlerProgramaIntegracion

dispatcher.connect(HandlerProgramaIntegracion.handle_programa_completado, signal=f'{ProgramaCompletado.__name__}Dominio')

dispatcher.connect(HandlerProgramaIntegracion.handle_programa_reabierto, signal=f'{ProgramaReabierto.__name__}Dominio')
