import os
import uuid

from flask import Flask


def importar_modelos_alchemy():
    import atribuciones.modulos.atribucion.infraestructura.dto


def create_app(name: str):
    app = Flask(name)

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
    from atribuciones.config.db import init_db

    init_db(app)
    importar_modelos_alchemy()

    from atribuciones.config.db import db

    with app.app_context():
        db.create_all()

    return app
