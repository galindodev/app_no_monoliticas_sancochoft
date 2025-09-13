""" Mapeadores para la capa de infrastructura del dominio de pagos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

import uuid

from atribuciones.modulos.atribucion.dominio.objetos_valor import Dinero, EstadoAtribucion, EventoAtribucion
from atribuciones.seedwork.dominio.repositorios import Mapeador

from atribuciones.modulos.atribucion.dominio.entidades import ProgramaAtribucion, Atribucion

from .dto import AtribucionesDTO, ProgramaAtribucionesDTO


class MapeadorProgramaAtribucion(Mapeador):
    def __init__(self):
        self.mapeador_atribucion = MapeadorAtribuciones()

    def obtener_tipo(self) -> type:
        return ProgramaAtribucion.__class__

    def entidad_a_dto(self, entidad: ProgramaAtribucion) -> ProgramaAtribucionesDTO:
        dto = ProgramaAtribucionesDTO()
        dto.id = str(entidad.id)
        dto.fecha_creacion = entidad.fecha_creacion
        dto.fecha_actualizacion = entidad.fecha_actualizacion
        dto.id_socio = str(entidad.id_socio)

        # Mapear las atribuciones asociadas
        dtos_atribuciones = []
        for atribucion in entidad.atribuciones:
            dto_atribucion = self.mapeador_atribucion.entidad_a_dto(atribucion)
            dtos_atribuciones.append(dto_atribucion)
        dto.atribuciones = dtos_atribuciones

        return dto

    def dto_a_entidad(self, dto: ProgramaAtribucionesDTO) -> ProgramaAtribucion:
        programa = ProgramaAtribucion(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        programa._id = uuid.UUID(dto.id)
        programa.id_socio = uuid.UUID(dto.id_socio)

        for atribucion_dto in dto.atribuciones:
            atribucion = self.mapeador_atribucion.dto_a_entidad(atribucion_dto)
            programa.atribuciones.append(atribucion)

        return programa


class MapeadorAtribuciones(Mapeador):
    def obtener_tipo(self) -> type:
        return Atribucion.__class__

    def entidad_a_dto(self, entidad: Atribucion) -> AtribucionesDTO:
        dto = AtribucionesDTO()
        dto.id = str(entidad.id)
        dto.fecha_creacion = entidad.fecha_creacion
        dto.fecha_actualizacion = entidad.fecha_actualizacion

        dto.estado = entidad.estado.value
        dto.evento = entidad.evento.value
        dto.monto = entidad.dinero.monto
        dto.moneda = entidad.dinero.moneda

        return dto

    def dto_a_entidad(self, dto: AtribucionesDTO) -> Atribucion:
        atribucion = Atribucion(
            id=uuid.UUID(dto.id),
            estado=EstadoAtribucion[dto.estado.name],
            evento=EventoAtribucion[dto.evento.name],
            dinero=Dinero(monto=dto.monto, moneda=dto.moneda)
        )
        atribucion._id = uuid.UUID(dto.id)
        return atribucion
