import logging

from flask import request

from liquidaciones.modulos.liquidacion.aplicacion.comandos.liquidar_pago import LiquidarPago
from liquidaciones.seedwork.aplicacion.comandos import ejecutar_commando
from liquidaciones.modulos.liquidacion.infraestructura import consumidores
from liquidaciones.modulos.liquidacion.infraestructura import despachadores

from .app import create_app, registrar_background_tasks


def init_app():
    app = create_app("Liquidaciones")

    @app.post("/liquidaciones")
    def liquidar_pago():
        """Endpoint de prueba para liquidar un pago."""
        comando = LiquidarPago(**request.json)
        ejecutar_commando(comando)
        return dict(message="Liquidación creada", payload=comando), 200

    registrar_background_tasks(
        dispatchers=[despachadores.LiquidacionFinalizadaDispatcher()],
        subscriptors=[consumidores.PagoSolicitadoSuscripcion()]
    )

    logging.info("🚀 Aplicación Liquidaciones iniciada v2")

    return app
