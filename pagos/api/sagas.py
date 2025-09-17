import json

from flask import Response

from pagos.modulos.sagas.aplicacion.queries.obtener_pagos_pendientes import ObtenerTransaccionesPago
from pagos.seedwork.aplicacion.queries import ejecutar_query
import pagos.seedwork.presentacion.api as api
from pagos.seedwork.dominio.excepciones import ExcepcionDominio


bp = api.crear_blueprint('sagas', '/sagas')


@bp.get('/<id_correlacion>')
def obtener_pagos_pendientes(id_correlacion):
    try:
        query_resultado = ejecutar_query(ObtenerTransaccionesPago(id_correlacion=id_correlacion))
        return Response(json.dumps(query_resultado.resultado), status=200, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
