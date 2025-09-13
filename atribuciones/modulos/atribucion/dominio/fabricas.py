""" Fábricas para la creación de objetos del dominio de pagos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de pagos

"""

from dataclasses import dataclass

from atribuciones.seedwork.dominio.fabricas import Fabrica
from atribuciones.seedwork.dominio.entidades import Entidad
from atribuciones.seedwork.dominio.repositorios import Mapeador

from .reglas import DineroPositivo
from .entidades import ProgramaAtribucion, Atribucion


@dataclass
class FabricaProgramaAtribucion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            programa_atribucion: ProgramaAtribucion = mapeador.dto_a_entidad(obj)
            return programa_atribucion


@dataclass
class FabricaAtribucion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            atribucion: Atribucion = mapeador.dto_a_entidad(obj)

            # Validaciones de reglas de negocio
            self.validar_regla(DineroPositivo(atribucion.dinero))

            return atribucion
