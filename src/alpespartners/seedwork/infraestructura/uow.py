from abc import ABC, abstractmethod
from enum import Enum

from alpespartners.seedwork.dominio.entidades import AgregacionRaiz
from pydispatch import dispatcher

import pickle


class Lock(Enum):
    OPTIMISTA = 1
    PESIMISTA = 2

class Batch:
    def __init__(self, operacion, lock: Lock, *args, **kwargs):
        self.operacion = operacion
        self.args = args
        self.lock = lock
        self.kwargs = kwargs

class UnidadTrabajo(ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def _obtener_eventos(self, batches=None):
        batches = self.batches if batches is None else batches
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    return arg.eventos
        return list()

    @abstractmethod
    def _limpiar_batches(self):
        raise NotImplementedError

    @abstractmethod
    def batches(self) -> list[Batch]:
        raise NotImplementedError

    @abstractmethod
    def savepoints(self) -> list:
        raise NotImplementedError

    def commit(self):
        self._publicar_eventos_post_commit()
        self._limpiar_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        self._limpiar_batches()

    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    def registrar_batch(self, operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        batch = Batch(operacion, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publicar_eventos_dominio(batch)

    def _publicar_eventos_dominio(self, batch):
        for evento in self._obtener_eventos(batches=[batch]):
            dispatcher.send(signal=f'{type(evento).__name__}Dominio', evento=evento)

    def _publicar_eventos_post_commit(self):
        for evento in self._obtener_eventos():
            dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)

def is_flask():
    try:
        from flask import session
        return True
    except Exception as e:
        return False

def registrar_unidad_de_trabajo(serialized_obj):
    from alpespartners.config.uow import UnidadTrabajoSQLAlchemy
    from flask import session


    session['uow'] = serialized_obj

def flask_uow():
    from flask import session
    from alpespartners.config.uow import UnidadTrabajoSQLAlchemy
    if session.get('uow'):
        return session['uow']
    else:
        uow_serialized = pickle.dumps(UnidadTrabajoSQLAlchemy())
        registrar_unidad_de_trabajo(uow_serialized)
        return uow_serialized

def unidad_de_trabajo() -> UnidadTrabajo:
    if is_flask():
        return pickle.loads(flask_uow())
    else:
        raise Exception('No hay unidad de trabajo')

def guardar_unidad_trabajo(uow: UnidadTrabajo):
    if is_flask():
        registrar_unidad_de_trabajo(pickle.dumps(uow))
    else:
        raise Exception('No hay unidad de trabajo')


class UnidadTrabajoPuerto:
    _uow_sqlalchemy = None

    @staticmethod
    def _get_uow():
        if UnidadTrabajoPuerto._uow_sqlalchemy is None:
            from alpespartners.config.uow import UnidadTrabajoSQLAlchemy
            UnidadTrabajoPuerto._uow_sqlalchemy = UnidadTrabajoSQLAlchemy()
        return UnidadTrabajoPuerto._uow_sqlalchemy

    @staticmethod
    def commit():
        uow = UnidadTrabajoPuerto._get_uow()
        try:
            uow.commit()
        except:
            uow.rollback()
        finally:
            UnidadTrabajoPuerto._uow_sqlalchemy = None

    @staticmethod
    def rollback(savepoint=None):
        uow = UnidadTrabajoPuerto._get_uow()
        uow.rollback(savepoint=savepoint)
        UnidadTrabajoPuerto._uow_sqlalchemy = None

    @staticmethod
    def savepoint():
        uow = UnidadTrabajoPuerto._get_uow()
        uow.savepoint()

    @staticmethod
    def dar_savepoints():
        uow = UnidadTrabajoPuerto._get_uow()
        return uow.savepoints()

    @staticmethod
    def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        uow = UnidadTrabajoPuerto._get_uow()
        uow.registrar_batch(operacion, *args, lock=lock, **kwargs)


class UnidadTrabajoMemoria(UnidadTrabajo):
    def __init__(self):
        self._batches = []
        self._savepoints = []

    def _limpiar_batches(self):
        self._batches.clear()

    @property
    def batches(self) -> list[Batch]:
        return self._batches

    @property
    def savepoints(self) -> list:
        return self._savepoints

    def rollback(self, savepoint=None):
        self._limpiar_batches()
        if savepoint:
            self._savepoints = [sp for sp in self._savepoints if sp != savepoint]

    def savepoint(self):
        count = len(self._savepoints) + 1
        savepoint_name = f"savepoint_{count}"
        self._savepoints.append(savepoint_name)
        return savepoint_name

    def commit(self):
        # Ejecuta las operaciones de los batches
        for batch in self._batches:
            batch.operacion(*batch.args, **batch.kwargs)
        self._publicar_eventos_post_commit()
        self._limpiar_batches()
