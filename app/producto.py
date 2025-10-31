
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Producto:
   
    nombre: str
    precio: float

    def __post_init__(self):  
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")

   
        try:
            precio = float(self.precio)
        except (TypeError, ValueError) as exc:
            raise ValueError("El precio debe ser un número.") from exc

        if not math.isfinite(precio):
            raise ValueError("El precio debe ser un número finito.")

        if precio <= 0:
            raise ValueError("El precio debe ser positivo.")
