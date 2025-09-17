import os
import requests
import logging

from liquidaciones.modulos.liquidacion.dominio.servicios import PasarelaPagosService


class PasarelaPagosServiceImpl(PasarelaPagosService):
    url = os.getenv("PASARELA_URL", "http://localhost:6000")

    def esta_disponible(self):
        response = requests.get(f"{self.url}/estado-pagos")
        response.raise_for_status()
        result = response.json()
        permitted = result.get("pagos_permitidos", False)
        logging.info(f"Pasarela de pagos disponible: {permitted}")
        return permitted
