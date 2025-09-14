from atribuciones.modulos.atribucion.aplicacion.comandos.agregar_atribucion import AgregarAtribucion
from atribuciones.modulos.atribucion.aplicacion.comandos.completar_programa import CompletarPrograma
from atribuciones.modulos.atribucion.aplicacion.comandos.reabrir_programa import ReabrirPrograma

from atribuciones.modulos.atribucion.infraestructura.schema.v1.comandos import ComandoAgregarAtribucion
from atribuciones.seedwork.aplicacion.comandos import ejecutar_commando
from atribuciones.seedwork.infraestructura.consumidores import CommandSubscriptor


class SuscriptorAgregarAtribucion(CommandSubscriptor):
    topic = "comandos-atribuciones"
    sub_name = "atribuciones-sub-comandos"
    schema = ComandoAgregarAtribucion

    def process_message(self, data):
        agregar_atribucion = AgregarAtribucion(
            id_programa=data.id_programa,
            evento=data.evento,
            monto=data.monto,
            moneda=data.moneda)
        ejecutar_commando(agregar_atribucion)


class SuscriptorPagoPagado(CommandSubscriptor):
    topic = "eventos-pago-pagado"
    sub_name = "eventos-pagos-pagados-a-atribuciones"

    def process_message(self, data):
        self.logInfo(f"📥 Evento de pago pagado recibido: {data}")
        completar_programa = CompletarPrograma(
            id_programa=data.id_programa,
            id_pago=data.id_pago
        )
        ejecutar_commando(completar_programa)


class SuscriptorPagoRechazado(CommandSubscriptor):
    topic = "eventos-pago-rechazado"
    sub_name = "eventos-pagos-rechazados-a-atribuciones"

    def process_message(self, data):
        self.logInfo(f"📥 Evento de pago rechazado recibido: {data}")
        reabrir_programa = ReabrirPrograma(
            id_programa=data.id_programa
        )
        ejecutar_commando(reabrir_programa)
