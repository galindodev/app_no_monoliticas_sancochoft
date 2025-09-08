import json

from flask import request, Response

from alpespartners.modulos.pagos.aplicacion.queries.obtener_pagos_pendientes import ObtenerPagosPendientes
from alpespartners.seedwork.aplicacion.queries import ejecutar_query
import alpespartners.seedwork.presentacion.api as api
from alpespartners.seedwork.dominio.excepciones import ExcepcionDominio

from alpespartners.modulos.pagos.aplicacion.mapeadores import MapeadorPagoDTOJson

from alpespartners.modulos.pagos.aplicacion.comandos.solicitar_pago import SolicitarPago
from alpespartners.modulos.pagos.infraestructura.despachadores import Despachador


bp = api.crear_blueprint('pagos', '/pagos')


@bp.route('/solicitar-pago-comando', methods=('POST',))
def solicitar_pago_asincrona():
    try:
        solicitud_dict = request.json

        map_solicitud = MapeadorPagoDTOJson()
        solicitud_dto = map_solicitud.externo_a_dto(solicitud_dict)

        comando = SolicitarPago(id_influencer=solicitud_dto.id_influencer, monto=solicitud_dto.monto)

        despachador = Despachador()
        despachador.publicar_comando(comando, topico='comandos-pagos')

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/obtener-pagos-pendientes', methods=('GET',))
def obtener_pagos_pendientes():
    try:
        query_resultado = ejecutar_query(ObtenerPagosPendientes())
        map_pagos = MapeadorPagoDTOJson()
        pendientes = map_pagos.dtos_a_externos(query_resultado.resultado)
        return Response(json.dumps(pendientes), status=200, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
