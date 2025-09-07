""" Mapeadores para la capa de infrastructura del dominio de pagos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

import uuid

from alpespartners.seedwork.dominio.repositorios import Mapeador

from alpespartners.modulos.liquidacion.dominio.entidades import Liquidacion
from alpespartners.modulos.liquidacion.dominio.objetos_valor import Monto

from .dto import Liquidacion as LiquidacionDTO


class MapeadorLiquidacion(Mapeador):
    def obtener_tipo(self) -> type:
        return Liquidacion.__class__

    def entidad_a_dto(self, entidad: Liquidacion) -> LiquidacionDTO:
        liquidacion_dto = LiquidacionDTO()
        liquidacion_dto.id = str(entidad.id)
        liquidacion_dto.fecha_creacion = entidad.fecha_creacion
        liquidacion_dto.fecha_actualizacion = entidad.fecha_actualizacion
        liquidacion_dto.id_pago = str(entidad.id_pago)
        liquidacion_dto.id_influencer = str(entidad.id_influencer)
        liquidacion_dto.monto = float(entidad.monto.valor)

        return liquidacion_dto

    def dto_a_entidad(self, dto: LiquidacionDTO) -> Liquidacion:
        liquidacion = Liquidacion(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)

        liquidacion.pago = uuid.UUID(dto.pago)
        liquidacion.id_influencer = uuid.UUID(dto.id_influencer)
        liquidacion.monto = Monto(dto.monto)

        return liquidacion
