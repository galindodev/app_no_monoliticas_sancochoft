from flask import current_app

from atribuciones.modulos.atribucion.aplicacion.comandos.agregar_atribucion import AgregarAtribucion
from atribuciones.modulos.atribucion.aplicacion.comandos.completar_programa import CompletarPrograma
from atribuciones.modulos.atribucion.aplicacion.comandos.reabrir_programa import ReabrirPrograma

from atribuciones.modulos.atribucion.infraestructura.schema.v1.comandos import ComandoAgregarAtribucion
from atribuciones.seedwork.aplicacion.comandos import ejecutar_commando
from atribuciones.seedwork.infraestructura.consumidores import CommandSubscriptor, EventSubscriptor


class SuscriptorAgregarAtribucion(CommandSubscriptor):
    topic = "comandos-atribuciones"
    sub_name = "atribuciones-sub-comandos"
    schema = ComandoAgregarAtribucion

    def process_message(self, data):
        current_app.config['id_correlacion'] = str(data.id_correlacion)
        agregar_atribucion = AgregarAtribucion(
            id_programa=data.id_programa,
            evento=data.evento,
            monto=data.monto,
            moneda=data.moneda)
        ejecutar_commando(agregar_atribucion)


class SuscriptorPagoSolicitado(EventSubscriptor):
    topic = "eventos-pago-solicitado"
    sub_name = "eventos-pagos-solicitados-a-atribuciones"

    def process_message(self, data):
        self.logInfo(f"📥 Evento de pago solicitado recibido: {data}")
        current_app.config['id_correlacion'] = str(data.id_correlacion)
        completar_programa = CompletarPrograma(
            id_programa=data.id_programa,
            id_socio=data.id_influencer
        )
        ejecutar_commando(completar_programa)


class SuscriptorPagoRechazado(EventSubscriptor):
    topic = "eventos-pago-rechazado"
    sub_name = "eventos-pagos-rechazados-a-atribuciones"

    def process_message(self, data):
        self.logInfo(f"📥 Evento de pago rechazado recibido: {data}")
        current_app.config['id_correlacion'] = str(data.id_correlacion)
        reabrir_programa = ReabrirPrograma(
            id_programa=data.id_programa
        )
        ejecutar_commando(reabrir_programa)
