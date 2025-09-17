from abc import ABC


class PasarelaPagosService(ABC):
    def esta_disponible(self):
        raise NotImplementedError
