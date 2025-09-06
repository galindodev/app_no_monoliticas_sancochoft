""" Mapeadores para la capa de infrastructura del dominio de pagos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

import uuid

from alpespartners.seedwork.dominio.repositorios import Mapeador

from alpespartners.modulos.pagos.dominio.entidades import Pago
from alpespartners.modulos.pagos.dominio.objetos_valor import Monto

from .dto import Pago as PagoDTO


class MapeadorPago(Mapeador):
    def obtener_tipo(self) -> type:
        return Pago.__class__

    def entidad_a_dto(self, entidad: Pago) -> PagoDTO:
        pago_dto = PagoDTO()
        pago_dto.id = str(entidad.id)
        pago_dto.fecha_creacion = entidad.fecha_creacion
        pago_dto.fecha_actualizacion = entidad.fecha_actualizacion
        pago_dto.id_influencer = str(entidad.id_influencer)
        pago_dto.monto = float(entidad.monto.valor)
        return pago_dto

    def dto_a_entidad(self, dto: PagoDTO) -> Pago:
        pago = Pago(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)

        pago.id_influencer = uuid.UUID(dto.id_influencer)
        pago.monto = Monto(dto.monto)

        return pago
