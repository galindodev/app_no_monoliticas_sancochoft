import os

import requests
from flask import Blueprint, request


bp = Blueprint("programas", __name__, url_prefix="/programas")


@bp.post("/")
def agregar_programa():
    payload = dict(
        id_socio=request.json.get('id_socio'),
    )
    atribuciones_host = os.getenv("ATRIBUCIONES_HOST")
    programas_url = f"http://{atribuciones_host}/programas"
    response = requests.post(programas_url, json=payload, timeout=15)
    response.raise_for_status()

    result = dict(payload=payload, response=response.json())

    return result, response.status_code


@bp.get('/<string:id_programa>')
def obtener_atribuciones(id_programa):
    """Endpoint para obtener una atribución por ID de programa."""
    atribuciones_host = os.getenv("ATRIBUCIONES_HOST")
    atribuciones_url = f"http://{atribuciones_host}/atribuciones/{id_programa}"
    json = requests.get(atribuciones_url, timeout=15).json()
    return json, 200
