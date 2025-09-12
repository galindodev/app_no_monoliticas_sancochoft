""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de pagos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de pagos

"""

from __future__ import annotations
from dataclasses import dataclass

from pagos.modulos.pagos.dominio.eventos import PagoSolicitado
from pagos.modulos.pagos.infraestructura.schema.v1.eventos import EventoDominioPagoSolicitado, EventoDominioPagoSolicitadoPayload
from pagos.seedwork.dominio.eventos import EventoDominio
from pagos.seedwork.dominio.fabricas import Fabrica
from pagos.seedwork.dominio.repositorios import Repositorio
from pagos.seedwork.infraestructura.schema.v1.eventos import EventoDominio as EventoDominioInfra

from pagos.modulos.pagos.dominio.repositorios import RepositorioPagos

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioPagosSQLAlchemy


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type) -> Repositorio:
        if obj == RepositorioPagos.__class__:
            return RepositorioPagosSQLAlchemy()
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
