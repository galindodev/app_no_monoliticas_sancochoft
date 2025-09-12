""" Fábricas para la creación de objetos del dominio de pagos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de pagos

"""

from dataclasses import dataclass

from liquidaciones.seedwork.dominio.fabricas import Fabrica
from liquidaciones.seedwork.dominio.entidades import Entidad
from liquidaciones.seedwork.dominio.repositorios import Mapeador

from .entidades import Liquidacion
from .reglas import MontoPositivo


@dataclass
class FabricaLiquidacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            liquidacion: Liquidacion = mapeador.dto_a_entidad(obj)

            # Validaciones de reglas de negocio
            self.validar_regla(MontoPositivo(liquidacion.monto))

            return liquidacion
