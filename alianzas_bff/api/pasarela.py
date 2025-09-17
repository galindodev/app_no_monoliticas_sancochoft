from flask import current_app as app
from flask import Blueprint


bp = Blueprint("pasarela", __name__, url_prefix="/pasarela")


@bp.post("/permitir-pagos")
def permitir_pagos():
    app.config["PAGOS_PERMITIDOS"] = True
    app.logger.info("Pagos permitidos")
    return {"message": "Pagos permitidos"}, 200


@bp.post("/bloquear-pagos")
def bloquear_pagos():
    app.config["PAGOS_PERMITIDOS"] = False
    app.logger.info("Pagos bloqueados")
    return {"message": "Pagos bloqueados"}, 200


@bp.get("/estado-pagos")
def estado_pagos():
    estado = app.config.get("PAGOS_PERMITIDOS")
    app.logger.info(f"Estado de pagos consultado: {estado}")
    return {"pagos_permitidos": estado}, 200
