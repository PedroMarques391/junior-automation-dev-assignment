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
    logger.info('Dados do convênio (CSV) carregados com sucesso.')
    
    internas = loaders.DataLoader.load_data('data/cobrancas_internas.xlsx')
    logger.info('Dados internos (Excel) carregados com sucesso.')

    convenio['nome_beneficiario'] = convenio['nome_beneficiario'].apply(processing.Processing.normalize_name)
    logger.info('Nomes de beneficiários do convênio normalizados.')
    
    internas['paciente'] = internas['paciente'].apply(processing.Processing.normalize_name)
    logger.info('Nomes de pacientes internos normalizados.')

    convenio['vl_liquido'] = convenio['vl_liquido'].apply(processing.Processing.normalize_value_csv_to_float)
    internas['valor'] = internas['valor'].astype(float)
    logger.info('Valores financeiros convertidos e normalizados.')

    internas = processing.Processing.rename_columns(internas, {"id_cobranca": "num_guia"})

    logger.info('Iniciando o cruzamento dos dados (merge)...')
    merged_df = processing.Processing.merge_dataFrames(convenio, internas, key='num_guia')

    logger.info('Verificando divergências entre as fontes de dados...')
    merged_df['divergencias'] = merged_df.apply(processing.Processing.check_divergences, axis=1)

    merged_df.to_csv('data/merged_data.csv', index=False) 
    merged_df.to_excel('data/merged_data.xlsx', index=False) 
    logger.info('Dados consolidados e exportados com sucesso em CSV e Excel.')
    
    logger.info('Processo finalizado.')

if __name__ == '__main__':
    main()