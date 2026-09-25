import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]

DOCS_DIR = BASE_DIR / "docs"
ARQUIVOS_BRUTOS_DIR = DOCS_DIR / "arquivos_brutos"
ARQUIVOS_LIMPOS_DIR = DOCS_DIR / "arquivos_limpos"

caminho_arquivo = ARQUIVOS_BRUTOS_DIR / "demanda_202201.csv" # Mudar depois pra que pegue todos os documentos da pasta
