import sys
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(APP_DIR))

from functions.function_app import carregar_dados, dados_demanda_dia
from app.components.components import sidebar, titulo_pagina, meses

# Config da pagina
st.set_page_config(
    page_title="Dados transporte público",
    page_icon="🚌",
    layout="wide",
)

try:
    df = carregar_dados("""SELECT "DataMovimento", "CodLinha", "NomeLinha", "TipoPassageiro", "NomePassageiro", "Demanda" FROM dados;""")
except Exception as erro:
    st.error(f"Não foi possível conectar ao banco de dados: {erro}")
    st.stop()

df["DataMovimento"] = pd.to_datetime(df["DataMovimento"])

# Sidebar
side = sidebar(df)

titulo_pagina("Transporte publico", "Dados tratados, com dois filtros (mes e tipo)")


if side == "todos":
    dfMes = df.copy()
else:
    dfMes = df[df["DataMovimento"].dt.month.map(meses) == side].reset_index(drop=True)

# Kpi's
st.subheader("Dados por Mês")
colM1, colM2, colM3, colM4 = st.columns(4)
colM1.metric("Total de registros", f"{len(dfMes):,}")
colM2.metric("Demanda total", f"{int(dfMes['Demanda'].sum()):,}")
colM3.metric("Linhas/terminais distintos", dfMes["CodLinha"].nunique())
colM4.metric("Mês", side)

st.divider()

# Graficos
colGraf1, colGraf2 = st.columns(2)
with colGraf1:
    st.subheader("Top 10 terminais/linhas por demanda")
    top10 = (dfMes.groupby("NomeLinha")["Demanda"].sum().sort_values(ascending=False).head(10))
    
    st.bar_chart(top10)
        
with colGraf2:

    st.subheader("Top 5 Passageiros por demanda")
    top10Passageiro = (dfMes.groupby("NomePassageiro")["Demanda"].sum().sort_values(ascending=False).head(5))
    
    st.bar_chart(top10Passageiro)

st.divider()

#st.subheader("")
#st._arrow_line_chart()

#st.divider()

# Tabela
st.subheader("Dados por Linhas")

tipo = ["todos"] + list(dfMes["NomeLinha"].unique())
tipoAtual = st.selectbox(options=tipo, label="Linhas")

if tipoAtual == "todos":
    dfMes = dfMes.copy()
else:
    dfMes = dfMes[dfMes["NomeLinha"] == tipoAtual].reset_index(drop=True)

st.dataframe(dfMes.groupby("NomePassageiro")["Demanda"].sum().sort_values(ascending=False), use_container_width=True)

st.divider()
num_mes = list(meses.values()).index(side)
if num_mes == 0:
    query = ''
else:
    query = f'WHERE EXTRACT(MONTH FROM "DataMovimento") = {num_mes}'
    
st.subheader("Demanda total por dia")
demanda_dias = dados_demanda_dia(query)
st.dataframe(demanda_dias, use_container_width=True)
