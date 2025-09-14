""" Mapeadores para la capa de infrastructura del dominio de pagos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

import uuid

from pagos.seedwork.dominio.repositorios import Mapeador

from pagos.modulos.pagos.dominio.entidades import Pago
from pagos.modulos.pagos.dominio.objetos_valor import Monto, EstadoPago

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
        pago_dto.estado = str(entidad.estado.name)
        pago_dto.id_programa = str(entidad.id_programa)
        return pago_dto

    def dto_a_entidad(self, dto: PagoDTO) -> Pago:
        pago = Pago(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)

        pago._id = uuid.UUID(dto.id)
        pago.id_influencer = uuid.UUID(dto.id_influencer)
        pago.monto = Monto(dto.monto)
        pago.estado = EstadoPago[dto.estado]
        pago.id_programa = uuid.UUID(dto.id_programa)

        return pago
