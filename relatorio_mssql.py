import pandas as pd
import pyodbc
import os
import sys
import getpass
from config import (
    MSSQL_SERVER,
    MSSQL_DATABASE,
    MSSQL_TABLE,
    MSSQL_OUTPUT_FILE,
    MSSQL_CHUNK_SIZE,
    MSSQL_TRUSTED_CONNECTION
)

# ==============================
# CONFIGURAÇÕES
# ==============================

SERVER = MSSQL_SERVER
DATABASE = MSSQL_DATABASE
TABLE = MSSQL_TABLE
OUTPUT_FILE = MSSQL_OUTPUT_FILE
CHUNK_SIZE = MSSQL_CHUNK_SIZE

# Construir string de conexão
if MSSQL_TRUSTED_CONNECTION.lower() == "yes":
    CONN_STR = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        'Trusted_Connection=yes;'
    )
else:
    print("Autenticação por credenciais:")
    user = input("Usuário SQL Server: ")
    password = getpass.getpass("Senha SQL Server: ")
    CONN_STR = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'UID={user};'
        f'PWD={password};'
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
	*
FROM
	{DATABASE}.dbo.{TABLE}
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