import sys
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
import os

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

# Carrega o .env da raiz do OT Trans
load_dotenv(dotenv_path=env_path)

def get_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )