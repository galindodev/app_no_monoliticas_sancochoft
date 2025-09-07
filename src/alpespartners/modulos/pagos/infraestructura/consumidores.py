import pulsar, _pulsar
from pulsar.schema import *
import logging
import traceback

from alpespartners.api import configure_app
from alpespartners.modulos.liquidacion.infraestructura.schema.v1.eventos import EventoDominioLiquidacionFinalizada
from alpespartners.modulos.pagos.aplicacion.comandos.solicitar_pago import SolicitarPago
from alpespartners.modulos.pagos.infraestructura.schema.v1.comandos import ComandoSolicitarPago
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando
from alpespartners.seedwork.infraestructura import utils


def suscribirse_a_eventos():
    cliente = None
    app = configure_app()
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(
            topic='eventos-liquidaciones',
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name='alpespartners-pagos-sub-eventos',
            schema=AvroSchema(EventoDominioLiquidacionFinalizada)
        )

        while True:
            mensaje = consumidor.receive()
            data = mensaje.value().data
            print('===========================')
            print(f'Evento recibido: {data}')
            print('===== ACTUALIZAR ESTADO DEL PAGO =====')
            print('===========================')

            # TODO: Lanzar comando para actualizar pago
            # comando = LiquidarPago(
            #     id_pago=data.id_pago,
            #     id_influencer=data.id_influencer,
            #     monto=data.monto
            # )
            # with app.app_context():
            #     ejecutar_commando(comando)

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos():
    cliente = None
    app = configure_app()

    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(topic='comandos-pagos', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='alpespartners-pagos-sub-comandos', schema=AvroSchema(ComandoSolicitarPago))

        while True:
            mensaje = consumidor.receive()
            data = mensaje.value().data
            print(f'Comando recibido: {data}')

            comando = SolicitarPago(id_influencer=data.id_influencer, monto=data.monto)
            with app.app_context():
                ejecutar_commando(comando)

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
