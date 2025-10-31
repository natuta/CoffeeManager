# streamlit_app.py
import streamlit as st
from app import Cliente, Producto, Pedido, calcular_subtotal, calcular_iva, calcular_total

st.set_page_config(page_title="CoffeeManager", page_icon="☕")
st.title("CoffeeManager – Sistema de pedidos")

# Datos demo (en un caso real vendrían de una BD)
CLIENTES_DEMO = [
    Cliente("Ana Gómez", "ana@example.com"),
    Cliente("Carlos Rojas", "carlos@example.com"),
    Cliente("Juan Pérez", "juan@example.com"),
]
PRODUCTOS_DEMO = {
    "Café": 10.0,
    "Tostada": 5.0,
    "Jugo": 8.0,
}

# Selección de cliente
cliente_nombre = st.selectbox("Selecciona un cliente", [c.nombre for c in CLIENTES_DEMO])
cliente = next(c for c in CLIENTES_DEMO if c.nombre == cliente_nombre)

st.subheader("Productos")
cantidades: dict[str, int] = {}
for nombre, precio in PRODUCTOS_DEMO.items():
    cantidades[nombre] = st.number_input(
        f"Cantidad de {nombre} (Bs {precio:.2f})",
        min_value=0,
        value=0,
        step=1,
        key=f"qty_{nombre}",
    )

if st.button("Calcular total"):
    pedido = Pedido(cliente)
    for nombre, qty in cantidades.items():
        if qty > 0:
            pedido.agregar_producto(Producto(nombre, PRODUCTOS_DEMO[nombre]), cantidad=qty)

    if not pedido.items:
        st.warning("Agrega al menos un producto.")
    else:
        subtotal = calcular_subtotal(pedido)
        iva = calcular_iva(subtotal)
        total = calcular_total(subtotal, iva)
        st.success(f"Subtotal: {subtotal:.2f} Bs  |  IVA (13%): {iva:.2f} Bs  |  Total: {total:.2f} Bs")

st.caption("Demo educativa – Streamlit")
