import uuid
from flask import Blueprint, request

from alianzas_bff.infraestructura import utils
from alianzas_bff.infraestructura.despachadores import Despachador


bp = Blueprint("pagos", __name__, url_prefix="/pagos")


@bp.post("/")
def solicitar_pago():
    payload = dict(
        id_influencer=request.json.get('id_influencer'),
        monto=request.json.get('monto'),
    )
    comando = dict(
        id=str(uuid.uuid4()),
        time=utils.time_millis(),
        specversion="v1",
        type="ComandoSolicitarPago",
        ingestion=utils.time_millis(),
        datacontenttype="AVRO",
        service_name="alianzas-bff",
        data=payload,
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, topico="comandos-pagos")
    return dict(message="Solicitud de pago enviada.", payload=payload), 202
