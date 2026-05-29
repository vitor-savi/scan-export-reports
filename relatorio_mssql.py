import pandas as pd
import pyodbc
import os

# ==============================
# CONFIGURAÇÕES
# ==============================

SERVER = 'server_name'
DATABASE = 'database_name'
TABLE = 'table_name'
OUTPUT_FILE = 'output_file.csv'

CHUNK_SIZE = 100000  

CONN_STR = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={SERVER};'
    f'DATABASE={DATABASE};'
    'Trusted_Connection=yes;'
)

# ==============================
# CONEXÃO
# ==============================

conn = pyodbc.connect(CONN_STR)

# ==============================
# QUERY
# ==============================

query = f"""
SELECT
	USR_CODIGO,
	USR_NOME,
	GRUPO_ID,
	GRUPO_CODIGO,
	GRUPO_NOME,
	REGRA_ID,
	REGRA_DESCRICAO,
	ROTINA_NOME,
	MENU_ACESSA,
	ROTINA_DESCRICAO,
	ROTINA_OPCAO,
	ROTINA_ACESSA,
	ROTINA_ORDEM,
	ROTINA_FUNCAO_MENU
FROM
	DATABASE.dbo.TABLE
"""

# ==============================
# EXPORTAÇÃO
# ==============================

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

print("Iniciando exportação para CSV...")

first_chunk = True
total_rows = 0

for chunk in pd.read_sql(query, conn, chunksize=CHUNK_SIZE):
    
    chunk.to_csv(
        OUTPUT_FILE,
        mode='a',
        index=False,
        header=first_chunk,
        sep=';',           
        encoding='utf-8-sig'  
    )

    total_rows += len(chunk)
    first_chunk = False

    print(f"{total_rows} linhas exportadas...")

print("✅ Exportação concluída!")
print(f"Arquivo gerado: {OUTPUT_FILE}")