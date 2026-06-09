import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import json

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

load_dotenv()

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

cliente = Groq(api_key=api_key)

ARCHIVO = "recetas.json"

CORTES = [
    "Bondiola de cerdo",
    "Chicharrón",
    "Punta de anca de res",
    "Chorizo",
    "Costillas de cerdo",
    "Pollo",
    "Falda de res",
    "Pecho de res"
]

ACOMPANANTES = [
    "Chimichurri",
    "Papa hervida",
    "Mazorca",
    "Ensalada",
    "Arepas"
]

CONDIMENTOS = [
    "Sal",
    "Pimienta",
    "Sal marina",
    "Cerveza (litro)",
    "Ajos",
    "Cebolla",
    "Pimentón"
]

UTENSILIOS = [
    "Contenedores J1",
    "Tenedores",
    "Palillos para dientes",
    "Copas de salsa",
    "Papel parafinado",
    "Bolsas",
    "Carbon"
    
]

def calcular_costo(cantidad, unidad, precio_unit):
    if unidad == "gramos":
        return (cantidad / 1000) * precio_unit
    else:
        return cantidad * precio_unit

def cargar_recetas():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    return {}

def guardar_recetas(recetas):
    with open(ARCHIVO, "w") as f:
        json.dump(recetas, f)

def seccion_cortes(prefijo):
    st.subheader("🥩 Cortes de carne")
    costos_cortes = {}
    total_carne = 0
    for corte in CORTES:
        incluir = st.checkbox(corte, key=f"{prefijo}_check_{corte}")
        if incluir:
            col1, col2, col3 = st.columns(3)
            with col1:
                cantidad = st.number_input("Cantidad", min_value=0.1, value=1.0, step=0.1, key=f"{prefijo}_cant_{corte}")
            with col2:
                unidad = st.selectbox("Unidad", ["kg","gramos", "unidad"], key=f"{prefijo}_uni_{corte}")
            with col3:
                precio_unit = st.number_input("Precio COP", min_value=0, value=20000, step=1000, key=f"{prefijo}_precio_{corte}")
            costo = calcular_costo(cantidad, unidad, precio_unit)
            costos_cortes[corte] = {"cantidad": cantidad, "unidad": unidad, "precio": precio_unit, "costo": costo}
            total_carne += costo
    if total_carne > 0:
        st.info(f"💰 Total carnes: ${total_carne:,.0f}")
    return costos_cortes, total_carne

def seccion_acompanantes(prefijo):
    st.subheader("🥗 Acompañantes")
    costos_acomp = {}
    total_acomp = 0
    for acomp in ACOMPANANTES:
        incluir = st.checkbox(acomp, key=f"{prefijo}_acomp_check_{acomp}")
        if incluir:
            col1, col2, col3 = st.columns(3)
            with col1:
                cantidad = st.number_input("Cantidad", min_value=0.1, value=1.0, step=0.1, key=f"{prefijo}_acomp_cant_{acomp}")
            with col2:
                unidad = st.selectbox("Unidad", ["unidad", "kg", "gramos"], key=f"{prefijo}_acomp_uni_{acomp}")
            with col3:
                precio_unit = st.number_input("Precio COP", min_value=0, value=5000, step=500, key=f"{prefijo}_acomp_precio_{acomp}")
            costo = calcular_costo(cantidad, unidad, precio_unit)
            costos_acomp[acomp] = {"cantidad": cantidad, "unidad": unidad, "precio": precio_unit, "costo": costo}
            total_acomp += costo
    if total_acomp > 0:
        st.info(f"💰 Total acompañantes: ${total_acomp:,.0f}")
    return costos_acomp, total_acomp

def seccion_condimentos(prefijo):
    st.subheader("🧂 Condimentos y marinada")
    costos_cond = {}
    total_cond = 0
    for cond in CONDIMENTOS:
        incluir = st.checkbox(cond, key=f"{prefijo}_cond_check_{cond}")
        if incluir:
            col1, col2, col3 = st.columns(3)
            with col1:
                cantidad = st.number_input("Cantidad", min_value=0.1, value=1.0, step=0.1, key=f"{prefijo}_cond_cant_{cond}")
            with col2:
                if cond == "Cerveza (litro)":
                    unidad = st.selectbox("Unidad", ["litro", "unidad"], key=f"{prefijo}_cond_uni_{cond}")
                else:
                    unidad = st.selectbox("Unidad", ["gramos", "kg", "unidad"], key=f"{prefijo}_cond_uni_{cond}")
            with col3:
                precio_unit = st.number_input("Precio COP", min_value=0, value=2000, step=500, key=f"{prefijo}_cond_precio_{cond}")
            costo = calcular_costo(cantidad, unidad, precio_unit)
            costos_cond[cond] = {"cantidad": cantidad, "unidad": unidad, "precio": precio_unit, "costo": costo}
            total_cond += costo
    if total_cond > 0:
        st.info(f"💰 Total condimentos: ${total_cond:,.0f}")
    return costos_cond, total_cond

def seccion_utensilios(prefijo):
    st.subheader("🧴 Utensilios")
    costos_util = {}
    total_util = 0
    for util in UTENSILIOS:
        incluir = st.checkbox(util, key=f"{prefijo}_util_check_{util}")
        if incluir:
            col1, col2 = st.columns(2)
            with col1:
                cantidad = st.number_input("Cantidad", min_value=1, value=10, step=1, key=f"{prefijo}_util_cant_{util}")
            with col2:
                precio_unit = st.number_input("Precio unidad COP", min_value=0, value=500, step=100, key=f"{prefijo}_util_precio_{util}")
            costo = cantidad * precio_unit
            costos_util[util] = {"cantidad": cantidad, "precio": precio_unit, "costo": costo}
            total_util += costo
    if total_util > 0:
        st.info(f"💰 Total utensilios: ${total_util:,.0f}")
    return costos_util, total_util

HISTORIAL = "historial.json"

def cargar_historial():
    if os.path.exists(HISTORIAL):
        with open(HISTORIAL, "r") as f:
            return json.load(f)
    return []

def guardar_historial(historial):
    with open(HISTORIAL, "w") as f:
        json.dump(historial, f)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("logo.png", width=300)   

st.markdown("""
    <style>
        .stApp {
            background-color: #F5F0E8;
        }
        .stSidebar {
            background-color: #FFFFFF;
            border-right: 3px solid #FF6B00;
        }
        h1, h2, h3 {
            color: #FF6B00 !important;
        }
        .stButton > button {
            background-color: #FF6B00;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #cc5500;
            color: white;
        }
        [data-testid="stMetricValue"] {
            color: #FF6B00 !important;
            font-weight: bold;
        }
        [data-testid="stMetricLabel"] {
            color: #666666 !important;
        }
        .stInfo {
            border-left: 3px solid #FF6B00;
        }
        hr {
            border-color: #FF6B00;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #C9A84C;'>🔥 BARRIL AND GRILL 🔥</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Calculadora de costos y ganancias</p>", unsafe_allow_html=True)

opcion = st.sidebar.selectbox("¿Qué quieres hacer?", [
    "Calcular precio por persona",
    "Calcular precio por evento",
    "Mis recetas guardadas",
    "🌮 Calculadora de Tacos",
    "📅 Historial de eventos",
    "📄 Generar presupuesto PDF",
    "Asesoría con IA"
])

if opcion == "Calcular precio por persona":
    st.header("👤 Precio por persona")
    costos_cortes, total_carne = seccion_cortes("pp")
    costos_acomp, total_acomp = seccion_acompanantes("pp")
    costos_cond, total_cond = seccion_condimentos("pp")
    costos_util, total_util = seccion_utensilios("pp")
    st.subheader("🚗 Logística")
    transporte = st.number_input("Transporte (COP)", min_value=0, value=20000, step=1000)
    otros = st.number_input("Otros gastos (COP)", min_value=0, value=10000, step=1000)
    personas = st.number_input("Número de personas", min_value=1, value=8, step=1)
    margen = st.slider("Margen de ganancia (%)", min_value=10, max_value=100, value=30)

    
    costo_total = total_carne + total_acomp + total_cond + total_util + transporte + otros
    costo_por_persona = costo_total / personas
    precio_venta = costo_por_persona * (1 + margen / 100)
    ganancia_total = (precio_venta - costo_por_persona) * personas
   
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Costo total", f"${costo_total:,.0f}")
    col2.metric("Costo por persona", f"${costo_por_persona:,.0f}")
    col3.metric("Precio sugerido", f"${precio_venta:,.0f}")
    col4.metric("Ganancia total", f"${ganancia_total:,.0f}")

    nombre_receta = st.text_input("Nombre para guardar esta receta")
    if st.button("Guardar receta"):
        if nombre_receta.strip():
            recetas = cargar_recetas()
            recetas[nombre_receta] = {
                "cortes": costos_cortes,
                "acompanantes": costos_acomp,
                "condimentos": costos_cond,
                "transporte": transporte,
                "otros": otros,
                "personas": personas,
                "margen": margen,
                "tipo": "por_persona"
            }
            guardar_recetas(recetas)
            st.success(f"✓ Receta '{nombre_receta}' guardada")
        else:
            st.warning("Escribe un nombre para la receta")

elif opcion == "Calcular precio por evento":
    st.header("🎉 Precio por evento")
    costos_cortes, total_carne = seccion_cortes("pe")
    costos_acomp, total_acomp = seccion_acompanantes("pe")
    costos_cond, total_cond = seccion_condimentos("pe")

    st.subheader("🚗 Logística y tiempo")
    transporte = st.number_input("Transporte (COP)", min_value=0, value=30000, step=1000)
    otros = st.number_input("Otros gastos (COP)", min_value=0, value=15000, step=1000)
    horas = st.number_input("Horas de trabajo", min_value=1, value=4, step=1)
    valor_hora = st.number_input("Valor hora de trabajo (COP)", min_value=0, value=25000, step=1000)
    margen = st.slider("Margen de ganancia (%)", min_value=10, max_value=100, value=30)
   
    costo_total = total_carne + total_acomp + total_cond + total_util + transporte + otros
    costo_por_persona = costo_total / personas
    precio_venta = costo_por_persona * (1 + margen / 100)
    ganancia_total = (precio_venta - costo_por_persona) * personas

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Costo total", f"${costo_total:,.0f}")
    col2.metric("Precio sugerido", f"${precio_evento:,.0f}")

elif opcion == "Mis recetas guardadas":
    st.header("📋 Mis recetas")
    recetas = cargar_recetas()
    if len(recetas) == 0:
        st.info("No tienes recetas guardadas todavía")
    else:
        for nombre, datos in recetas.items():
            with st.expander(f"🍖 {nombre}"):
                if "cortes" in datos:
                    st.write("**Cortes incluidos:**")
                    for corte, info in datos["cortes"].items():
                        if isinstance(info, dict):
                            st.write(f"- {corte}: {info['cantidad']} {info['unidad']} — ${info['costo']:,.0f}")
                total_carne = sum(v["costo"] if isinstance(v, dict) else v for v in datos.get("cortes", {}).values())
                total_acomp = sum(v["costo"] if isinstance(v, dict) else v for v in datos.get("acompanantes", {}).values())
                total_cond = sum(v["costo"] if isinstance(v, dict) else v for v in datos.get("condimentos", {}).values())
                costo = total_carne + total_acomp + total_cond + datos.get("transporte", 0) + datos.get("otros", 0)
                precio = (costo / datos["personas"]) * (1 + datos["margen"] / 100)
                ganancia = (precio - costo / datos["personas"]) * datos["personas"]
                col1, col2, col3 = st.columns(3)
                col1.metric("Personas", datos["personas"])
                col2.metric("Precio por persona", f"${precio:,.0f}")
                col3.metric("Ganancia", f"${ganancia:,.0f}")
                if st.button(f"Eliminar", key=f"del_{nombre}"):
                    del recetas[nombre]
                    guardar_recetas(recetas)
                    st.rerun()

elif opcion == "🌮 Calculadora de Tacos":
    st.header("🌮 Tacos de Birria")
    st.caption("Calcula el costo y precio de tus tacos")

    st.subheader("🥩 Carnes")
    carnes_taco = {}
    total_carnes_taco = 0
    for carne in ["Falda de res", "Pecho de res", "Cañón de cerdo"]:
        incluir = st.checkbox(carne, key=f"taco_carne_{carne}")
        if incluir:
            col1, col2, col3 = st.columns(3)
            with col1:
                cantidad = st.number_input("Cantidad", min_value=0.1, value=1.0, step=0.1, key=f"taco_cant_{carne}")
            with col2:
                unidad = st.selectbox("Unidad", ["kg", "gramos"], key=f"taco_uni_{carne}")
            with col3:
                precio = st.number_input("Precio COP", min_value=0, value=20000, step=1000, key=f"taco_precio_{carne}")
            costo = calcular_costo(cantidad, unidad, precio)
            carnes_taco[carne] = costo
            total_carnes_taco += costo
    if total_carnes_taco > 0:
        st.info(f"💰 Total carnes: ${total_carnes_taco:,.0f}")

    st.subheader("🥬 Legumbres y frescos")
    legumbres_taco = {}
    total_legumbres = 0
    for leg in ["Tomate", "Cebolla", "Ajo", "Ají", "Aguacate", "Perejil", "Piña", "Limones", "Cebolla morada"]:
        incluir = st.checkbox(leg, key=f"taco_leg_{leg}")
        if incluir:
            col1, col2, col3 = st.columns(3)
            with col1:
                cantidad = st.number_input("Cantidad", min_value=0.1, value=1.0, step=0.1, key=f"taco_leg_cant_{leg}")
            with col2:
                unidad = st.selectbox("Unidad", ["unidad", "kg", "gramos"], key=f"taco_leg_uni_{leg}")
            with col3:
                precio = st.number_input("Precio COP", min_value=0, value=2000, step=500, key=f"taco_leg_precio_{leg}")
            costo = calcular_costo(cantidad, unidad, precio)
            legumbres_taco[leg] = costo
            total_legumbres += costo
    if total_legumbres > 0:
        st.info(f"💰 Total legumbres: ${total_legumbres:,.0f}")

    st.subheader("🧂 Especias")
    especias_taco = {}
    total_especias = 0
    for esp in ["Orégano", "Tomillo", "Laurel", "Sal", "Pimienta"]:
        incluir = st.checkbox(esp, key=f"taco_esp_{esp}")
        if incluir:
            col1, col2, col3 = st.columns(3)
            with col1:
                cantidad = st.number_input("Cantidad", min_value=0.1, value=1.0, step=0.1, key=f"taco_esp_cant_{esp}")
            with col2:
                unidad = st.selectbox("Unidad", ["gramos", "kg", "unidad"], key=f"taco_esp_uni_{esp}")
            with col3:
                precio = st.number_input("Precio COP", min_value=0, value=1000, step=500, key=f"taco_esp_precio_{esp}")
            costo = calcular_costo(cantidad, unidad, precio)
            especias_taco[esp] = costo
            total_especias += costo
    if total_especias > 0:
        st.info(f"💰 Total especias: ${total_especias:,.0f}")

    st.subheader("🧀 Otros ingredientes")
    otros_taco = {}
    total_otros_taco = 0
    for otro in ["Queso mozzarella", "Tortillas", "Agua"]:
        incluir = st.checkbox(otro, key=f"taco_otro_{otro}")
        if incluir:
            col1, col2, col3 = st.columns(3)
            with col1:
                cantidad = st.number_input("Cantidad", min_value=0.1, value=1.0, step=0.1, key=f"taco_otro_cant_{otro}")
            with col2:
                if otro == "Agua":
                    unidad = st.selectbox("Unidad", ["litro"], key=f"taco_otro_uni_{otro}")
                elif otro == "Tortillas":
                    unidad = st.selectbox("Unidad", ["unidad", "paquete"], key=f"taco_otro_uni_{otro}")
                else:
                    unidad = st.selectbox("Unidad", ["kg", "gramos"], key=f"taco_otro_uni_{otro}")
            with col3:
                precio = st.number_input("Precio COP", min_value=0, value=5000, step=500, key=f"taco_otro_precio_{otro}")
            costo = calcular_costo(cantidad, unidad, precio)
            otros_taco[otro] = costo
            total_otros_taco += costo
    if total_otros_taco > 0:
        st.info(f"💰 Total otros: ${total_otros_taco:,.0f}")

    st.subheader("⚙️ Logística")
    gas = st.number_input("Gas (COP)", min_value=0, value=10000, step=1000)
    transporte_taco = st.number_input("Transporte (COP)", min_value=0, value=20000, step=1000)
    tacos_por_porcion = st.selectbox("Tacos por porción", [2, 3])
    total_tacos = st.number_input("Total de tacos a preparar", min_value=1, value=30, step=1)
    margen_taco = st.slider("Margen de ganancia (%)", min_value=10, max_value=100, value=40)

    costo_total_taco = total_carnes_taco + total_legumbres + total_especias + total_otros_taco + gas + transporte_taco
    porciones = total_tacos / tacos_por_porcion
    costo_por_porcion = costo_total_taco / porciones if porciones > 0 else 0
    precio_porcion = costo_por_porcion * (1 + margen_taco / 100)
    ganancia_taco = (precio_porcion - costo_por_porcion) * porciones

    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Costo total", f"${costo_total_taco:,.0f}")
    col2.metric("Costo por porción", f"${costo_por_porcion:,.0f}")
    col3.metric(f"Precio por {tacos_por_porcion} tacos", f"${precio_porcion:,.0f}")
    col4.metric("Ganancia total", f"${ganancia_taco:,.0f}")

elif opcion == "📅 Historial de eventos":
    st.header("📅 Historial de eventos")

    historial = cargar_historial()

    st.subheader("➕ Registrar nuevo evento")
    col1, col2 = st.columns(2)
    with col1:
        tipo_evento = st.selectbox("Tipo de evento", ["Asado al barril", "Tacos de birria", "Evento completo"])
        fecha = st.date_input("Fecha del evento")
    with col2:
        descripcion = st.text_input("Descripción (opcional)")
        personas_evento = st.number_input("Personas atendidas", min_value=1, value=8, step=1)

    col1, col2, col3 = st.columns(3)
    with col1:
        ingresos = st.number_input("Ingresos totales (COP)", min_value=0, value=0, step=1000)
    with col2:
        costos = st.number_input("Costos totales (COP)", min_value=0, value=0, step=1000)
    with col3:
        ganancia_evento = ingresos - costos
        st.metric("Ganancia", f"${ganancia_evento:,.0f}")

    if st.button("Registrar evento"):
        if ingresos > 0:
            historial.append({
                "tipo": tipo_evento,
                "fecha": str(fecha),
                "descripcion": descripcion,
                "personas": personas_evento,
                "ingresos": ingresos,
                "costos": costos,
                "ganancia": ganancia_evento
            })
            guardar_historial(historial)
            st.success("✓ Evento registrado")
        else:
            st.warning("Ingresa los ingresos del evento")

    st.divider()
    st.subheader("📋 Eventos registrados")

    if len(historial) == 0:
        st.info("No tienes eventos registrados todavía")
    else:
        total_ingresos = sum(e["ingresos"] for e in historial)
        total_costos = sum(e["costos"] for e in historial)
        total_ganancia = sum(e["ganancia"] for e in historial)
        total_personas = sum(e["personas"] for e in historial)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total ingresos", f"${total_ingresos:,.0f}")
        col2.metric("Total costos", f"${total_costos:,.0f}")
        col3.metric("Total ganancia", f"${total_ganancia:,.0f}")
        col4.metric("Personas atendidas", total_personas)

        st.divider()
        for i, evento in enumerate(reversed(historial)):
            with st.expander(f"📌 {evento['fecha']} — {evento['tipo']} — ${evento['ganancia']:,.0f}"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Ingresos", f"${evento['ingresos']:,.0f}")
                col2.metric("Costos", f"${evento['costos']:,.0f}")
                col3.metric("Ganancia", f"${evento['ganancia']:,.0f}")
                st.write(f"👥 Personas: {evento['personas']}")
                if evento['descripcion']:
                    st.write(f"📝 {evento['descripcion']}")
                if st.button("Eliminar", key=f"del_evento_{i}"):
                    historial.pop(len(historial) - 1 - i)
                    guardar_historial(historial)
                    st.rerun()

elif opcion == "📄 Generar presupuesto PDF":
    st.header("📄 Generar presupuesto")
    st.caption("Crea un presupuesto profesional para tu cliente")

    col1, col2 = st.columns(2)
    with col1:
        nombre_cliente = st.text_input("Nombre del cliente")
        telefono_cliente = st.text_input("Teléfono del cliente")
        correo_cliente = st.text_input("Correo electrónico del cliente")
        fecha_evento = st.date_input("Fecha del evento")
    with col2:
        tipo_servicio = st.selectbox("Tipo de servicio", [
            "Asado al barril",
            "Tacos de birria",
            "Asado al barril + Tacos",
            "Evento completo"
        ])
        personas_presupuesto = st.number_input("Número de personas", min_value=1, value=10, step=1)
        lugar_evento = st.text_input("Lugar del evento")

    st.subheader("💰 Detalles del presupuesto")
    
    st.write("**Servicios incluidos:**")
    items = []
    
    agregar_item = st.checkbox("Agregar item personalizado")
    if agregar_item:
        col1, col2, col3 = st.columns(3)
        with col1:
            item_nombre = st.text_input("Descripción del item")
        with col2:
            item_cantidad = st.number_input("Cantidad", min_value=1, value=1)
        with col3:
            item_precio = st.number_input("Precio unitario COP", min_value=0, value=10000, step=1000)
        if item_nombre:
            items.append({"nombre": item_nombre, "cantidad": item_cantidad, "precio": item_precio})

    costo_base = st.number_input("Costo base del servicio (COP)", min_value=0, value=200000, step=10000)
    descuento = st.slider("Descuento (%)", min_value=0, max_value=30, value=0)
    nota_cliente = st.text_area("Nota para el cliente (opcional)")

if st.button("✍️ Corregir texto con IA"):
    if nota_cliente.strip():
        with st.spinner("Corrigiendo..."):
            respuesta = cliente.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un corrector ortográfico. Corrige tildes, puntuación y ortografía del texto que te den. Devuelve SOLO el texto corregido, sin explicaciones ni comentarios."
                    },
                    {
                        "role": "user",
                        "content": nota_cliente
                    }
                ]
            )
            nota_cliente = respuesta.choices[0].message.content
            st.success("✓ Texto corregido")
            st.write(nota_cliente)
    else:
        st.warning("Escribe algo primero")
        
    subtotal = costo_base + sum(i["cantidad"] * i["precio"] for i in items)
    descuento_valor = subtotal * (descuento / 100)
    total = subtotal - descuento_valor

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Subtotal", f"${subtotal:,.0f}")
    col2.metric("Descuento", f"${descuento_valor:,.0f}")
    col3.metric("Total", f"${total:,.0f}")

    if st.button("📄 Generar PDF"):
        if not nombre_cliente:
            st.warning("Escribe el nombre del cliente")
        else:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                   rightMargin=inch*0.75, leftMargin=inch*0.75,
                                   topMargin=inch*0.75, bottomMargin=inch*0.75)

            styles = getSampleStyleSheet()
            elementos = []

            estilo_titulo = ParagraphStyle(
                'titulo',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#FF6B00'),
                spaceAfter=6,
                alignment=1
            )
            estilo_subtitulo = ParagraphStyle(
                'subtitulo',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#666666'),
                spaceAfter=4,
                alignment=1
            )
            estilo_normal = ParagraphStyle(
                'normal',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=4
            )
            estilo_bold = ParagraphStyle(
                'bold',
                parent=styles['Normal'],
                fontSize=10,
                fontName='Helvetica-Bold',
                spaceAfter=4
            )

            try:
                elementos.append(RLImage("logo.png", width=1.5*inch, height=1.5*inch))
            except:
                pass

            elementos.append(Paragraph("BARRIL AND GRILL", estilo_titulo))
            elementos.append(Paragraph("Marinados · Ahumados · Calidad", estilo_subtitulo))
            elementos.append(Spacer(1, 0.2*inch))

            datos_empresa = [
                ["📞 WhatsApp:", "3245872010"],
                ["📍 Ciudad:", "EL RETIRO"],
                ["📅 Fecha presupuesto:", str(fecha_evento)],
            ]
            tabla_empresa = Table(datos_empresa, colWidths=[2*inch, 4*inch])
            tabla_empresa.setStyle(TableStyle([
                ('FONTSIZE', (0,0), (-1,-1), 9),
                ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#FF6B00')),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ]))
            elementos.append(tabla_empresa)
            elementos.append(Spacer(1, 0.2*inch))

            elementos.append(Paragraph("DATOS DEL CLIENTE", ParagraphStyle('sec', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#FF6B00'))))
            
            datos_cliente = [
                ["Cliente:", nombre_cliente],
                ["Teléfono:", telefono_cliente],
                ["Fecha del evento:", str(fecha_evento)],
                ["Lugar:", lugar_evento],
                ["Número de personas:", str(personas_presupuesto)],
                ["Servicio:", tipo_servicio],
            ]
            tabla_cliente = Table(datos_cliente, colWidths=[2*inch, 4*inch])
            tabla_cliente.setStyle(TableStyle([
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#333333')),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#F5F0E8'), colors.white]),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DDDDDD')),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            elementos.append(tabla_cliente)
            elementos.append(Spacer(1, 0.2*inch))

            elementos.append(Paragraph("DETALLE DEL PRESUPUESTO", ParagraphStyle('sec', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#FF6B00'))))

            datos_tabla = [["Descripción", "Cantidad", "Precio unit.", "Total"]]
            datos_tabla.append([tipo_servicio, "1", f"${costo_base:,.0f}", f"${costo_base:,.0f}"])
            for item in items:
                total_item = item['cantidad'] * item['precio']
                datos_tabla.append([item['nombre'], str(item['cantidad']), f"${item['precio']:,.0f}", f"${total_item:,.0f}"])
            datos_tabla.append(["", "", "Subtotal:", f"${subtotal:,.0f}"])
            if descuento > 0:
                datos_tabla.append(["", "", f"Descuento ({descuento}%):", f"-${descuento_valor:,.0f}"])
            datos_tabla.append(["", "", "TOTAL:", f"${total:,.0f}"])

            tabla_presupuesto = Table(datos_tabla, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
            tabla_presupuesto.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FF6B00')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('GRID', (0,0), (-1,-2), 0.5, colors.HexColor('#DDDDDD')),
                ('ROWBACKGROUNDS', (0,1), (-1,-3), [colors.white, colors.HexColor('#F5F0E8')]),
                ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
                ('TEXTCOLOR', (2,-1), (-1,-1), colors.HexColor('#FF6B00')),
                ('FONTSIZE', (0,-1), (-1,-1), 12),
                ('PADDING', (0,0), (-1,-1), 8),
            ]))
            elementos.append(tabla_presupuesto)
            elementos.append(Spacer(1, 0.2*inch))

            if nota_cliente:
                elementos.append(Paragraph("NOTAS:", estilo_bold))
                elementos.append(Paragraph(nota_cliente, estilo_normal))
                elementos.append(Spacer(1, 0.1*inch))

            elementos.append(Spacer(1, 0.3*inch))
            elementos.append(Paragraph("¡Gracias por confiar en Barril And Grill!", ParagraphStyle('gracias', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#FF6B00'), alignment=1)))
            elementos.append(Paragraph("Sabor Real · Fuego Lento · Marinados · Ahumados · Calidad", ParagraphStyle('slogan', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#888888'), alignment=1)))

            doc.build(elementos)
            buffer.seek(0)

            st.success("✓ PDF generado exitosamente")
            st.download_button(
                label="⬇️ Descargar presupuesto PDF",
                data=buffer,
                file_name=f"presupuesto_{nombre_cliente}_{fecha_evento}.pdf",
                mime="application/pdf"
            )
elif opcion == "Asesoría con IA":
    st.header("🤖 Asesoría con IA")
    st.caption("Pregúntale a la IA sobre precios, estrategias y consejos para tu negocio")

    if "historial_asados" not in st.session_state:
        st.session_state.historial_asados = []

    for mensaje in st.session_state.historial_asados:
        if mensaje["role"] == "user":
            st.chat_message("user").write(mensaje["content"])
        else:
            st.chat_message("assistant").write(mensaje["content"])

    pregunta = st.chat_input("¿Qué quieres preguntarle?")
    if pregunta:
        st.session_state.historial_asados.append({"role": "user", "content": pregunta})
        st.chat_message("user").write(pregunta)

        with st.spinner("Consultando..."):
            mensajes = [
                {"role": "system", "content": "Eres un experto en emprendimientos de comida colombiana, especialmente asados al barril y tacos. Das consejos prácticos sobre precios, costos, marketing y estrategias de negocio. Usas pesos colombianos (COP) y conoces el mercado colombiano."}
            ] + st.session_state.historial_asados

            respuesta = cliente.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=mensajes
            )

            respuesta_texto = respuesta.choices[0].message.content
            st.session_state.historial_asados.append({"role": "assistant", "content": respuesta_texto})
            st.chat_message("assistant").write(respuesta_texto)