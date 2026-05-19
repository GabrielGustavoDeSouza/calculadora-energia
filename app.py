import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Calculadora de Economia de Energia",
    page_icon="💡",
    layout="wide"
)

def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("💡 Calculadora de Economia de Energia")
st.markdown("Simule a economia com base no uso real das lâmpadas.")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    lampadas_anteriores = st.number_input(
        "Qtd lâmpadas (ANTES)",
        min_value=0,
        value=200
    )

with col2:
    lampadas_atuais = st.number_input(
        "Qtd lâmpadas (ATUAL)",
        min_value=0,
        value=150
    )

with col3:
    potencia_watts = st.number_input(
        "Potência por lâmpada (Watts)",
        min_value=0.0,
        value=100.0
    )

with col4:
    valor_kwh = st.number_input(
        "Valor do kWh (R$)",
        min_value=0.0,
        value=0.90
    )

# NOVA LINHA
col5, col6 = st.columns(2)

with col5:
    horas_dia = st.number_input(
        "Horas por dia",
        min_value=0.0,
        value=10.0
    )

with col6:
    dias_mes = st.number_input(
        "Dias trabalhados no mês",
        min_value=0,
        value=22
    )

# 🔥 CÁLCULO REAL
consumo_kwh_por_lampada = (potencia_watts * horas_dia * dias_mes) / 1000

custo_anterior_mes = lampadas_anteriores * consumo_kwh_por_lampada * valor_kwh
custo_atual_mes = lampadas_atuais * consumo_kwh_por_lampada * valor_kwh

economia_mes = custo_anterior_mes - custo_atual_mes
economia_12_meses = economia_mes * 12

st.divider()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Custo mensal anterior", moeda(custo_anterior_mes))
kpi2.metric("Custo mensal atual", moeda(custo_atual_mes))
kpi3.metric("Economia mensal", moeda(economia_mes))
kpi4.metric("Economia em 12 meses", moeda(economia_12_meses))

meses = list(range(1, 13))

df = pd.DataFrame({
    "Mês": meses,
    "Gasto anterior acumulado": [custo_anterior_mes * mes for mes in meses],
    "Gasto atual acumulado": [custo_atual_mes * mes for mes in meses],
    "Economia acumulada": [economia_mes * mes for mes in meses]
})

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Mês"],
    y=df["Gasto anterior acumulado"],
    mode="lines+markers",
    name="Gasto anterior",
    line=dict(color="red", width=4)
))

fig.add_trace(go.Scatter(
    x=df["Mês"],
    y=df["Gasto atual acumulado"],
    mode="lines+markers",
    name="Gasto atual",
    line=dict(color="orange", width=4)
))

fig.add_trace(go.Scatter(
    x=df["Mês"],
    y=df["Economia acumulada"],
    mode="lines+markers",
    name="Economia",
    line=dict(color="green", width=4)
))

fig.update_layout(
    title="Projeção acumulada em 12 meses",
    xaxis_title="Mês",
    yaxis_title="R$",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Projeção mês a mês")
st.dataframe(df, use_container_width=True)
