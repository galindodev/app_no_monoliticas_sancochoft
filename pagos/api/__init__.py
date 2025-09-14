import os

from flask import Flask, jsonify
from flask_swagger import swagger


# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import pagos.modulos.pagos.aplicacion


def importar_modelos_alchemy():
    import pagos.modulos.pagos.infraestructura.dto


def configure_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'.format(
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        db=os.getenv('POSTGRES_DB')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from pagos.config.db import init_db

    init_db(app)
    importar_modelos_alchemy()

    return app


def create_app():
    configuracion = {}
    app = configure_app(configuracion)

    from pagos.config.db import db

    registrar_handlers()

    with app.app_context():
        db.create_all()

    # Importa Blueprints
    from . import pagos

    # Registro de Blueprints
    app.register_blueprint(pagos.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return { "status": "up", "app": app.name }

    return app
