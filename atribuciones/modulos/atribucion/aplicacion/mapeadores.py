import uuid

from atribuciones.seedwork.dominio.repositorios import Mapeador as RepMap

from atribuciones.modulos.atribucion.dominio.entidades import Atribucion, ProgramaAtribucion
from atribuciones.modulos.atribucion.dominio.objetos_valor import Dinero, EstadoAtribucion, EventoAtribucion

from .dto import AtribucionDTO, ProgramaAtribucionDTO


class MapeadorProgramaAtribucion(RepMap):
    def __init__(self):
        self.mapeador_atribucion = MapeadorAtribucion()

    def obtener_tipo(self) -> type:
        return ProgramaAtribucion.__class__

    def entidad_a_dto(self, entidad: ProgramaAtribucion) -> ProgramaAtribucionDTO:
        atribuciones = [self.mapeador_atribucion.entidad_a_dto(atr) for atr in entidad.atribuciones]

        return ProgramaAtribucionDTO(
            atribuciones=atribuciones,
            id_socio=str(entidad.id_socio),
        )

    def dto_a_entidad(self, dto: ProgramaAtribucionDTO) -> ProgramaAtribucion:
        programa = ProgramaAtribucion()
        programa.id_socio = uuid.UUID(dto.id_socio)

        programa.atribuciones = [self.mapeador_atribucion.dto_a_entidad(atr) for atr in dto.atribuciones]

        return programa


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
