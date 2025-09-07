import uuid

from alpespartners.seedwork.aplicacion.dto import Mapeador as AppMap
from alpespartners.seedwork.dominio.repositorios import Mapeador as RepMap

from alpespartners.modulos.pagos.dominio.entidades import Pago
from alpespartners.modulos.pagos.dominio.objetos_valor import Monto, EstadoPago

from .dto import PagoDTO


class MapeadorPago(RepMap):
    def obtener_tipo(self) -> type:
        return Pago.__class__

    def entidad_a_dto(self, entidad: Pago) -> PagoDTO:
        id_influencer = str(entidad.id_influencer)
        monto = entidad.monto.valor
        return PagoDTO(id_influencer, monto)

    def dto_a_entidad(self, dto: PagoDTO) -> Pago:
        pago = Pago()
        pago._id = uuid.UUID(dto.id)
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

