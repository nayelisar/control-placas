import streamlit as st
import pandas as pd
import os

# Configuración del archivo
ARCHIVO_DB = "base_placas.csv"
FOTO_POR_DEFECTO = "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?q=80&w=400&auto=format&fit=crop"

# 1. Inicializar la base de datos con las 5 columnas requeridas
def inicializar_base_datos():
    if not os.path.exists(ARCHIVO_DB):
        df = pd.DataFrame(columns=["Placas", "Tipo", "Color", "Estado", "Foto"])
        df.to_csv(ARCHIVO_DB, index=False)

inicializar_base_datos()

# Título de la app
st.title("🚗 Control de Placas Independiente")
st.write("Funciona desde cualquier celular.")

# --- SECCIÓN 1: VERIFICAR PLACA ---
st.header("Verificar Placa")

try:
    df_base = pd.read_csv(ARCHIVO_DB)
    # Limpiamos espacios y aseguramos que todo esté en mayúsculas para evitar fallos
    df_base["Placas"] = df_base["Placas"].astype(str).str.strip().str.upper()
except Exception as e:
    st.error(f"Error al leer la base de datos local: {e}")
    df_base = pd.DataFrame(columns=["Placas", "Tipo", "Color", "Estado", "Foto"])

placa_buscar = st.text_input("Ingresa o dicta la placa a buscar:").strip().upper()

if st.button("Verificar Acceso", type="primary"):
    if placa_buscar:
        vehiculo_encontrado = df_base[df_base["Placas"] == placa_buscar]
        
        if not vehiculo_encontrado.empty:
            st.success(f"🟢 ACCESO PERMITIDO: La placa {placa_buscar} SÍ está registrada.")
            
            st.subheader("📋 Datos del Vehículo")
            datos_auto = vehiculo_encontrado.iloc[0]
            
            # Extraer características controlando celdas vacías
            tipo = datos_auto.get("Tipo", "No especificado")
            color = datos_auto.get("Color", "No especificado")
            estado = datos_auto.get("Estado", "No especificado")
            url_foto = datos_auto.get("Foto", FOTO_POR_DEFECTO)
            
            if pd.isna(url_foto) or str(url_foto).strip() == "":
                url_foto = FOTO_POR_DEFECTO
                
            # Diseño en dos columnas para el celular
            col_datos, col_foto = st.columns([1, 1])
            with col_datos:
                st.write(f"**🚘 Tipo:** {tipo}")
                st.write(f"**🎨 Color:** {color}")
                st.write(f"**📌 Estado:** {estado}")
            with col_foto:
                st.image(url_foto, use_container_width=True)
        else:
            st.error(f"🔴 ACCESO DENEGADO: La placa {placa_buscar} NO está registrada.")
    else:
        st.warning("Por favor, ingresa una placa válida primero.")

st.markdown("---")

# --- SECCIÓN 2: AGREGAR NUEVAS PLACAS ---
with st.expander("➕ Registrar Nuevo Vehículo"):
    st.write("Llena los campos para añadir un auto a la lista permitida:")
    
    # Formulario de entrada
    nueva_placa = st.text_input("Número de Placa (Obligatorio):").strip().upper()
    nuevo_tipo = st.text_input("Tipo / Marca de Auto (Ej. Ford Explorer):").strip()
    nuevo_color = st.text_input("Color del Vehículo:").strip()
    nuevo_estado = st.text_input("Estado / Origen (Ej. Oaxaca):").strip()
    nueva_foto = st.text_input("Enlace (URL) de la Foto (Opcional):").strip()

    if st.button("Guardar Registro"):
        if nueva_placa:
            # Comprobar si ya existe para evitar duplicados
            if nueva_placa in df_base["Placas"].values:
                st.warning(f"La placa {nueva_placa} ya se encuentra registrada en el sistema.")
            else:
                # Si no hay foto, dejar celda vacía para usar el respaldo por defecto
                foto_guardar = nueva_foto if nueva_foto else ""
                
                # Crear nueva fila
                nueva_fila = pd.DataFrame([{
                    "Placas": nueva_placa,
                    "Tipo": nuevo_tipo,
                    "Color": nuevo_color,
                    "Estado": nuevo_estado,
                    "Foto": foto_guardar
                }])
                
                # Guardar al final del archivo CSV sin alterar el resto
                nueva_fila.to_csv(ARCHIVO_DB, mode='a', header=False, index=False)
                st.success(f"✅ ¡Excelente! Vehículo con placas {nueva_placa} registrado con éxito.")
                
                # Forzar recarga ligera para actualizar la lista en memoria
                st.rerun()
        else:
            st.error("El campo 'Número de Placa' no puede quedar vacío.")