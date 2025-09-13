from __future__ import annotations
from dataclasses import dataclass

from atribuciones.seedwork.dominio.eventos import EventoDominio


@dataclass
class AtribucionAgregada(EventoDominio):
    id_programa: str = None
    id_atribucion: str = None
    monto: float = None
    moneda: str = None


@dataclass
class ProgramaCompletado(EventoDominio):
    id_programa: str = None
    id_socio: str = None


@dataclass
class ProgramaReabierto(EventoDominio):
    id_programa: str = None
    id_socio: str = None
