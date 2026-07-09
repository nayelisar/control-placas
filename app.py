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


def inicializar_base_datos():
    """Verifica si el archivo base existe; si no, crea uno vacío con la columna correcta."""
    if not os.path.exists(ARCHIVO_DB):
        df = pd.DataFrame(columns=["Placas"])
        df.to_csv(ARCHIVO_DB, index=False)


def cargar_placas():
    """Lee las placas guardadas en el archivo del servidor."""
    try:
        inicializar_base_datos()
        df = pd.read_csv(ARCHIVO_DB)
        # Limpia espacios en blanco y convierte todo a mayúsculas
        return df["Placas"].astype(str).str.strip().str.upper().tolist()
    except Exception as e:
        st.error(f"Error al leer la base de datos local: {e}")
        return []


def guardar_nueva_placa(placa):
    """Agrega físicamente una nueva placa al archivo del servidor."""
    inicializar_base_datos()
    df = pd.read_csv(ARCHIVO_DB)

    # Creamos la nueva fila
    nueva_fila = pd.DataFrame([{"Placas": placa}])
    df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)

    # Guardamos los cambios
    df_actualizado.to_csv(ARCHIVO_DB, index=False)


# --- Interfaz de la Aplicación en Pantalla ---
st.title("🚗 Control de Placas Independiente")
st.write("Versión en la nube protegida. Funciona desde cualquier celular.")

# Pestañas para el celular
tab_verificar, tab_registrar = st.tabs(["🔍 Verificar", "📝 Registrar"])

# Cargamos la lista actualizada
lista_placas = cargar_placas()

# --- PESTAÑA 1: VERIFICAR ---
with tab_verificar:
    st.subheader("Verificar Placa")
    placa_buscar = (
        st.text_input("Ingresa o dicta la placa a buscar:", key="buscar")
        .strip()
        .upper()
        .replace(" ", "")
    )

    if st.button("Verificar Acceso", type="primary"):
        if placa_buscar:
            if placa_buscar in lista_placas:
                st.success(
                    f"🟢 **ACCESO PERMITIDO:** La placa {placa_buscar} SÍ está registrada."
                )
            else:
                st.error(
                    f"🔴 **ALERTA:** La placa {placa_buscar} NO se encuentra en el sistema."
                )
        else:
            st.warning("Por favor, ingresa una placa primero.")

# --- PESTAÑA 2: REGISTRAR ---
with tab_registrar:
    st.subheader("Registrar Nueva Placa")
    nueva_placa = (
        st.text_input("Ingresa la nueva placa a guardar:", key="registrar")
        .strip()
        .upper()
        .replace(" ", "")
    )

    if st.button("Guardar Placa"):
        if nueva_placa:
            if nueva_placa in lista_placas:
                st.error(f"⚠️ La placa {nueva_placa} ya existe en la base de datos.")
            else:
                guardar_nueva_placa(nueva_placa)
                st.success(
                    f"✅ ¡La placa {nueva_placa} se guardó con éxito en el sistema!"
                )
                st.rerun()
        else:
            st.warning("La placa no puede estar vacía.")
