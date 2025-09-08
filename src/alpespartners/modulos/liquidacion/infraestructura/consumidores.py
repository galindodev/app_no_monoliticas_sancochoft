import pulsar, _pulsar
from pulsar.schema import *
import logging
import traceback

from alpespartners.api import configure_app
from alpespartners.modulos.liquidacion.aplicacion.comandos.liquidar_pago import LiquidarPago
from alpespartners.modulos.liquidacion.dominio.excepciones import LiquidaRechazadaExcepcion
from alpespartners.modulos.pagos.infraestructura.schema.v1.eventos import EventoDominioPagoSolicitado
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando
from alpespartners.seedwork.infraestructura import utils


def suscribirse_a_eventos():
    cliente = None
    app = configure_app()
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(
            topic='eventos-pagos',
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name='alpespartners-liquidacion-sub-eventos',
            schema=AvroSchema(EventoDominioPagoSolicitado),
            negative_ack_redelivery_delay_ms=5000
        )

        while True:
            mensaje = consumidor.receive()
            data = mensaje.value().data
            print('===========================')
            print(f'Evento recibido: {data}')
            print('===== PAGO SOLICITADO =====')
            print('===========================')

            comando = LiquidarPago(
                id_pago=data.id_pago,
                id_influencer=data.id_influencer,
                monto=data.monto
            )
            with app.app_context():
                try:
                    ejecutar_commando(comando)
                    consumidor.acknowledge(mensaje)
                    print("===========================")
                    print("===== PAGO LIQUIDADO =====")
                    print("===========================")
                except Exception as error:
                    print(f'Error al procesar el evento: {error}')
                    traceback.print_exc()
                    consumidor.negative_acknowledge(mensaje)

        cliente.close()
    except:
        print('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos():
    pass
