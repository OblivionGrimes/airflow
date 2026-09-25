import sys
from pathlib import Path

import pandas as pd
import streamlit as st

SRC_DIR = Path(__file__).resolve().parents[2] # 3x parent
sys.path.append(str(SRC_DIR))

from core.db_connection import get_connection

meses = {0:"todos", 1:'janeiro', 2:'fevereiro', 3:'março', 4:'abril', 5:'maio', 6:'junho', 7:'julho', 8:'agosto', 9:'setembro', 10:'outubro', 11:'novembro', 12:'dezembro'}

############################################################################################################

def sidebar(df):
    with st.sidebar:
        st.header("Filtros")
        mesesMov = sorted(df["DataMovimento"].dt.month.unique())
        mesesMov = ["todos"] + [meses[mes] for mes in mesesMov if mes in meses]

        atualMes = st.selectbox(options=mesesMov, label="Mes")
        if st.button("🔄 Atualizar dados"):
            st.cache_data.clear()
            
        return atualMes
            
############################################################################################################

def titulo_pagina(titulo: str, desc: str):
    st.title(titulo)
    st.caption(desc)