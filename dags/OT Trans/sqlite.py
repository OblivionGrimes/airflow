import sqlite3
import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).parent / "src"
sys.path.append(str(SRC_DIR))
from core.db_connection import get_connection 

SQLITE = Path(__file__).parent / "src" / "core" / "demanda.db"

def exportar():
    conn = get_connection()

    df = pd.read_sql(f'SELECT * FROM dados', conn)
    conn.close()

    SQLITE.parent.mkdir(parents=True, exist_ok=True)
    conn_sqlite = sqlite3.connect(SQLITE)

    df.to_sql("dados", conn_sqlite, if_exists="replace", index=False)
    conn_sqlite.close()

    tamanho_mb = SQLITE.stat().st_size / (1024 * 1024)
    print(f"[OK] {len(df)} linha(s) exportada(s) para {SQLITE} ({tamanho_mb:.2f} MB)")


if __name__ == "__main__":
    exportar()