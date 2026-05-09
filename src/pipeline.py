from asyncio.log import logger

from src.loaders import DataLoader
from src.processing import Processing


class Pipeline:
    @staticmethod
    def step1():
        logger.info("====== step 1: load data ======")
        logger.info('Iniciando o processo de consolidação de cobranças...')
    
        convenio = DataLoader.load_data('data/cobrancas_convenio.csv')
        internas = DataLoader.load_data('data/cobrancas_internas.xlsx')

        convenio['nome_beneficiario'] = convenio['nome_beneficiario'].apply(Processing.normalize_name)
        internas['paciente'] = internas['paciente'].apply(Processing.normalize_name)

        convenio['vl_liquido'] = convenio['vl_liquido'].apply(Processing.normalize_value_csv_to_float)
        internas['valor'] = internas['valor'].astype(float)

        internas = Processing.rename_columns(internas, {"id_cobranca": "num_guia"})

        merged_df = Processing.merge_dataFrames(convenio, internas, key='num_guia')

        merged_df['divergencias'] = merged_df.apply(Processing.check_divergences, axis=1)

        merged_df.to_csv('data/merged_data.csv', index=False)

        logger.info(f'Arquivo salvo em: data/merged_data.csv')
            
        logger.info('Processo finalizado.')
        logger.info("====== step 1: finished ======")

        
        