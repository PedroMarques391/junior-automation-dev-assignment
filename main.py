import logging
from datetime import datetime

import src.loaders as loaders
import src.processing as processing

logger = logging.getLogger(__name__)

def main():
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f'logs/execution_{current_time}.log'

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    logger.info('Iniciando o processo de consolidação de cobranças...')
    
    convenio = loaders.DataLoader.load_data('data/cobrancas_convenio.csv')
    internas = loaders.DataLoader.load_data('data/cobrancas_internas.xlsx')

    convenio['nome_beneficiario'] = convenio['nome_beneficiario'].apply(processing.Processing.normalize_name)
    internas['paciente'] = internas['paciente'].apply(processing.Processing.normalize_name)

    convenio['vl_liquido'] = convenio['vl_liquido'].apply(processing.Processing.normalize_value_csv_to_float)
    internas['valor'] = internas['valor'].astype(float)

    internas = processing.Processing.rename_columns(internas, {"id_cobranca": "num_guia"})

    merged_df = processing.Processing.merge_dataFrames(convenio, internas, key='num_guia')

    merged_df['divergencias'] = merged_df.apply(processing.Processing.check_divergences, axis=1)

    merged_df.to_csv('data/merged_data.csv', index=False) 
    merged_df.to_excel('data/merged_data.xlsx', index=False) 
    
    logger.info('Processo finalizado.')

if __name__ == '__main__':
    main()