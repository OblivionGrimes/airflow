import sys
from pathlib import Path
import pandas as pd
import sqlite3
import streamlit as st
from core.db_connection import get_connection

SRC_DIR = Path(__file__).parent.parent
SQLITE = SRC_DIR / "core" / "demanda.db"

# Querys
@st.cache_data(ttl=600) # dados ficam armazenados em cache por 10 min
def carregar_dados(query: str):
    try:
        with get_connection() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        with sqlite3.connect(SQLITE) as conn:
            return pd.read_sql(query, conn)
    
def dados_demanda_dia(num_mes=None):
    try:
        with get_connection() as conn:
            if num_mes is None:
                query = """
                    SELECT "DataMovimento", SUM("Demanda") AS demanda_total
                    FROM dados
                    GROUP BY "DataMovimento"
                    ORDER BY "DataMovimento";
                """
            else:
                query = f"""
                    SELECT "DataMovimento", SUM("Demanda") AS demanda_total
                    FROM dados
                    WHERE EXTRACT(MONTH FROM "DataMovimento") = {int(num_mes)}
                    GROUP BY "DataMovimento"
                    ORDER BY "DataMovimento";
                """
            return pd.read_sql(query, conn)

    except Exception:
        sqlite_uri = f"file:{SQLITE.resolve().as_posix()}?mode=ro"
        with sqlite3.connect(sqlite_uri, uri=True) as conn:
            if num_mes is None:
                query = """
                    SELECT "DataMovimento", SUM("Demanda") AS demanda_total
                    FROM dados
                    GROUP BY "DataMovimento"
                    ORDER BY "DataMovimento";
                """
            else:
                mes = int(num_mes)
                query = f"""
                    SELECT "DataMovimento", SUM("Demanda") AS demanda_total
                    FROM dados
                    WHERE strftime('%m', "DataMovimento") = '{mes:02d}'
                    GROUP BY "DataMovimento"
                    ORDER BY "DataMovimento";
                """
            return pd.read_sql(query, conn)