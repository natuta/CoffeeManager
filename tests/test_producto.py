import pytest
from app import Producto




def test_crear_producto_valido():
    p = Producto("Café", 10.5)
    assert p.nombre == "Café"
    assert p.precio == 10.5




def test_precio_invalido_negativo():
    with pytest.raises(ValueError):
     Producto("Café", -2)




def test_precio_invalido_cero():
    with pytest.raises(ValueError):
     Producto("Café", 0)




def test_precio_no_numerico():
    with pytest.raises(ValueError):
     Producto("Café", float("nan"))