
from atribuciones.seedwork.dominio.repositorios import Mapeador as RepMap

from atribuciones.modulos.atribucion.dominio.entidades import Atribucion
from atribuciones.modulos.atribucion.dominio.objetos_valor import Dinero, EstadoAtribucion, EventoAtribucion

from .dto import AtribucionDTO


class MapeadorAtribucion(RepMap):
    def obtener_tipo(self) -> type:
        return Atribucion.__class__

    def entidad_a_dto(self, entidad: Atribucion) -> AtribucionDTO:
        estado = entidad.estado.value
        evento = entidad.evento.value
        monto = entidad.dinero.monto
        moneda = entidad.dinero.moneda

        return AtribucionDTO(
            estado=estado,
            evento=evento,
            monto=monto,
            moneda=moneda
        )

    def dto_a_entidad(self, dto: AtribucionDTO) -> Atribucion:
        atribucion = Atribucion()

        atribucion.estado = EstadoAtribucion[dto.estado]
        atribucion.evento = EventoAtribucion[dto.evento]
        atribucion.dinero = Dinero(dto.monto, dto.moneda)

        return atribucion
