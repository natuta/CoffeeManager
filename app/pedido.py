# app/pedido.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple

from .cliente import Cliente
from .producto import Producto


@dataclass
class Pedido:
    """Pedido con items (producto, cantidad) para un cliente."""

    cliente: Cliente
    items: List[Tuple[Producto, int]] = field(default_factory=list)

    def agregar_producto(self, producto: Producto, cantidad: int = 1) -> None:
        """Agrega un producto con cantidad >= 1. Si ya existe, acumula cantidad."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser al menos 1.")

        # Buscar si el producto ya existe para acumular la cantidad
        for i, (prod, cant) in enumerate(self.items):
            if prod == producto:
                self.items[i] = (prod, cant + cantidad)
                break
        else:
            # No se encontró: agregar nuevo ítem
            self.items.append((producto, cantidad))

    def quitar_producto(self, producto: Producto, cantidad: int | None = None) -> None:
        """
        Quita un producto o reduce su cantidad.
        Si cantidad es None, elimina el ítem completo.
        """
        for i, (prod, cant) in enumerate(self.items):
            if prod == producto:
                if cantidad is None or cantidad >= cant:
                    self.items.pop(i)
                elif cantidad > 0:
                    self.items[i] = (prod, cant - cantidad)
                else:
                    raise ValueError("La cantidad a quitar debe ser positiva.")
                return
        raise ValueError("El producto no está en el pedido.")

    def calcular_total(self) -> float:
        """Suma de precios * cantidades (subtotal)."""
        return float(sum(prod.precio * cant for prod, cant in self.items))
