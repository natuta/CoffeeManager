import pytest
from app import Cliente




def test_cliente_valido():
    c = Cliente("Ana Gómez", "ana@gmail.com")
    assert c.nombre == "Ana Gómez"
    assert c.email == "ana@gmail.com"




def test_cliente_nombre_vacio():
    with pytest.raises(ValueError):
     Cliente("")




def test_cliente_email_invalido():
    with pytest.raises(ValueError):
     Cliente("Carlos", "correo-invalido")