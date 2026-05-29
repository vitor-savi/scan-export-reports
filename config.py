import os
from dotenv import load_dotenv

load_dotenv()

# Oracle
ORACLE_CLIENT_PATH = os.getenv("ORACLE_CLIENT_PATH", r"C:\oracle\instantclient_23_9")
ORACLE_DSN = os.getenv("ORACLE_DSN", "server:port/database")
ORACLE_USER = os.getenv("ORACLE_USER", "")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "")

# MSSQL
MSSQL_SERVER = os.getenv("MSSQL_SERVER", "server_name")
MSSQL_DATABASE = os.getenv("MSSQL_DATABASE", "database_name")
MSSQL_TABLE = os.getenv("MSSQL_TABLE", "table_name")
MSSQL_TRUSTED_CONNECTION = os.getenv("MSSQL_TRUSTED_CONNECTION", "yes")

# Arquivos de saída
ORACLE_OUTPUT_FILE = os.getenv("ORACLE_OUTPUT_FILE", "relatorio.xlsx")
ORACLE_LOG_FILE = os.getenv("ORACLE_LOG_FILE", "console.log")
ORACLE_CHECKPOINT_FILE = os.getenv("ORACLE_CHECKPOINT_FILE", "checkpoint.txt")

MSSQL_OUTPUT_FILE = os.getenv("MSSQL_OUTPUT_FILE", "output_file.csv")

# Performance
ORACLE_FETCH_SIZE = int(os.getenv("ORACLE_FETCH_SIZE", "5000"))
ORACLE_MAX_RETRIES = int(os.getenv("ORACLE_MAX_RETRIES", "5"))
ORACLE_RETRY_WAIT = int(os.getenv("ORACLE_RETRY_WAIT", "30"))

MSSQL_CHUNK_SIZE = int(os.getenv("MSSQL_CHUNK_SIZE", "100000"))
