from .pedido import Pedido


IVA_BOLIVIA = 0.13




def calcular_subtotal(pedido: Pedido) -> float:


    return float(pedido.calcular_total())




def calcular_iva(subtotal: float, tasa: float = IVA_BOLIVIA) -> float:
    if subtotal < 0:
      raise ValueError("El subtotal no puede ser negativo.")
    if tasa < 0:
        raise ValueError("La tasa no puede ser negativa.")
    return float(subtotal * tasa)




def calcular_total(subtotal: float, iva: float) -> float:

    if subtotal < 0 or iva < 0:
     raise ValueError("Ni subtotal ni IVA pueden ser negativos.")
    return float(subtotal + iva)