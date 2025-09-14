import json
import logging

from flask import request, Response

from atribuciones.modulos.atribucion.aplicacion.comandos.agregar_atribucion import AgregarAtribucion
from atribuciones.modulos.atribucion.aplicacion.comandos.agregar_programa import AgregarPrograma
from atribuciones.modulos.atribucion.aplicacion.queries.obtener_atribuciones import ObtenerAtribuciones
from atribuciones.seedwork.aplicacion.queries import ejecutar_query
from atribuciones.seedwork.dominio.excepciones import ExcepcionDominio
from atribuciones.seedwork.aplicacion.comandos import ejecutar_commando


from .app import create_app


app = create_app("Atribuciones")


@app.route("/health")
def health():
    return {"status": "up", "app": app.name}


@app.post("/atribuciones")
def agregar_atribucion():
    """Endpoint de prueba para agregar una atribución."""
    comando = AgregarAtribucion(**request.json)
    ejecutar_commando(comando)
    return dict(message="Atribución agregada", payload=comando), 200


@app.get('/atribuciones/<string:id_programa>')
def obtener_atribuciones(id_programa):
    """Endpoint para obtener una atribución por ID de programa."""
    obtener_atribuciones = ObtenerAtribuciones(id_programa=id_programa)
    ejecucion_query = ejecutar_query(obtener_atribuciones)
    return ejecucion_query.resultado.__dict__, 200


@app.post('/programas')
def agregar_programa():
    """Endpoint para agregar un programa."""
    comando = AgregarPrograma(id_socio=request.json.get('id_socio'))
    id_programa = ejecutar_commando(comando)
    result = dict(id_programa=id_programa)
    return dict(message="Programa agregado", payload=comando, result=result), 200


@app.errorhandler(ExcepcionDominio)
def handle_dominio_exception(error):
    logging.error(f"Excepción de dominio: {error}")
    result = json.dumps(dict(error=str(error)))
    return Response(result, status=400, mimetype="application/json")


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    logging.basicConfig(level=gunicorn_logger.level)
