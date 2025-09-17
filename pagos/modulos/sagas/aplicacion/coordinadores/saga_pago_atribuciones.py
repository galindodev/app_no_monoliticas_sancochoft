from pagos.modulos.sagas.infraestructura.dto import SagaPagoAtribucionDto
from pagos.modulos.sagas.infraestructura.fabricas import FabricaRepositorio
from pagos.seedwork.infraestructura.uow import UnidadTrabajoPuerto


class SagaPagoAtribucionesCoreador:
    """Este coreador no tiene mucho por hacer. Solo persiste el mensaje recibido en la base de datos.
       Los eventos de compensacion y confirmacion son manejados por la misma coreografía en los
       microservicios respectivos.
    """
    def __init__(self):
        self.repositorio = FabricaRepositorio().crear_objeto()

    def procesar(self, mensaje):
        dto = SagaPagoAtribucionDto()
        dto.id_correlacion = mensaje['id_correlacion']
        dto.nombre = mensaje['nombre']
        dto.tipo_mensaje = mensaje['tipo_mensaje']
        self.repositorio.agregar(dto)
        UnidadTrabajoPuerto.commit()
