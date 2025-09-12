import logging
from .app import create_app


app = create_app("Liquidaciones")


@app.route("/health")
def health():
    return {"status": "up"}


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
