import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
sys.path.append(str(SRC_DIR))

from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from Config.config import caminho_arquivo
from functions.function import dados_brutos, tratar_dados, salvar_dados



with DAG('index_dag', start_date=datetime(2026, 1, 1), schedule=None, catchup=False) as dag:
    
    dados_brutos_task = PythonOperator(
        task_id='dados_brutos_task',
        python_callable=dados_brutos,
        op_args=[caminho_arquivo]
    )

    
    tratar_dados_task = PythonOperator(
        task_id='tratar_dados_task',
        python_callable=tratar_dados,
        op_args=[dados_brutos_task.output]
    )
    
    salvar_dados_task = PythonOperator(
        task_id='salvar_dados_task',
        python_callable=salvar_dados,
        op_args=[tratar_dados_task.output]
    )
    
    
    dados_brutos_task >> tratar_dados_task >> salvar_dados_task