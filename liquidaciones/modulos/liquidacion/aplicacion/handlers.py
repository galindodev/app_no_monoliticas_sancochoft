from liquidaciones.modulos.liquidacion.infraestructura.despachadores import LiquidacionFinalizadaDispatcher
from liquidaciones.seedwork.aplicacion.handlers import Handler

from liquidaciones.modulos.liquidacion.dominio.eventos import LiquidacionFinalizada


class HandlerLiquidacionIntegracion(Handler):
    @staticmethod
    def handle_liquidacion_finalizada(evento: LiquidacionFinalizada):
        dispatcher = LiquidacionFinalizadaDispatcher()
        dispatcher.handle(evento)
