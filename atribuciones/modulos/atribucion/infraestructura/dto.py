"""DTOs para la capa de infrastructura del dominio de atribuciones

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos
"""

from atribuciones.config.db import db
from atribuciones.modulos.atribucion.dominio.objetos_valor import EstadoAtribucion, EventoAtribucion


Base = db.declarative_base()


class ProgramaAtribucionesDTO(db.Model):
    __tablename__ = "programa_atribuciones"
    id = db.Column(db.String, primary_key=True)
    id_socio = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)

    # Relación uno a muchos: un programa tiene muchas atribuciones
    atribuciones = db.relationship(
        "AtribucionesDTO",
        back_populates="programa",
        cascade="all, delete-orphan"
    )


class AtribucionesDTO(db.Model):
    __tablename__ = "atribuciones"
    id = db.Column(db.String, primary_key=True)

    estado = db.Column(db.Enum(EstadoAtribucion), nullable=False)
    evento = db.Column(db.Enum(EventoAtribucion), nullable=False)

    monto = db.Column(db.Float, nullable=False)
    moneda = db.Column(db.String, nullable=False)

    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)

    # Clave foránea para la relación con ProgramaAtribucionesDTO
    programa_id = db.Column(db.String, db.ForeignKey("programa_atribuciones.id"), nullable=False)
    programa = db.relationship("ProgramaAtribucionesDTO", back_populates="atribuciones")
