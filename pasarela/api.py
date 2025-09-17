import logging
from flask import Flask


app = Flask("Pasarela API")
app.config['PAGOS_PERMITIDOS'] = False


logger = logging.getLogger("gunicorn.error")
logging.basicConfig(level=logger.level)
app.logger.setLevel(logger.level)


@app.route("/health")
def health():
    return { "status": "up", "app": app.name }


@app.post('/permitir-pagos')
def permitir_pagos():
    app.config['PAGOS_PERMITIDOS'] = True
    logger.info("Pagos permitidos")
    return {"message": "Pagos permitidos"}, 200


@app.post('/bloquear-pagos')
def bloquear_pagos():
    app.config['PAGOS_PERMITIDOS'] = False
    logger.info("Pagos bloqueados")
    return {"message": "Pagos bloqueados"}, 200


@app.get('/estado-pagos')
def estado_pagos():
    estado = app.config.get('PAGOS_PERMITIDOS')
    logger.info(f"Estado de pagos consultado: {estado}")
    return {"pagos_permitidos": estado}, 200
