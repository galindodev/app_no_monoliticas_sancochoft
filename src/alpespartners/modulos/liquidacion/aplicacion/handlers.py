from alpespartners.modulos.liquidacion.dominio.eventos import LiquidacionFinalizada
from alpespartners.modulos.liquidacion.infraestructura.despachadores import Despachador
from alpespartners.seedwork.aplicacion.handlers import Handler


class HandlerLiquidacionDominio(Handler):
    @staticmethod
    def handle_liquidacion_finalizada(evento: LiquidacionFinalizada):
        despachador = Despachador()
        despachador.publicar_evento(evento, topico='eventos-liquidaciones')
