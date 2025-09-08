import os

from flask import Flask, jsonify
from flask_swagger import swagger


# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import alpespartners.modulos.pagos.aplicacion
    import alpespartners.modulos.liquidacion.aplicacion


def importar_modelos_alchemy():
    import alpespartners.modulos.pagos.infraestructura.dto
    import alpespartners.modulos.liquidacion.infraestructura.dto


def comenzar_consumidor():
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """
    import threading
    import alpespartners.modulos.pagos.infraestructura.consumidores as pagos
    import alpespartners.modulos.liquidacion.infraestructura.consumidores as liquidacion

    # Suscripción a eventos
    threading.Thread(target=pagos.suscribirse_a_eventos).start()
    threading.Thread(target=liquidacion.suscribirse_a_eventos).start()

    # Suscripción a comandos
    threading.Thread(target=pagos.suscribirse_a_comandos).start()
    threading.Thread(target=liquidacion.suscribirse_a_comandos).start()


def configure_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'.format(
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', 5433),
        db=os.getenv('DB_NAME', 'pagos')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from alpespartners.config.db import init_db

    init_db(app)
    importar_modelos_alchemy()

    return app


def create_app(configuracion={}):
    app = configure_app(configuracion)

    from alpespartners.config.db import db

    registrar_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor()

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
        return { "status": "up" }

    return app
