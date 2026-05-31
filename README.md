# Export Heavy Reports 

Programa para exportar dados de grandes volumes de banco de dados (Oracle e SQL Server) sem perder a conexão e com suporte a retomada de processo.

## 📋 Sobre o Projeto

Este projeto foi criado para resolver dois problemas críticos:

### 1. **relatorio_oracle.py** - Queries pesadas do Oracle
- Executa queries absurdamente pesadas que demoram **mais de 10 horas**
- Usa **modo Thick** do Oracle (requerido para Oracle 11g)
- **Sistema de checkpoint**: Salva progresso a cada lote processado
- **Retry automático**: Reconecta automaticamente em caso de falha de conexão
- Exporta dados para arquivo Excel com streaming (economiza memória)

### 2. **relatorio_mssql.py** - Exportação de grandes tabelas SQL Server
- Exporta planilhas com **mais de 1.000.000 de registros**
- Processa dados em **chunks** para evitar consumo excessivo de memória
- Exporta dados para arquivo CSV
- Suporta autenticação por Trusted Connection ou credenciais

## ⚙️ Configuração

### Arquivo .env (variáveis de ambiente)

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
# Oracle
ORACLE_CLIENT_PATH=C:\oracle\instantclient_23_9
ORACLE_DSN=servidor:porta/banco_de_dados
ORACLE_USER=
ORACLE_PASSWORD=

# MSSQL
MSSQL_SERVER=servidor
MSSQL_DATABASE=banco_de_dados
MSSQL_TABLE=tabela
MSSQL_TRUSTED_CONNECTION=yes

# Arquivos de saída
ORACLE_OUTPUT_FILE=relatorio.xlsx
ORACLE_LOG_FILE=console.log
ORACLE_CHECKPOINT_FILE=checkpoint.txt
MSSQL_OUTPUT_FILE=output.csv

# Performance
ORACLE_FETCH_SIZE=5000
ORACLE_MAX_RETRIES=5
ORACLE_RETRY_WAIT=30
MSSQL_CHUNK_SIZE=100000
```

#### Parâmetros:

| Parâmetro | Descrição | Padrão |
|-----------|-----------|--------|
| `ORACLE_CLIENT_PATH` | Caminho do Oracle Instant Client (Thick Mode) | `C:\oracle\instantclient_23_9` |
| `ORACLE_DSN` | String de conexão Oracle (servidor:porta/banco) | `server:port/database` |
| `ORACLE_USER` | Usuário Oracle (deixe vazio para pedir interativamente) | `` |
| `ORACLE_PASSWORD` | Senha Oracle (deixe vazio para pedir interativamente) | `` |
| `MSSQL_SERVER` | Nome/IP do servidor SQL Server | `server_name` |
| `MSSQL_DATABASE` | Banco de dados SQL Server | `database_name` |
| `MSSQL_TABLE` | Tabela SQL Server para exportar | `table_name` |
| `MSSQL_TRUSTED_CONNECTION` | Usar autenticação Windows? (`yes`/`no`) | `yes` |
| `ORACLE_FETCH_SIZE` | Quantidade de linhas por lote (Oracle) | `5000` |
| `ORACLE_MAX_RETRIES` | Máximo de tentativas de reconexão | `5` |
| `ORACLE_RETRY_WAIT` | Segundos para aguardar antes de reconectar | `30` |
| `MSSQL_CHUNK_SIZE` | Quantidade de linhas por chunk (MSSQL) | `100000` |

## 📦 Instalação de Dependências

### Requisitos
- Python 3.7+
- ODBC Driver 17 for SQL Server (para MSSQL)
- Oracle Instant Client (para Oracle)

### Instalar pacotes Python

```bash
pip install -r requirements.txt
```

## 🚀 Como Usar

### Oracle (relatorio_oracle.py)

#### Opção 1: Usar o script batch (Windows)

```bash
rodar_script.bat
```

Este script irá:
- Verificar e copiar os arquivos do Oracle Instant Client
- Instalar dependências Python necessárias
- Executar o programa

#### Opção 2: Executar diretamente com Python

```bash
python relatorio_oracle.py
```

**O programa pedirá interativamente:**
1. Usuário Oracle
2. Senha Oracle

**Saídas:**
- `relatorio.xlsx` - Arquivo com os dados exportados
- `console.log` - Log detalhado de execução
- `checkpoint.txt` - Arquivo de progresso (criado automaticamente)

#### Recursos:
- ✅ Sistema de checkpoint automático
- ✅ Retomada de processo em caso de falha
- ✅ Barra de progresso em tempo real
- ✅ Retry automático com aguardo
- ✅ Logs detalhados para debug

### SQL Server (relatorio_mssql.py)

```bash
python relatorio_mssql.py
```

**O programa:**
1. Lê a configuração do `.env`
2. Pede credenciais se `MSSQL_TRUSTED_CONNECTION=no`
3. Exporta dados em chunks para `MSSQL_OUTPUT_FILE`

**Saída:**
- Arquivo CSV com separador `;` e encoding UTF-8

## 📝 Modificando as Queries

### Para Oracle (relatorio_oracle.py)

Edite o arquivo `relatorio_oracle.py` e procure pela seção `CONFIGURAÇÕES`:

```python
QUERY = """
SELECT A.DATA, A.REVIDE, A.PEDIDO
    FROM SCHEMA.TABLE A
ORDER BY DATANF DESC
"""
```

### Para SQL Server (relatorio_mssql.py)

A query padrão seleciona todas as colunas. Para customizar, edite o arquivo `relatorio_mssql.py`:

```python
query = f"""
SELECT *
FROM
    {DATABASE}.dbo.{TABLE}
"""
```

## 🔍 Monitoramento

### Oracle

Durante a execução do `relatorio_oracle.py`:
- Uma barra de progresso mostra quantas linhas foram exportadas
- O arquivo `console.log` registra todos os eventos
- O arquivo `checkpoint.txt` é atualizado a cada lote (para retomar depois)

### SQL Server

Durante a execução do `relatorio_mssql.py`:
- Console exibe quantas linhas foram exportadas
- Arquivo CSV é gerado incrementalmente

## ⚠️ Tratamento de Erros

### Oracle

Se a conexão cair:
1. O programa tenta reconectar automaticamente
2. Se falhar, aguarda `ORACLE_RETRY_WAIT` segundos e tenta novamente
3. Tenta até `ORACLE_MAX_RETRIES` vezes
4. O checkpoint permite retomar do ponto exato onde parou

### SQL Server

Em caso de erro:
- O programa encerra a execução
- Verifique as configurações de conexão no `.env`
- Certifique-se que o ODBC Driver 17 está instalado

## 📊 Performance

### Oracle
- `ORACLE_FETCH_SIZE`: Aumentar para 10000-50000 pode melhorar a velocidade, mas usar mais memória
- Recomendado: 5000-10000 para queries muito pesadas

### SQL Server
- `MSSQL_CHUNK_SIZE`: Aumentar para 500000-1000000 pode melhorar a velocidade
- Recomendado: 100000-500000 dependendo da memória disponível

## 🛠️ Troubleshooting

### Oracle: "ORA-12162: TNS:net service name is incorrectly specified"
- Verifique o formato de `ORACLE_DSN` no `.env`
- Formato correto: `servidor:porta/nome_banco`

### Oracle: "Instant Client not found"
- Certifique-se que `ORACLE_CLIENT_PATH` aponta para a pasta correta
- Se usar `rodar_script.bat`, verifique o caminho de cópia de arquivos

### SQL Server: "IM002: [Microsoft][ODBC Driver Manager] Data source name not found"
- Instale o ODBC Driver 17: https://docs.microsoft.com/pt-br/sql/connect/odbc/download-odbc-driver-for-sql-server

### SQL Server: "Login failed for user"
- Verifique usuário e senha no `.env`
- Se usar Trusted Connection, certifique-se que tem permissão na máquina

## 📄 Estrutura de Arquivos

```
export-heavy-reports/
├── config.py                    # Configurações centralizadas
├── relatorio_oracle.py          # Script de exportação Oracle
├── relatorio_mssql.py           # Script de exportação SQL Server
├── rodar_script.bat             # Script para executar Oracle (Windows)
├── requirements.txt             # Dependências Python
├── .env                         # Variáveis de ambiente (CRIAR)
└── README.md                    # Este arquivo
```

## 📌 Notas Importantes

1. **Checkpoint Oracle**: O arquivo `checkpoint.txt` é crítico. Não o delete até ter certeza que a exportação completou com sucesso!

2. **Credenciais**: Nunca comite o arquivo `.env` com credenciais no Git. Use `.gitignore`.

3. **Logs**: Verifique `console.log` para debug em caso de erros silenciosos.

4. **Modo Thick Oracle**: O `rodar_script.bat` configura automaticamente o Thick Mode para Oracle 11g.

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs (`console.log`)
2. Consulte a seção de Troubleshooting
3. Verifique se as variáveis de ambiente estão corretas no `.env`

---

**Versão**: 1.3  
**Data**: 2026-05-30  
**Python**: 3.7+