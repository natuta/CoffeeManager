from app import Cliente, Producto, Pedido, calcular_subtotal, calcular_iva, calcular_total




def test_calculo_total_integrado():
    cliente = Cliente("Juan Pérez")
    p1 = Producto("Café", 10)
    p2 = Producto("Tostada", 5)
    pedido = Pedido(cliente)
    pedido.agregar_producto(p1)
    pedido.agregar_producto(p2)


    subtotal = calcular_subtotal(pedido)
    iva = calcular_iva(subtotal)
    total = calcular_total(subtotal, iva)


    assert subtotal == 15
    assert round(iva, 2) == 1.95 # 13% de 15
    assert round(total, 2) == 16.95