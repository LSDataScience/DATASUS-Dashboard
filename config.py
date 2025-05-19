# config.py

from datetime import datetime

# FTP do DATASUS
host = "ftp.datasus.gov.br"

# Sistemas disponíveis
sistemas = ["CNES", "SIASUS", "SIHSUS"]

# Tipos de arquivos por sistema
tipos_por_sistema = {
    "CNES": ["LT"],
    "SIASUS": ["PA", "AR", "AQ"],
    "SIHSUS": ["RD", "SP"],
}

# Estado a ser baixado
estado = "SP"

# Período de interesse
ano_inicio = 2022
ano_atual = datetime.now().year
meses = [f"{m:02}" for m in range(1, 13)]

# Caminho base para salvar arquivos
diretorio_dados_sus = r"D:\DATASUS-Dados"

# Caminho base para exportação dos arquivos convertidos (CSV, DBF etc.)
diretorio_convertidos = r"D:\DATASUS-Convertidos"
