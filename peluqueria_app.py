
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

ARCHIVO = "peluqueria.xlsx"

# Crear archivo si no existe
if not os.path.exists(ARCHIVO):
    df = pd.DataFrame(columns=["Fecha", "Hora", "Cliente", "Forma de pago", "Monto"])
    df.to_excel(ARCHIVO, index=False)

# Cargar datos existentes
df = pd.read_excel(ARCHIVO)

# Formulario de carga
st.title("💇‍♀️ Control de pagos - Peluquería")

st.markdown("Ingresá los datos del cliente:")

cliente = st.text_input("Cliente")
forma_pago = st.selectbox("Forma de pago", ["Efectivo", "Transferencia"])
monto = st.text_input("Monto ($)")

if st.button("Guardar"):
    if cliente and monto:
        try:
            monto = float(monto)
            ahora = datetime.utcnow() - timedelta(hours=3)  # Hora Argentina UTC-3
            nueva_fila = {
                "Fecha": ahora.strftime("%Y-%m-%d"),
                "Hora": ahora.strftime("%H:%M"),
                "Cliente": cliente,
                "Forma de pago": forma_pago,
                "Monto": monto
            }
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
            df.to_excel(ARCHIVO, index=False)
            st.success("✅ Datos guardados")
            st.rerun()
        except ValueError:
            st.error("❌ Monto inválido")
    else:
        st.error("❌ Completá todos los campos")

# Totales diarios y mensuales
df["Fecha"] = pd.to_datetime(df["Fecha"])
hoy = datetime.now().date()
mes_actual = datetime.now().month

df_hoy = df[df["Fecha"].dt.date == hoy]
df_mes = df[df["Fecha"].dt.month == mes_actual]

st.subheader("💰 Totales del día")
efectivo_dia = df_hoy[df_hoy["Forma de pago"] == "Efectivo"]["Monto"].sum()
transferencia_dia = df_hoy[df_hoy["Forma de pago"] == "Transferencia"]["Monto"].sum()
st.write(f"Efectivo: ${efectivo_dia:.2f} | Transferencia: ${transferencia_dia:.2f}")

st.subheader("📅 Total del mes")
total_mes = df_mes["Monto"].sum()
st.write(f"Total mensual: ${total_mes:.2f}")
