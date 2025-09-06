import uuid

from alpespartners.seedwork.dominio.repositorios import Mapeador as RepMap

from alpespartners.modulos.pagos.dominio.entidades import Pago
from alpespartners.modulos.pagos.dominio.objetos_valor import Monto

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
        pago.id_influencer = uuid.UUID(dto.id_influencer)
        pago.monto = Monto(dto.monto)
        return pago
