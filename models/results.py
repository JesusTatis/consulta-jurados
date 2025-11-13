from dataclasses import dataclass
from typing import Optional

@dataclass
class ConsultaResult:
    exito: bool
    mensaje: str
    es_jurado: Optional[bool] = None
    detalle: Optional[str] = None
    cedula: Optional[str] = None
    
    def __post_init__(self):
        if self.es_jurado is None and self.exito:
            self.es_jurado = False