"""DTOs para la capa de infrastructura del dominio de liquidacion

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de liquidacion
"""

from liquidaciones.config.db import db


Base = db.declarative_base()


class Liquidacion(db.Model):
    __tablename__ = "liquidaciones"
    id = db.Column(db.String, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    id_pago = db.Column(db.String, nullable=False, index=True)
    id_influencer = db.Column(db.String, nullable=False, index=True)
    monto = db.Column(db.Float, nullable=False)
