from pagos.modulos.sagas.aplicacion.coordinadores.saga_pago_atribuciones import SagaPagoAtribucionesCoreador
from pagos.seedwork.infraestructura.consumidores import CommandSubscriptor, EventSubscriptor


class SagaEvent(EventSubscriptor):
    topic: str
    sub_name: str
    nombre: str
    tipo_mensaje: str

    def __init__(self, topic: str, sub_name: str, nombre: str, tipo_mensaje: str):
        self.topic = topic
        self.sub_name = sub_name
        self.nombre = nombre
        self.tipo_mensaje = tipo_mensaje
        super().__init__()
        self.saga = SagaPagoAtribucionesCoreador()

    @staticmethod
    def create(topic: str):
        sub_name = f"saga-{topic}"
        tipo_mensaje = "EVENTO" if topic.startswith("eventos") else "COMANDO"

        splitted = topic.split("-")[1:]
        upper_first = [word.capitalize() for word in splitted]
        nombre = "".join(upper_first)

        return SagaEvent(topic, sub_name, nombre, tipo_mensaje)

    def process_message(self, data):
        self.logInfo(f"🐍 Saga - Mensaje {self.nombre} recibido")
        self.saga.procesar(
            dict(
                id_correlacion=data.id_correlacion,
                nombre=self.nombre,
                tipo_mensaje=self.tipo_mensaje,
            )
        )


class SagaCommand(CommandSubscriptor):
    topic: str
    sub_name: str
    nombre: str
    tipo_mensaje: str

    def __init__(self, topic: str, sub_name: str, nombre: str, tipo_mensaje: str):
        self.topic = topic
        self.sub_name = sub_name
        self.nombre = nombre
        self.tipo_mensaje = tipo_mensaje
        super().__init__()
        self.saga = SagaPagoAtribucionesCoreador()

    @staticmethod
    def create(topic: str):
        sub_name = f"saga-{topic}"
        tipo_mensaje = "EVENTO" if topic.startswith("eventos") else "COMANDO"

        splitted = topic.split("-")[1:]
        upper_first = [word.capitalize() for word in splitted]
        nombre = "".join(upper_first)

        return SagaEvent(topic, sub_name, nombre, tipo_mensaje)

    def process_message(self, data):
        self.logInfo(f"🐍 Saga - Mensaje {self.nombre} recibido")
        self.saga.procesar(
            dict(
                id_correlacion=data.id_correlacion,
                nombre=self.nombre,
                tipo_mensaje=self.tipo_mensaje,
            )
        )
