from atribuciones.modulos.atribucion.aplicacion.comandos.agregar_atribucion import AgregarAtribucion
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
