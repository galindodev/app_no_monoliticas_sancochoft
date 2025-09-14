import logging

from flask import Flask

from . import pagos
from . import atribuciones
from . import programas

app = Flask("Alianzas BFF")

app.register_blueprint(pagos.bp)
app.register_blueprint(atribuciones.bp)
app.register_blueprint(programas.bp)


@app.route("/health")
def health():
    return {"status": "up", "app": app.name}


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    logging.basicConfig(level=gunicorn_logger.level)
