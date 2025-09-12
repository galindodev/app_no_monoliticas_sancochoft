import uuid

from liquidaciones.seedwork.dominio.repositorios import Mapeador as RepMap

from liquidaciones.modulos.liquidacion.dominio.entidades import Liquidacion
from liquidaciones.modulos.liquidacion.dominio.objetos_valor import Monto

from .dto import LiquidacionDTO


class MapeadorLiquidacion(RepMap):
    def obtener_tipo(self) -> type:
        return Liquidacion.__class__

    def entidad_a_dto(self, entidad: Liquidacion) -> LiquidacionDTO:
        id_pago = str(entidad.id_pago)
        id_influencer = str(entidad.id_influencer)
        monto = entidad.monto.valor
        return LiquidacionDTO(id_pago, id_influencer, monto)

    def dto_a_entidad(self, dto: LiquidacionDTO) -> Liquidacion:
        liquidacion = Liquidacion()
        liquidacion.id_pago = uuid.UUID(dto.id_pago)
        liquidacion.id_influencer = uuid.UUID(dto.id_influencer)
        liquidacion.monto = Monto(dto.monto)
        return liquidacion
