@echo off
echo "Verificando pasta de dependencias do Oracle..."

IF NOT EXIST "C:\oracle" (

	echo "Pasta C:\oracle nao encontrada."
	echo "Criando pasta e copiando arquivos (isso deve demorar alguns segundos)..."

	md "C:\oracle"

	xcopy /e /y /q "\\brafps01.corp2000.org\Share\SCSC\Sistema\MyScanSource\oracle" "C:\oracle"

	echo "Copia dos arquivos concluidas, iniciando programa de criacao de usuarios"
) ELSE (
	echo "Pasta C:\oracle ja existe. Iniciando programa para geracao de relatorios, por favor aguarde..."
)

py -m pip install oracledb -q
py -m pip install tqdm -q
py -m pip install openpyxl -q

echo --------------------------------------------------

py "%~dp0relatorio_oracle.py"

pause