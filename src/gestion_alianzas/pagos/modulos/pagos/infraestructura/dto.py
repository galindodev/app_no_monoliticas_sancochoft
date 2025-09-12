"""DTOs para la capa de infrastructura del dominio de pagos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos
"""

from pagos.config.db import db
from pagos.modulos.pagos.dominio.objetos_valor import EstadoPago


Base = db.declarative_base()


class Pago(db.Model):
    __tablename__ = "pagos"
    id = db.Column(db.String, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    id_influencer = db.Column(db.String, nullable=True, index=True)
    monto = db.Column(db.Float, nullable=False)
    estado = db.Column(db.Enum(EstadoPago), nullable=False)
