import oracledb
import getpass
import os
import time
import logging
from tqdm import tqdm
from openpyxl import Workbook
import sys

# =========================
# CONFIGURAÇÕES
# =========================

ORACLE_CLIENT_PATH = r"C:\oracle\instantclient_23_9"

DSN = "server:port/database"

QUERY = """
SELECT A.DATA, A.REVIDE, A.PEDIDO
    FROM SCHEMA.TABLE A
ORDER BY DATANF DESC
"""

FETCH_SIZE = 5000
CHECKPOINT_FILE = "checkpoint.txt"
OUTPUT_FILE = "relatorio.xlsx"
LOG_FILE = "console.log"

MAX_RETRIES = 5
RETRY_WAIT = 30


# =========================
# LOG
# =========================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("Inicializando Oracle Client...\n")

oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)

# =========================
# CREDENCIAIS
# =========================

usuario = input("Usuário Oracle: ")
senha = getpass.getpass("Senha Oracle: ")


# =========================
# CONEXÃO COM RETRY
# =========================

def conectar():
    for tentativa in range(MAX_RETRIES):
        try:
            conn = oracledb.connect(
                user=usuario,
                password=senha,
                dsn=DSN,
                expire_time=60
            )
            logging.info("Conexão estabelecida com sucesso.")
            return conn
        except Exception as e:
            logging.error(f"Erro na conexão: {e}")
            print(f"Erro ao conectar. Tentando novamente em {RETRY_WAIT}s...")
            time.sleep(RETRY_WAIT)

    raise Exception("Falha ao conectar após várias tentativas.")


# =========================
# CHECKPOINT
# =========================

def salvar_checkpoint(linhas):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(linhas))


def carregar_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            return int(f.read().strip())
    return 0


# =========================
# LIMPA CHECKPOINT ANTIGO
# =========================

if os.path.exists(CHECKPOINT_FILE):
    os.remove(CHECKPOINT_FILE)


# =========================
# INICIO DA EXECUÇÃO
# =========================

linhas_processadas = carregar_checkpoint()

print(f"Checkpoint encontrado: {linhas_processadas} linhas")

modo_arquivo = "a" if linhas_processadas > 0 else "w"

conn = conectar()
cursor = conn.cursor()

cursor.arraysize = FETCH_SIZE

# +------------------------------------------------------------------------------------------------------------+
# Adicionando função para executar query com retry
# Solicitado alteração após erro detectado durante queda de conexão durante a execução do cursor.execute(QUERY)
# +------------------------------------------------------------------------------------------------------------+

def executar_query(cursor):

    global conn

    for tentativa in range(MAX_RETRIES):

        try:

            logging.info("Executando query...")
            print("Executando query... (isso pode levar horas)")

            cursor.execute(QUERY)

            logging.info("Query executada com sucesso")

            return cursor 

        except Exception as e:

            logging.error(f"Erro durante execute(): {e}")
            print(f"\nErro durante execucao da query, caso necessario, verifique o erro no console.log\n")

            if tentativa < MAX_RETRIES - 1:

                print(f"Tentando novamente em {RETRY_WAIT}s...")
                time.sleep(RETRY_WAIT)

                conn = conectar()
                cursor = conn.cursor()
                cursor.arraysize = FETCH_SIZE

            else:

                raise

cursor = executar_query(cursor)

# =========================
# PULA LINHAS JÁ PROCESSADAS
# =========================

# +------------------------------------------------------------------------+
# Adicionado ao log as informações sobre o número de linhas a serem puladas, 
# para facilitar o monitoramento e diagnóstico em caso de erros
# +------------------------------------------------------------------------+

if linhas_processadas > 0:
    print("Pulando linhas já processadas...")
    logging.info(f"Pulando {linhas_processadas} linhas já exportadas")
    puladas = 0

    while puladas < linhas_processadas:
        rows = cursor.fetchmany(FETCH_SIZE)
        if not rows:
            break
        puladas += len(rows)


# =========================
# EXCEL UTILIZANDO STREAMING
# =========================

wb = Workbook(write_only=True)
ws = wb.create_sheet("Relatorio")

if linhas_processadas == 0:

    if cursor.description is None:
        logging.info("Query não executada corretamente. cursor.description está vazio.")

    colunas = [col[0] for col in cursor.description]
    ws.append(colunas)

# =========================
# PROGRESS BAR
# =========================

pbar = tqdm(desc="Exportando linhas")

while True:

    try:

        rows = cursor.fetchmany(FETCH_SIZE)

        if not rows:
            break

        for row in rows:
            ws.append(row)

        linhas_processadas += len(rows)

        salvar_checkpoint(linhas_processadas)

        pbar.update(len(rows))

    except Exception as e:

        print("Erro detectado. Reconectando...")

        logging.error(e)

        conn = conectar()
        cursor = conn.cursor()
        cursor.arraysize = FETCH_SIZE
        cursor.execute(QUERY)

        puladas = 0

        while puladas < linhas_processadas:

            rows = cursor.fetchmany(FETCH_SIZE)
            puladas += len(rows)

pbar.close()

# =========================
# SALVA EXCEL
# =========================

print("Salvando arquivo Excel...")

wb.save(OUTPUT_FILE)

cursor.close()
conn.close()

print("Exportação concluída com sucesso.")

# +-----------------------------------------------------------+
# Adicionando log de finalização e tratamento de exceção fatal
# +-----------------------------------------------------------+

try:
    logging.info("Script finalizado com sucesso.")

except Exception as e:

    logging.exception(f"Erro fatal no script:\n {e}")
    print(f"\nERRO FATAL: {e}\n")

finally:

    input("Pressione ENTER para fechar...")