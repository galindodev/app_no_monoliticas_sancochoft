from flask import Blueprint


bp = Blueprint("pagos", __name__, url_prefix="/pagos")


@bp.post("/")
def solicitar_pago():
    return "OK"
