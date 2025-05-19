"""
================================================================================
    download_dados_sus.py
================================================================================
    Descrição:
        Realiza download automatizado de arquivos DBC dos sistemas CNES, SIASUS
        e SIHSUS a partir do FTP do DATASUS, organizando-os por sistema, tipo e
        ano/mês, conforme configurações centralizadas.

    Autor:        Luccas Silva
    Versão:       1.2.0
    Data criação: 19/05/2025
    Atualização:  19/05/2025

    Dependências:
        - ftplib
        - os
        - datetime
        - config.py

================================================================================
"""

from ftplib import FTP
import os
from config import (
    host,
    sistemas,
    tipos_por_sistema,
    estado,
    ano_inicio,
    ano_atual,
    meses,
    diretorio_dados_sus,
)

# ========================================================================
# Funções
# ========================================================================

def listar_arquivos_ftp(ftp, sistema):
    """
    Lista arquivos disponíveis no FTP para o sistema informado.

    Parâmetros:
        ftp (ftplib.FTP): Conexão FTP ativa.
        sistema (str): Nome do sistema (CNES, SIASUS, SIHSUS).

    Retorna:
        list: Lista de nomes de arquivos disponíveis.
    """
    try:
        if sistema == "CNES":
            ftp.cwd(f"/dissemin/publicos/{sistema}/200508_/Dados/LT/")
        else:
            ftp.cwd(f"/dissemin/publicos/{sistema}/200801_/Dados/")
        return ftp.nlst()
    except Exception as e:
        print(f"[!] Erro ao listar arquivos para o sistema {sistema}: {e}")
        return []

def baixar_arquivo(ftp, nome_arquivo, caminho_arquivo):
    """
    Baixa um arquivo do FTP e salva no caminho local especificado.

    Parâmetros:
        ftp (ftplib.FTP): Conexão FTP ativa.
        nome_arquivo (str): Nome do arquivo a baixar.
        caminho_arquivo (str): Caminho local completo para salvar o arquivo.
    """
    try:
        with open(caminho_arquivo, "wb") as f:
            print(f"[↓] Baixando: {nome_arquivo}")
            ftp.retrbinary(f"RETR {nome_arquivo}", f.write)
        print(f"[✔] Arquivo salvo em: {caminho_arquivo}")
    except Exception as e:
        print(f"[!] Erro ao baixar {nome_arquivo}: {e}")

# ========================================================================
# Execução principal
# ========================================================================

def main():
    ftp = FTP(host)
    ftp.login()

    for sistema in sistemas:
        print(f"\n[INFO] Processando sistema: {sistema}")

        arquivos_ftp = listar_arquivos_ftp(ftp, sistema)
        tipos = tipos_por_sistema.get(sistema, [])

        for tipo in tipos:
            for ano in range(ano_inicio, ano_atual + 1):
                for mes in meses:
                    base_sigla = f"{tipo}{estado}{str(ano)[-2:]}{mes}"
                    pasta_destino = os.path.join(diretorio_dados_sus, sistema, tipo)
                    os.makedirs(pasta_destino, exist_ok=True)

                    if tipo == "PA":
                        for sufixo in "abcdefghijklmnopqrstuvwxyz":
                            nome_arquivo = f"{base_sigla}{sufixo}.dbc"
                            caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
                            if nome_arquivo in arquivos_ftp:
                                if not os.path.exists(caminho_arquivo):
                                    baixar_arquivo(ftp, nome_arquivo, caminho_arquivo)
                                else:
                                    print(f"[✓] Já existe: {nome_arquivo}")
                            else:
                                break
                    else:
                        nome_arquivo = f"{base_sigla}.dbc"
                        caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
                        if nome_arquivo in arquivos_ftp:
                            if not os.path.exists(caminho_arquivo):
                                baixar_arquivo(ftp, nome_arquivo, caminho_arquivo)
                            else:
                                print(f"[✓] Já existe: {nome_arquivo}")
                        else:
                            print(f"[!] Arquivo não encontrado no FTP: {nome_arquivo}")

    ftp.quit()
    print("\n[✔] Download concluído.")

if __name__ == "__main__":
    main()
# ========================================================================
# Fim do script