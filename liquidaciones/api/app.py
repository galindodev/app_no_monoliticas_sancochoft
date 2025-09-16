import json
import os
from threading import Thread
import uuid
import logging

from flask import Flask, Response

from liquidaciones.seedwork.dominio.excepciones import ExcepcionDominio
from liquidaciones.seedwork.infraestructura.utils import register_esquemas


def importar_modelos_alchemy():
    import liquidaciones.modulos.liquidacion.infraestructura.dto


def escuchar_mensaje(subscriptor):
    subscriptor.subscribe()


def create_app(name: str) -> Flask:
    app = Flask(name)

    app.logger.setLevel(os.getenv('LOG_LEVEL', 'WARNING'))
    logging.basicConfig(level=app.logger.level)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            db=os.getenv("POSTGRES_DB"),
        )
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.secret_key = os.getenv("SECRET_KEY", str(uuid.uuid4()))
    app.config["TESTING"] = os.getenv("TESTING")

    # Inicializa la DB
    from liquidaciones.config.db import init_db

    init_db(app)
    importar_modelos_alchemy()

    from liquidaciones.config.db import db

    with app.app_context():
        db.create_all()

    @app.route("/health")
    def health():
        return {"status": "up", "app": app.name}

    @app.errorhandler(ExcepcionDominio)
    def handle_dominio_exception(error):
        logging.error(f"Excepción de dominio: {error}")
        result = json.dumps(dict(error=str(error)))
        return Response(result, status=400, mimetype="application/json")

    return app


def registrar_background_tasks(dispatchers, subscriptors):
    for dispatcher in dispatchers:
        register_esquemas(dispatcher)

    for subscriptor in subscriptors:
        Thread(target=escuchar_mensaje, args=(subscriptor,), daemon=True).start()
