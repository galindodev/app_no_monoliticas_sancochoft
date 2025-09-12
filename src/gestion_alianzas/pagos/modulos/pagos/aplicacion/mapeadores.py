import uuid

from pagos.seedwork.aplicacion.dto import Mapeador as AppMap
from pagos.seedwork.dominio.repositorios import Mapeador as RepMap

from pagos.modulos.pagos.dominio.entidades import Pago
from pagos.modulos.pagos.dominio.objetos_valor import Monto, EstadoPago

from .dto import PagoDTO


class MapeadorPago(RepMap):
    def obtener_tipo(self) -> type:
        return Pago.__class__

    def entidad_a_dto(self, entidad: Pago) -> PagoDTO:
        id_influencer = str(entidad.id_influencer)
        monto = entidad.monto.valor
        return PagoDTO(id_influencer, monto, estado=entidad.estado.value)

    def dto_a_entidad(self, dto: PagoDTO) -> Pago:
        pago = Pago()
        pago.id_influencer = uuid.UUID(dto.id_influencer)
        pago.monto = Monto(dto.monto)
        pago.estado = EstadoPago[dto.estado]
        return pago


class MapeadorPagoDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> PagoDTO:
        pago_dto = PagoDTO(
            id_influencer=externo.get("id_influencer", None),
            monto=float(externo.get("monto", None)),
            estado=None,
        )
        return pago_dto

    def dto_a_externo(self, dto: PagoDTO) -> dict:
        return dto.__dict__


    def dtos_a_externos(self, dtos: list[PagoDTO]) -> list[dict]:
        return [self.dto_a_externo(dto) for dto in dtos]
