import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
from Config.config import caminho_arquivo
from core.db_connection import get_connection

###################################################################################################################################

def dados_brutos(caminho_arquivo):
    
    COLUNAS = ["DataMovimento", "CodLinha", "NomeLinha", "TipoPassageiro", "NomePassageiro", "Demanda"]
    var = pd.read_csv(caminho_arquivo, sep=";", header=None, nrows=1, encoding="utf-8-sig")
    primeiro_valor = str(var.iloc[0, 0]).strip()
    
    try:
        datetime.strptime(str(primeiro_valor), '%d/%m/%Y')
        head = False
    except ValueError:
        head = True

    df = pd.read_csv(caminho_arquivo, sep=";", header=0 if head else None, names=COLUNAS, encoding="utf-8-sig")
    
    print(f"[info] datas {df['DataMovimento'].unique()}")
    
    return df.to_json(orient="records") #date_format="iso"

###################################################################################################################################

def tratar_dados(dataframe_json):
    df = pd.read_json(dataframe_json, orient="records")

    for col in ["NomeLinha", "NomePassageiro"]:
        df[col] = df[col].str.strip()

    # Converte tipos
    #df["DataMovimento"] = pd.to_datetime(df["DataMovimento"], errors="coerce")
    df["DataMovimento"] = df["DataMovimento"].astype(str).str.strip()
    df["DataMovimento"] = pd.to_datetime(df["DataMovimento"], dayfirst=True, errors="coerce")
    df["CodLinha"] = pd.to_numeric(df["CodLinha"], errors="coerce").astype("Int64")
    df["TipoPassageiro"] = pd.to_numeric(df["TipoPassageiro"], errors="coerce").astype("Int64")
    df["Demanda"] = pd.to_numeric(df["Demanda"], errors="coerce").astype("Int64")

    nulos_data = df["DataMovimento"].isna().sum()
    nulos_demanda = df["Demanda"].isna().sum()
    print(
        f"[DEBUG] Nulos em DataMovimento: {nulos_data} | Nulos em Demanda:"
        f" {nulos_demanda}"
    )

    linhas_antes = len(df)

    vazios = df[df[["DataMovimento", "Demanda"]].isna().any(axis=1)]
    if not vazios.empty:
        print(f"[ALERTA] {len(vazios)} linha(s) com DataMovimento ou Demanda vazios foram removidas.")

    df = df.dropna(subset=["DataMovimento", "Demanda"]).reset_index(drop=True)

    print(f"[OK] {linhas_antes} linhas lidas -> {len(df)} linhas após limpeza.")
    # Por para salvar em documento depois

    print(f"[info] datas {df['DataMovimento'].unique()}")
    return df.to_json(orient="records", date_format="iso")

###################################################################################################################################

def mapear_tipo_sql(dtype):
  """Mapeia o tipo de coluna do Pandas para o tipo correspondente no PostgreSQL."""
  if pd.api.types.is_datetime64_any_dtype(dtype):
      return "DATE"
  elif pd.api.types.is_integer_dtype(dtype):
    return "INT"
  elif pd.api.types.is_float_dtype(dtype):
    return "NUMERIC"
  else:
    return "VARCHAR(255)"

###################################################################################################################################

def salvar_dados(dataframe_tratado_json, table = 'dados') -> bool:
    
    df = pd.read_json(dataframe_tratado_json, orient="records")
    df['DataMovimento'] = pd.to_datetime(df['DataMovimento']) #converte para Y/m/d
        
    print(f"[info] datas {df['DataMovimento'].unique()}")
        
    head = list(df.columns)
    
    print(f"[info] head:{head}")
    
    colunas = []
    for col in head:
        tipo_sql = mapear_tipo_sql(df[col].dtype)
        colunas.append(f'"{col}" {tipo_sql}')
        
    str_colunas = ",\n    ".join(colunas)
    colunas_insert = ", ".join([f'"{col}"' for col in head])
    
    sql = f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                {str_colunas}
            );
            """
    valores = [tuple(x) for x in df.to_numpy()]
    query = f"INSERT INTO {table} ({colunas_insert}) VALUES %s;"
    
    print(f"[info] SQL:{sql}")
    
    with get_connection() as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(sql)
            
            if execute_values(cursor, query, valores, page_size=5000) == None:
                res = True
            else:
                res = False
        
        cursor.close()
    conn.close()
    
    return res


