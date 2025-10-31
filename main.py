from app import Cliente, Producto, Pedido, calcular_subtotal, calcular_iva, calcular_total




def demo() -> None:
    cliente = Cliente("Juan Pérez", "juan@gmail.com")
    p1 = Producto("Café", 10)
    p2 = Producto("Tostada", 5)


    pedido = Pedido(cliente)
    pedido.agregar_producto(p1, 2)
    pedido.agregar_producto(p2, 1)


    subtotal = calcular_subtotal(pedido)
    iva = calcular_iva(subtotal)
    total = calcular_total(subtotal, iva)


    print(f"Cliente: {cliente.nombre}")
    print(f"Subtotal: {subtotal:.2f} Bs | IVA: {iva:.2f} Bs | Total: {total:.2f} Bs")




if __name__ == "__main__":
    demo()