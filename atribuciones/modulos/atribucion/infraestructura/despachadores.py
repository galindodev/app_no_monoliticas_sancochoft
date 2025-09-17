from atribuciones.modulos.atribucion.dominio.eventos import ProgramaCompletado, ProgramaReabierto
from atribuciones.modulos.atribucion.infraestructura.schema.v1.eventos import EventoProgramaCompletado, EventoProgramaCompletadoPayload, EventoProgramaReabierto, EventoProgramaReabiertoPayload
from atribuciones.seedwork.infraestructura.despachadores import BaseDispatcher


class ProgramaCompletadoDispatcher(BaseDispatcher):
    topic = "eventos-programa-completado"
    schema = EventoProgramaCompletado

    def map_event(self, evento: ProgramaCompletado):
        return EventoProgramaCompletado(
            data=EventoProgramaCompletadoPayload(
                id_programa=str(evento.id_programa),
                id_socio=str(evento.id_socio),
            )
        )


class ProgramaReabiertoDispatcher(BaseDispatcher):
    topic = "eventos-programa-reabierto"
    schema = EventoProgramaReabierto

    def map_event(self, evento: ProgramaReabierto):
        return EventoProgramaReabierto(
            data=EventoProgramaReabiertoPayload(
                id_programa=str(evento.id_programa),
                id_socio=str(evento.id_socio),
            )
        )
