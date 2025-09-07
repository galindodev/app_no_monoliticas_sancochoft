""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de pagos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de pagos

"""

from __future__ import annotations
from dataclasses import dataclass

from alpespartners.modulos.pagos.dominio.eventos import PagoSolicitado
from alpespartners.modulos.pagos.infraestructura.schema.v1.eventos import EventoDominioPagoSolicitado, EventoDominioPagoSolicitadoPayload
from alpespartners.seedwork.dominio.eventos import EventoDominio
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.repositorios import Repositorio
from alpespartners.seedwork.infraestructura.schema.v1.eventos import EventoDominio as EventoDominioInfra

from alpespartners.modulos.pagos.dominio.repositorios import RepositorioPagos

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioReservasSQLAlchemy


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type) -> Repositorio:
        if obj == RepositorioPagos.__class__:
            return RepositorioReservasSQLAlchemy()
        else:
            raise ExcepcionFabrica()

@dataclass
class FabricaEventosDominio:
    @staticmethod
    def crear_evento(evento: EventoDominio) -> EventoDominioInfra:
        if isinstance(evento, PagoSolicitado):
            return EventoDominioPagoSolicitado(
                data=EventoDominioPagoSolicitadoPayload(
                    id_pago=str(evento.id_pago),
                    id_influencer=str(evento.id_influencer),
                    monto=evento.monto
                )
            )
        else:
            raise ExcepcionFabrica("Evento de dominio no soportado en la fábrica de infraestructura.")
