import os
import pandas as pd
import streamlit as st

# 1. Configuración de la interfaz móvil
st.set_page_config(
    page_title="Control de Placas Independiente",
    page_icon="🚗",
    layout="centered",
)

ARCHIVO_DB = "base_placas.csv"
# Foto por defecto (silueta de auto) si un vehículo no tiene enlace de imagen
FOTO_POR_DEFECTO = "https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?w=500"


def inicializar_base_datos():
    """Verifica si el archivo base existe; si no, crea uno estructurado con nuevas columnas."""
    if not os.path.exists(ARCHIVO_DB):
        df = pd.DataFrame(columns=["Placas", "Tipo", "Color", "Estado", "Foto"])
        df.to_csv(ARCHIVO_DB, index=False)


def cargar_base_datos():
    """Lee toda la tabla de datos de forma segura."""
    try:
        inicializar_base_datos()
        df = pd.read_csv(ARCHIVO_DB)
        # Limpiamos la columna de placas para evitar errores de espacios o minúsculas
        df["Placas"] = df["Placas"].astype(str).str.strip().str.upper()
        return df
    except Exception as e:
        st.error(f"Error al leer la base de datos local: {e}")
        return pd.DataFrame()


# --- Interfaz de la Aplicación en Pantalla ---
st.title("🚗 Control de Placas Independiente")
st.write("Versión de consulta avanzada. Funciona desde cualquier celular.")

# Cargamos el DataFrame con toda la información (no solo la lista de placas)
df_base = cargar_base_datos()

st.subheader("Verificar Placa")
placa_buscar = (
    st.text_input("Ingresa o dicta la placa a buscar:", key="buscar")
    .strip()
    .upper()
    .replace(" ", "")
)

if st.button("Verificar Acceso", type="primary"):
    if placa_buscar:
        # Buscamos la fila exacta que coincida con la placa escrita
        vehiculo_encontrado = df_base[df_base["Placas"] == placa_buscar]

        if not vehiculo_encontrado.empty:
            st.success(f"🟢 **ACCESO PERMITIDO:** La placa {placa_buscar} SÍ está registrada.")
            
            # Extraemos los datos del vehículo (tomamos la primera coincidencia)
            datos_auto = vehiculo_encontrado.iloc[0]
            
            tipo = datos_auto.get("Tipo", "No especificado")
            color = datos_auto.get("Color", "No especificado")
            estado = datos_auto.get("Estado", "No especificado")
            url_foto = datos_auto.get("Foto")

            # Si la columna de foto está vacía en el archivo, usamos la silueta por defecto
            if pd.isna(url_foto) or str(url_foto).strip() == "":
                url_foto = FOTO_POR_DEFECTO

            # --- DISEÑO VISUAL EN EL CELULAR ---
            st.write("---")
            st.subheader("📋 Datos del Vehículo")
            
            # Creamos dos columnas: una para el texto y otra para la foto
            col_datos, col_foto = st.columns([1, 1])
            
            with col_datos:
                st.write(f"**🚘 Tipo:** {tipo}")
                st.write(f"**🎨 Color:** {color}")
                st.write(f"**📍 Estado/Origen:** {estado}")
                
            with col_foto:
                st.image(
                    url_foto, 
                    caption=f"Registro visual: {placa_buscar}", 
                    use_container_width=True
                )
        else:
            st.error(f"🔴 **ALERTA:** La placa {placa_buscar} NO se encuentra en el sistema.")
    else:
        st.warning("Por favor, ingresa una placa primero.")
