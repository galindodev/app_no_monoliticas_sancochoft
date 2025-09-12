"""Entidades reusables parte del seedwork del proyecto

En este archivo usted encontrará las clases para eventos reusables parte del seedwork del proyecto

"""

import uuid
from datetime import datetime
from dataclasses import dataclass, field

from .reglas import IdEntidadEsInmutable
from .excepciones import IdDebeSerInmutableExcepcion


@dataclass
class EventoDominio():
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    fecha_evento: datetime =  field(default=datetime.now())


    @classmethod
    def siguiente_id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not IdEntidadEsInmutable(self).es_valido():
            raise IdDebeSerInmutableExcepcion()
        self._id = self.siguiente_id()
