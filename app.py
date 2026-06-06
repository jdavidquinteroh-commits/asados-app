import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import json

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

st.title("🔥 Calculadora de Asados")
st.caption("Controla tus costos y ganancias fácilmente")

opcion = st.sidebar.selectbox("¿Qué quieres hacer?", [
    "Calcular precio por persona",
    "Calcular precio por evento",
    "Mis recetas guardadas",
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