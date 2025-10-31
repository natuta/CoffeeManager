import pytest
from app import Cliente, Producto, Pedido




def test_agregar_y_calcular_total():
    cliente = Cliente("Juan Pérez")
    pedido = Pedido(cliente)
    cafe = Producto("Café", 10)
    tostada = Producto("Tostada", 5)


    pedido.agregar_producto(cafe, 2) # 20
    pedido.agregar_producto(tostada, 1) # 5


    assert pedido.calcular_total() == 25




def test_agregar_cantidad_invalida():
    cliente = Cliente("Juan Pérez")
    pedido = Pedido(cliente)
    with pytest.raises(ValueError):
     pedido.agregar_producto(Producto("Café", 10), 0)




def test_quitar_producto_y_cantidades():
    cliente = Cliente("Ana")
    pedido = Pedido(cliente)
    cafe = Producto("Café", 10)
    pedido.agregar_producto(cafe, 3)
    pedido.quitar_producto(cafe, 1)
    assert pedido.calcular_total() == 20
    pedido.quitar_producto(cafe)
    assert pedido.items == []




def test_quitar_producto_no_existente():
    cliente = Cliente("Ana")
    pedido = Pedido(cliente)
    with pytest.raises(ValueError):
     pedido.quitar_producto(Producto("Café", 10))