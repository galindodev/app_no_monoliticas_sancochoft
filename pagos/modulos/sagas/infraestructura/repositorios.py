from pagos.config.db import db


from .dto import SagaPagoAtribucionDto


class RepositorioSagaAtribucionesSQLAlchemy:
    def obtener_por_id(self, id_correlacion: str) -> list[SagaPagoAtribucionDto]:
        return db.session.query(SagaPagoAtribucionDto).filter_by(id_correlacion=id_correlacion).all()

    def agregar(self, dto: SagaPagoAtribucionDto):
        db.session.add(dto)
