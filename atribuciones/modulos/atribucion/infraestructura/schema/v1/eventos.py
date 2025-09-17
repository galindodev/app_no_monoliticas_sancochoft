from pulsar.schema import Record, String

from atribuciones.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class EventoProgramaCompletadoPayload(Record):
    id_programa = String()
    id_socio = String()
    id_correlacion = String()


class EventoProgramaCompletado(EventoIntegracion):
    data = EventoProgramaCompletadoPayload()


class EventoProgramaReabiertoPayload(Record):
    id_programa = String()
    id_socio = String()
    id_correlacion = String()


class EventoProgramaReabierto(EventoIntegracion):
    data = EventoProgramaReabiertoPayload()
