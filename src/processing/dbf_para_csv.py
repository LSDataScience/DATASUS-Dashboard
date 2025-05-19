import pandas as pd
from dbfread import DBF
import os

# Caminho da pasta
pasta_dbf = r"D:\DATASUS-Convertidos\CNES\DBF\LT"

# Lista todos os arquivos DBF na pasta
arquivos_dbf = [f for f in os.listdir(pasta_dbf) if f.lower().endswith(".dbf")]

# Lista para armazenar DataFrames
dataframes = []

# Itera pelos arquivos e lê cada um
for arquivo in arquivos_dbf:
    caminho_completo = os.path.join(pasta_dbf, arquivo)
    print(f"Lendo {arquivo} ...")
    df_temp = pd.DataFrame(iter(DBF(caminho_completo, encoding='latin1')))
    dataframes.append(df_temp)

# Concatena todos em um único DataFrame
df_consolidado = pd.concat(dataframes, ignore_index=True)

# Salva o DataFrame consolidado em CSV
df_consolidado.to_csv(r"D:\DATASUS-Convertidos\CNES\DBF\LT\CNES_LT_CONSOLIDADO.csv", index=False, sep=";", encoding="utf-8-sig")

print("Arquivos consolidados e CSV gerado com sucesso!")
