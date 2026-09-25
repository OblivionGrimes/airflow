import sys
from pathlib import Path

tests = Path(__file__).resolve().parents[1]
sys.path.append(str(tests))

import pandas as pd
import pytest
import json

from src.functions.function import mapear_tipo_sql, tratar_dados, dados_brutos


def test_data():
  assert mapear_tipo_sql(pd.Series([1]).dtype) == "INT"
  assert mapear_tipo_sql(pd.Series([1.5]).dtype) == "NUMERIC"
  assert mapear_tipo_sql(pd.Series(["texto"]).dtype) == "VARCHAR(255)"
  assert (mapear_tipo_sql(pd.to_datetime(pd.Series(["2022-01-01"])).dtype) == "DATE")


def test_tratar_dados():
    json_teste = json.dumps([
        {
            "DataMovimento": "01/02/2022",
            "CodLinha": "2",
            "NomeLinha": "  Catraca Móvel/Terminal/Antônio Bezerra  ",
            "TipoPassageiro": "2",
            "NomePassageiro": "Popular",
            "Demanda": "50",
        },
        {
            "DataMovimento": None,
            "CodLinha": "1",
            "NomeLinha": "Terminal Antônio Bezerra",
            "TipoPassageiro": "5",
            "NomePassageiro": "Vale-transporte (vermelho)",
            "Demanda": None,
        },  
    ])

    res = tratar_dados(json_teste)
    dados = json.loads(res)

    assert len(dados) == 1
    assert dados[0]["NomeLinha"] == "Catraca Móvel/Terminal/Antônio Bezerra"
    
def test_dados_brutos(tmp_path):
    arquivo = tmp_path / "dados.csv"
    arquivo.write_text(
        "01/02/2022;2;Catraca Móvel/Terminal/Antônio Bezerra;2;Popular;50",
        encoding="utf-8-sig",
    )

    res = dados_brutos(str(arquivo))
    dados = json.loads(res)

    assert len(dados) == 1
    assert dados[0]["CodLinha"] == 2
    assert dados[0]["Demanda"] == 50
    