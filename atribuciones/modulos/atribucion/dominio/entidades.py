"""Entidades del dominio de atribucion

En este archivo usted encontrará las entidades del dominio de atribucion
"""
from __future__ import annotations
from dataclasses import dataclass, field
from uuid import UUID

from atribuciones.seedwork.dominio.entidades import AgregacionRaiz, Entidad

from .objetos_valor import Dinero, EstadoAtribucion, EventoAtribucion
from .eventos import AtribucionAgregada, ProgramaCompletado, ProgramaReabierto


@dataclass
class ProgramaAtribucion(AgregacionRaiz):
    id_socio: UUID = field(default=None)
    atribuciones: list[Atribucion] = field(default_factory=list)

    def agregar(self, atribucion: Atribucion):
        self.atribuciones.append(atribucion)
        evento = AtribucionAgregada(
            id_programa=str(self.id),
            id_atribucion=str(atribucion.id),
            monto=atribucion.dinero.monto,
            moneda=atribucion.dinero.moneda
        )
        self.agregar_evento(evento)

    def completar(self):
        for atribucion in self.atribuciones:
            atribucion.estado = EstadoAtribucion.VALIDADA

        evento = ProgramaCompletado(
            id_programa=str(self.id),
            id_socio=str(self.id_socio),
        )
        self.agregar_evento(evento)

    def reabrir(self):
        for atribucion in self.atribuciones:
            atribucion.estado = EstadoAtribucion.PENDIENTE

        evento = ProgramaReabierto(
            id_programa=str(self.id),
            id_socio=str(self.id_socio),
        )
        self.agregar_evento(evento)


@dataclass
class Atribucion(Entidad):
    estado: EstadoAtribucion = field(default=None)
    evento: EventoAtribucion = field(default=None)
    dinero: Dinero = field(default=None)
