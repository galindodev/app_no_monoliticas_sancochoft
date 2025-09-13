import uuid
from flask import Blueprint, request

from alianzas_bff.infraestructura import utils
from alianzas_bff.infraestructura.despachadores import Despachador


bp = Blueprint("atribuciones", __name__, url_prefix="/atribuciones")


@bp.post("/")
def agregar_atribucion():
    payload = dict(
        id_programa=request.json.get('id_programa'),
        evento=request.json.get('evento'),
        monto=request.json.get('monto'),
        moneda=request.json.get('moneda'),
    )
    comando = dict(
        id=str(uuid.uuid4()),
        time=utils.time_millis(),
        specversion="v1",
        type="ComandoAgregarAtribucion",
        ingestion=utils.time_millis(),
        datacontenttype="AVRO",
        service_name="alianzas-bff",
        data=payload,
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, topico="comandos-atribuciones")
    return dict(message="Solicitud de atribución enviada.", payload=payload), 202
