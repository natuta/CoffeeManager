# streamlit_app.py
import streamlit as st
import pandas as pd
from typing import List, Tuple

from app import (
    Cliente,
    Producto,
    Pedido,
    calcular_subtotal,
    calcular_iva,
    calcular_total,
)

# -------------------------------------------------
# Configuración base
# -------------------------------------------------
st.set_page_config(page_title="CoffeeManager", page_icon="☕", layout="wide")

# -------------------------------------------------
# Tema y estilos (Café latte vibes)
# -------------------------------------------------
st.markdown(
    """
    <style>
    :root {
      --c-brown: #5C3D2E;     /* moka */
      --c-brown-2: #7A4E3A;   /* mocha */
      --c-cream: #F5E6D3;     /* crema */
      --c-cream-2: #F2E9E4;   /* espuma */
      --c-hazelnut: #C49A6C;  /* avellana */
      --c-white: #FFFFFF;
      --c-shadow: rgba(0,0,0,0.1);
    }

    /* Fondo con textura sutil de café */
    .stApp {
      background-image: url('https://images.unsplash.com/photo-1512568400610-62da28bc8a13?q=80&w=1600&auto=format&fit=crop');
      background-size: cover;
      background-attachment: fixed;
      background-position: center;
    }

    /* Contenedor principal con velo suave */
    .block-container {
      background: rgba(255,255,255,0.86);
      backdrop-filter: blur(2.5px);
      border-radius: 18px;
      box-shadow: 0 6px 30px var(--c-shadow);
      padding: 1.2rem 1.4rem 1.6rem;
    }

    /* ------------ SIDEBAR estilo cafetería ----------- */
    [data-testid="stSidebar"] > div {
      height: 100%;
      background: linear-gradient(180deg, var(--c-brown) 0%, #4C3428 100%);
      color: var(--c-cream);
      padding-top: .5rem;
    }
    [data-testid="stSidebar"] .stLogo { filter: drop-shadow(0 2px 6px rgba(0,0,0,.25)); }

    .cm-side-head {
      display: flex; align-items: center; gap:.6rem;
      padding: .6rem .6rem 0 .3rem; margin-bottom: .3rem;
      color: var(--c-cream);
    }
    .cm-side-head .bean {
      width: 38px; height: 38px; border-radius: 10px;
      background: linear-gradient(135deg, var(--c-hazelnut), #b37f4e);
      display:flex; align-items:center; justify-content:center;
      box-shadow: inset 0 2px 6px rgba(0,0,0,.18), 0 4px 16px rgba(0,0,0,.14);
      font-size: 1.1rem;
    }
    .cm-side-head h2 {
      margin:0; font-weight:700; font-size:1.05rem; letter-spacing:.3px;
    }
    .cm-divider {
      height:1px; background: linear-gradient(90deg, rgba(255,255,255,.0), rgba(255,255,255,.55), rgba(255,255,255,.0));
      margin:.4rem 0 .6rem;
    }

    /* Radio nav: estilo de “píldoras” */
    [data-testid="stSidebar"] .stRadio > label { color: var(--c-cream); opacity:.9; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > div {
      border: 1px solid rgba(255,255,255,.16);
      background: rgba(255,255,255,.06);
      color: var(--c-cream);
      padding: .55rem .7rem;
      border-radius: 12px;
      margin: .25rem 0;
      transition: all .18s ease-in-out;
      box-shadow: inset 0 0 0 0 rgba(255,255,255,0);
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > div:hover {
      transform: translateX(2px);
      background: rgba(255,255,255,.10);
      border-color: rgba(255,255,255,.26);
      box-shadow: inset 0 0 0 1px rgba(255,255,255,.08);
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > div[aria-checked="true"] {
      background: linear-gradient(135deg, var(--c-hazelnut), #b37f4e);
      color: var(--c-white);
      border-color: transparent;
      box-shadow: 0 4px 22px rgba(0,0,0,.18), inset 0 0 0 1px rgba(255,255,255,.14);
    }

    /* Botones */
    .stButton>button, button[kind="primary"] {
      border-radius: 12px !important;
      border: 0 !important;
      background: linear-gradient(135deg, var(--c-brown-2), var(--c-hazelnut)) !important;
      color: var(--c-white) !important;
      box-shadow: 0 6px 16px rgba(92,61,46,.25) !important;
    }
    .stButton>button:hover, button[kind="primary"]:hover {
      filter: brightness(1.03);
      transform: translateY(-1px);
    }

    /* Tablas */
    .stDataFrame { border-radius: 12px; overflow: hidden; }

    /* Métricas */
    .stMetric { background: var(--c-cream-2); border-radius: 12px; padding:.6rem; box-shadow: 0 4px 10px var(--c-shadow); }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    '<div class="cm-side-head"><div class="bean">☕</div><h2>CoffeeManager</h2></div><div class="cm-divider"></div>',
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Estado en memoria (sin base de datos)
# -------------------------------------------------
def seed_if_empty():
    if "clientes" not in st.session_state:
        st.session_state.clientes: List[Cliente] = [
            Cliente("Ana Gómez", "ana@example.com"),
            Cliente("Carlos Rojas", "carlos@example.com"),
            Cliente("Juan Pérez", "juan@example.com"),
        ]
    if "productos" not in st.session_state:
        st.session_state.productos: List[Producto] = [
            Producto("Café", 10.0),
            Producto("Tostada", 5.0),
            Producto("Jugo", 8.0),
        ]
    if "pedidos" not in st.session_state:
        st.session_state.pedidos: List[Pedido] = []
    if "carrito" not in st.session_state:
        st.session_state.carrito: List[Tuple[Producto, int]] = []

seed_if_empty()

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def df_clientes() -> pd.DataFrame:
    return pd.DataFrame([{"Nombre": c.nombre, "Email": c.email or ""} for c in st.session_state.clientes])

def df_productos() -> pd.DataFrame:
    return pd.DataFrame([{"Producto": p.nombre, "Precio (Bs)": float(p.precio)} for p in st.session_state.productos])

def df_pedidos() -> pd.DataFrame:
    rows = []
    for idx, ped in enumerate(st.session_state.pedidos, start=1):
        subtotal = calcular_subtotal(ped)
        iva = calcular_iva(subtotal)
        total = calcular_total(subtotal, iva)
        items_txt = ", ".join([f"{prod.nombre} x{cant}" for prod, cant in ped.items])
        rows.append({
            "N°": idx,
            "Cliente": ped.cliente.nombre,
            "Ítems": items_txt,
            "Subtotal (Bs)": round(subtotal, 2),
            "IVA 13% (Bs)": round(iva, 2),
            "Total (Bs)": round(total, 2),
        })
    return pd.DataFrame(rows)

def table_height(df: pd.DataFrame, base: int = 80) -> int:
    return min(420, base + 35 * (len(df) + 1))

# -------------------------------------------------
# Navegación (con iconos)
# -------------------------------------------------
label_map = {
    "Inicio": "🏠  Inicio",
    "Pedidos": "🧾  Pedidos",
    "Productos": "🫘  Productos",
    "Clientes": "👤  Clientes",
}
options = list(label_map.keys())
choice = st.sidebar.radio(
    "Navegación",
    options=options,
    format_func=lambda x: label_map[x],
    index=0,
    label_visibility="collapsed",
)

# -------------------------------------------------
# Páginas
# -------------------------------------------------
if choice == "Inicio":
    st.title("CoffeeManager – Sistema de pedidos")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Clientes", len(st.session_state.clientes))
    with c2: st.metric("Productos", len(st.session_state.productos))
    with c3: st.metric("Pedidos", len(st.session_state.pedidos))

    st.markdown("### Últimos pedidos")
    df = df_pedidos()
    if df.empty:
        st.info("Aún no hay pedidos. Crea uno en la sección **Pedidos**.")
    else:
        st.dataframe(df, width="stretch", height=table_height(df))

if choice == "Productos":
    st.title("🫘 Productos")
    left, right = st.columns([2, 1], gap="large")

    with left:
        st.subheader("Listado")
        df = df_productos()
        st.dataframe(df, width="stretch", height=table_height(df))

    with right:
        st.subheader("Agregar producto")
        with st.form("form_producto", clear_on_submit=True):
            nombre = st.text_input("Nombre del producto")
            precio = st.number_input("Precio (Bs)", min_value=0.0, step=0.5, format="%.2f")
            enviar = st.form_submit_button("Guardar")
            if enviar:
                try:
                    nuevo = Producto(nombre, float(precio))
                    if any(p.nombre.lower() == nuevo.nombre.lower() for p in st.session_state.productos):
                        st.warning("Ya existe un producto con ese nombre.")
                    else:
                        st.session_state.productos.append(nuevo)
                        st.success(f"Producto **{nuevo.nombre}** agregado.")
                        st.rerun()
                except Exception as e:
                    st.error(str(e))

if choice == "Clientes":
    st.title("👤 Clientes")
    left, right = st.columns([2, 1], gap="large")

    with left:
        st.subheader("Listado")
        df = df_clientes()
        st.dataframe(df, width="stretch", height=table_height(df))

    with right:
        st.subheader("Agregar cliente")
        with st.form("form_cliente", clear_on_submit=True):
            nombre = st.text_input("Nombre completo")
            email = st.text_input("Email (opcional)", placeholder="usuario@ejemplo.com")
            enviar = st.form_submit_button("Guardar")
            if enviar:
                try:
                    nuevo = Cliente(nombre, email if email.strip() else None)
                    if any(c.nombre.lower() == nuevo.nombre.lower() for c in st.session_state.clientes):
                        st.warning("Ya existe un cliente con ese nombre.")
                    else:
                        st.session_state.clientes.append(nuevo)
                        st.success(f"Cliente **{nuevo.nombre}** agregado.")
                        st.rerun()
                except Exception as e:
                    st.error(str(e))

if choice == "Pedidos":
    st.title("🧾 Pedidos")
    list_col, form_col = st.columns([2, 1], gap="large")

    with list_col:
        st.subheader("Listado")
        df = df_pedidos()
        st.dataframe(df, width="stretch", height=table_height(df))

    with form_col:
        st.subheader("Crear nuevo pedido")

        if not st.session_state.clientes or not st.session_state.productos:
            st.info("Necesitas al menos 1 cliente y 1 producto para crear un pedido.")
        else:
            cliente_nombre = st.selectbox("Cliente", [c.nombre for c in st.session_state.clientes], key="pedido_cliente")
            prod_nombres = [p.nombre for p in st.session_state.productos]
            prod_sel = st.selectbox("Producto", prod_nombres, key="pedido_producto")
            qty = st.number_input("Cantidad", min_value=1, value=1, step=1, key="pedido_cantidad")

            cbtn1, cbtn2, cbtn3 = st.columns([1, 1, 1])
            with cbtn1:
                if st.button("➕ Agregar ítem"):
                    p = next(p for p in st.session_state.productos if p.nombre == prod_sel)
                    st.session_state.carrito.append((p, int(qty)))
                    st.success(f"Agregado: {p.nombre} x{qty}")
                    st.rerun()
            with cbtn2:
                if st.button("🗑️ Quitar último"):
                    if st.session_state.carrito:
                        st.session_state.carrito.pop()
                        st.info("Último ítem quitado.")
                        st.rerun()
            with cbtn3:
                if st.button("🧹 Vaciar carrito"):
                    st.session_state.carrito.clear()
                    st.info("Carrito vacío.")
                    st.rerun()

            if st.session_state.carrito:
                st.markdown("**Ítems en el pedido:**")
                df_carrito = pd.DataFrame(
                    [{"Producto": prod.nombre, "Cantidad": cant, "Precio (Bs)": float(prod.precio)} for prod, cant in st.session_state.carrito]
                )
                st.dataframe(df_carrito, width="stretch", height=table_height(df_carrito, base=60))

                subtotal_preview = sum(prod.precio * cant for prod, cant in st.session_state.carrito)
                iva_preview = calcular_iva(subtotal_preview)
                total_preview = calcular_total(subtotal_preview, iva_preview)
                st.info(
                    f"**Subtotal:** {subtotal_preview:.2f} Bs  |  **IVA (13%):** {iva_preview:.2f} Bs  |  **Total:** {total_preview:.2f} Bs"
                )
            else:
                st.caption("Carrito vacío. Agrega ítems con el botón **➕ Agregar ítem**.")

            if st.button("💾 Guardar pedido", type="primary"):
                try:
                    if not st.session_state.carrito:
                        st.warning("Agrega al menos un ítem al carrito.")
                    else:
                        cliente = next(c for c in st.session_state.clientes if c.nombre == cliente_nombre)
                        pedido = Pedido(cliente)
                        for prod, cant in st.session_state.carrito:
                            pedido.agregar_producto(prod, cantidad=cant)
                        st.session_state.pedidos.append(pedido)
                        st.session_state.carrito.clear()

                        subtotal = calcular_subtotal(pedido)
                        iva = calcular_iva(subtotal)
                        total = calcular_total(subtotal, iva)
                        st.success(
                            f"Pedido guardado — Subtotal: {subtotal:.2f} Bs | IVA (13%): {iva:.2f} Bs | Total: {total:.2f} Bs"
                        )
                        st.rerun()
                except Exception as e:
                    st.error(str(e))

# Footer
st.sidebar.caption("Sabor a código • In-memory (sin BD)")
