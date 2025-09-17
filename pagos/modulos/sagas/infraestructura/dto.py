from pagos.config.db import db


Base = db.declarative_base()


class SagaPagoAtribucionDto(db.Model):
    __tablename__ = "saga_pago_atribuciones"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_correlacion = db.Column(db.String, nullable=False, index=True)
    nombre = db.Column(db.String, nullable=False)
    tipo_mensaje = db.Column(db.String, nullable=False)
