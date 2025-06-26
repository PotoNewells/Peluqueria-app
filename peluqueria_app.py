import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

ARCHIVO = "peluqueria.xlsx"
bsas_tz = pytz.timezone("America/Argentina/Buenos_Aires")

# Crear archivo si no existe
if not os.path.exists(ARCHIVO):
    df = pd.DataFrame(columns=["Fecha y hora", "Cliente", "Forma de pago", "Monto"])
    df.to_excel(ARCHIVO, index=False)

# Cargar datos existentes
df = pd.read_excel(ARCHIVO)

# Convertir la columna "Fecha y hora" a datetime con manejo de errores
df["Fecha y hora"] = pd.to_datetime(df["Fecha y hora"], format="%d/%m/%Y %H:%M:%S", errors="coerce")

# Mostrar advertencia si hay fechas inválidas
if df["Fecha y hora"].isna().any():
    st.warning("⚠️ Algunas filas tienen fechas inválidas y no serán consideradas.")

# Título
st.title("💇‍♀️ Control de pagos - Peluquería")
st.markdown("Ingresá los datos del cliente:")

with st.form(key="formulario"):
    cliente = st.text_input("Cliente")
    forma_pago = st.selectbox("Forma de pago", ["Efectivo", "Transferencia"])
    monto = st.text_input("Monto ($)")
    submit_button = st.form_submit_button(label="Guardar")

if submit_button:
    if cliente and monto:
        try:
            monto_valor = float(monto)
            ahora_bsas = datetime.now(bsas_tz)
            fecha_str = ahora_bsas.strftime("%d/%m/%Y %H:%M:%S")
            nueva_fila = {
                "Fecha y hora": fecha_str,
                "Cliente": cliente,
                "Forma de pago": forma_pago,
                "Monto": monto_valor
            }
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
            df.to_excel(ARCHIVO, index=False)
            st.success("✅ Datos guardados correctamente")
        except ValueError:
            st.error("❌ Monto inválido")
    else:
        st.error("❌ Completá todos los campos")

# Fecha actual según zona horaria BsAs para filtrar
ahora_bsas = datetime.now(bsas_tz)
hoy_bsas = ahora_bsas.date()
mes_actual_bsas = ahora_bsas.month

# Filtrar filas con fechas válidas para hoy y mes actual
df_valid = df.dropna(subset=["Fecha y hora"])

df_hoy = df_valid[df_valid["Fecha y hora"].dt.date == hoy_bsas]
df_mes = df_valid[df_valid["Fecha y hora"].dt.month == mes_actual_bsas]

st.subheader("💰 Totales del día")
efectivo_dia = df_hoy[df_hoy["Forma de pago"] == "Efectivo"]["Monto"].sum()
transferencia_dia = df_hoy[df_hoy["Forma de pago"] == "Transferencia"]["Monto"].sum()
st.write(f"Efectivo: ${efectivo_dia:.2f} | Transferencia: ${transferencia_dia:.2f}")

st.subheader("📅 Total del mes")
total_mes = df_mes["Monto"].sum()
st.write(f"Total mensual: ${total_mes:.2f}")

# Exportar cierre del día
if not df_hoy.empty:
    cierre_nombre = f"cierre_{hoy_bsas.strftime('%d-%m-%Y')}.xlsx"
    df_hoy.to_excel(cierre_nombre, index=False)
    with open(cierre_nombre, "rb") as f:
        st.download_button("📤 Exportar cierre del día", f, file_name=cierre_nombre)

# Descargar todo el Excel
with open(ARCHIVO, "rb") as f:
    st.download_button(
        label="📥 Descargar todo el Excel con los datos",
        data=f,
        file_name=ARCHIVO,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
