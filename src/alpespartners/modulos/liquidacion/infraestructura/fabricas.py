""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de liquidacion

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de liquidacion

"""

from __future__ import annotations
from dataclasses import dataclass

from alpespartners.modulos.liquidacion.dominio.eventos import LiquidacionFinalizada
from alpespartners.modulos.liquidacion.infraestructura.schema.v1.eventos import EventoDominioLiquidacionFinalizada, EventoDominioLiquidacionFinalizadaPayload
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.repositorios import Repositorio
from alpespartners.seedwork.infraestructura.schema.v1.eventos import EventoDominio as EventoDominioInfra

from alpespartners.modulos.liquidacion.dominio.repositorios import RepositorioLiquidacion
from alpespartners.seedwork.infraestructura.schema.v1.eventos import EventoDominio

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioLiquidacionesSQLAlchemy


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type) -> Repositorio:
        if obj == RepositorioLiquidacion.__class__:
            return RepositorioLiquidacionesSQLAlchemy()
        else:
            raise ExcepcionFabrica()


@dataclass
class FabricaEventosDominio:
    @staticmethod
    def crear_evento(evento: EventoDominio) -> EventoDominioInfra:
        if isinstance(evento, LiquidacionFinalizada):
            return EventoDominioLiquidacionFinalizada(
                data=EventoDominioLiquidacionFinalizadaPayload(
                    id_pago=str(evento.id_pago),
                    id_liquidacion=str(evento.id_liquidacion),
                    pagado=evento.pagado
                )
            )
        else:
            raise ExcepcionFabrica("Evento de dominio no soportado en la fábrica de infraestructura.")
