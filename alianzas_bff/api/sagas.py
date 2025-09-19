import os

import requests
from flask import Blueprint


bp = Blueprint("sagas", __name__, url_prefix="/sagas")


@bp.get('/<string:id_correlacion>')
def obtener_sagas(id_correlacion):
    """Endpoint para obtener las sagas asociadas a un ID de correlación."""
    pagos_host = os.getenv("PAGOS_HOST", "pagos.ddd:5000")
    sagas_url = f"http://{pagos_host}/sagas/{id_correlacion}"
    response = requests.get(sagas_url, timeout=15)
    response.raise_for_status()
    return response.json(), 200
