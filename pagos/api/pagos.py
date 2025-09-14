import json

from flask import Response

from pagos.modulos.pagos.aplicacion.queries.obtener_pagos_pendientes import ObtenerPagosPendientes
from pagos.seedwork.aplicacion.queries import ejecutar_query
import pagos.seedwork.presentacion.api as api
from pagos.seedwork.dominio.excepciones import ExcepcionDominio

from pagos.modulos.pagos.aplicacion.mapeadores import MapeadorPagoDTOJson


bp = api.crear_blueprint('pagos', '/pagos')


@bp.route('/obtener-pagos-pendientes', methods=('GET',))
def obtener_pagos_pendientes():
    try:
        query_resultado = ejecutar_query(ObtenerPagosPendientes())
        map_pagos = MapeadorPagoDTOJson()
        pendientes = map_pagos.dtos_a_externos(query_resultado.resultado)
        return Response(json.dumps(pendientes), status=200, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
