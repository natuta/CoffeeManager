import pytest
from app import Cliente




def test_cliente_valido():
    c = Cliente("Ana Gómez", "ana@example.com")
    assert c.nombre == "Ana Gómez"
    assert c.email == "ana@example.com"




def test_cliente_nombre_vacio():
    with pytest.raises(ValueError):
     Cliente("")




def test_cliente_email_invalido():
    with pytest.raises(ValueError):
     Cliente("Carlos", "correo-invalido")