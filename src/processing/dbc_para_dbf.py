import os
import logging
from datasus_dbc import decompress
import config

def configurar_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='w', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def converter_dbc_em_pasta(input_dir, output_dir):
    if not os.path.exists(input_dir):
        logging.warning(f"Pasta de entrada {input_dir} não existe. Pulando...")
        return

    os.makedirs(output_dir, exist_ok=True)

    arquivos_dbc = [f for f in os.listdir(input_dir) if f.lower().endswith('.dbc')]
    logging.info(f"{len(arquivos_dbc)} arquivos DBC encontrados em {input_dir}")

    for arquivo in arquivos_dbc:
        caminho_entrada = os.path.join(input_dir, arquivo)
        nome_sem_ext = os.path.splitext(arquivo)[0]
        caminho_saida = os.path.join(output_dir, nome_sem_ext + ".dbf")

        logging.info(f"Lendo {arquivo} ...")
        try:
            decompress(caminho_entrada, caminho_saida)
            logging.info(f"{arquivo} convertido para {nome_sem_ext}.dbf com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao processar {arquivo}: {e}")

def converter_todos_dbc():
    for sistema in config.sistemas:
        tipos = config.tipos_por_sistema.get(sistema, [])
        for tipo in tipos:
            # Monta caminho de entrada conforme padrão config
            input_dir = os.path.join(config.diretorio_dados_sus, sistema, tipo)
            output_dir = os.path.join(config.diretorio_convertidos, sistema, "DBF", tipo)

            logging.info(f"Iniciando conversão para sistema={sistema}, tipo={tipo}")
            converter_dbc_em_pasta(input_dir, output_dir)

    logging.info("Todas as conversões foram concluídas.")

if __name__ == "__main__":
    LOG_FILE = "dbc_to_dbf_conversion.log"
    configurar_logging(LOG_FILE)
    converter_todos_dbc()
