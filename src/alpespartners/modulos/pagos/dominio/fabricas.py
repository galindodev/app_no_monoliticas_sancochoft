""" Fábricas para la creación de objetos del dominio de pagos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de pagos

"""

from dataclasses import dataclass

from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.entidades import Entidad
from alpespartners.seedwork.dominio.repositorios import Mapeador

from .entidades import Pago
from .reglas import MontoPositivo


@dataclass
class FabricaPagos(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            pago: Pago = mapeador.dto_a_entidad(obj)

            # Validaciones de reglas de negocio
            self.validar_regla(MontoPositivo(pago.monto))

            return pago

    def create_muchos_objetos(self, objs: list[any], mapeador: Mapeador) -> list[any]:
        return [self.crear_objeto(obj, mapeador) for obj in objs]
