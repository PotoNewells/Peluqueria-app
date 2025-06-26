import streamlit as st
import pandas as pd
from datetime import datetime
import os

ARCHIVO = "peluqueria.xlsx"

# Crear archivo si no existe
if not os.path.exists(ARCHIVO):
    df = pd.DataFrame(columns=["Fecha y hora", "Cliente", "Forma de pago", "Monto"])
    df.to_excel(ARCHIVO, index=False)

# Cargar datos existentes
df = pd.read_excel(ARCHIVO)

# Título
st.title("💇‍♀️ Control de pagos - Peluquería")
st.markdown("Ingresá los datos del cliente:")

# Formulario
with st.form(key="formulario"):
    cliente = st.text_input("Cliente")
    forma_pago = st.selectbox("Forma de pago", ["Efectivo", "Transferencia"])
    monto = st.text_input("Monto ($)")
    submit_button = st.form_submit_button(label="Guardar")

if submit_button:
    if cliente and monto:
        try:
            monto_valor = float(monto)
            nueva_fila = {
                "Fecha y hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Cliente": cliente,
                "Forma de pago": forma_pago,
                "Monto": monto_valor
            }
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
            df.to_excel(ARCHIVO, index=False)
            st.success("✅ Datos guardados correctamente")

            # Refrescar para limpiar campos
            st.experimental_set_query_params(refrescar="1")

        except ValueError:
            st.error("❌ Monto inválido")
    else:
        st.error("❌ Completá todos los campos")

# Totales
df["Fecha y hora"] = pd.to_datetime(df["Fecha y hora"])
hoy = datetime.now().date()
mes_actual = datetime.now().month

df_hoy = df[df["Fecha y hora"].dt.date == hoy]
df_mes = df[df["Fecha y hora"].dt.month == mes_actual]

st.subheader("💰 Totales del día")
efectivo_dia = df_hoy[df_hoy["Forma de pago"] == "Efectivo"]["Monto"].sum()
transferencia_dia = df_hoy[df_hoy["Forma de pago"] == "Transferencia"]["Monto"].sum()
st.write(f"Efectivo: ${efectivo_dia:.2f} | Transferencia: ${transferencia_dia:.2f}")

st.subheader("📅 Total del mes")
total_mes = df_mes["Monto"].sum()
st.write(f"Total mensual: ${total_mes:.2f}")

# Exportar cierre del día
if not df_hoy.empty:
    cierre_nombre = f"cierre_{hoy.strftime('%Y-%m-%d')}.xlsx"
    df_hoy.to_excel(cierre_nombre, index=False)
    with open(cierre_nombre, "rb") as f:
        st.download_button("📤 Exportar cierre del día", f, file_name=cierre_nombre)
