from pathlib import Path

import pandas as pd

from src.file_manager import FileManager
from src.loaders import DataLoader
from src.mailer import Mailer
from src.processing import Processing
from src.reporter import Reporter
from src.utils.file_utils import FileUtils
from src.utils.normalize_utils import NormalizeUtils


class Pipeline:
    def __init__(self, logger):
        self.logger = logger
        self.data_loader = DataLoader(self.logger)
        self.processing = Processing(self.logger)
        self.file_manager = FileManager(self.logger)
        self.mailer = Mailer(self.logger)

    def step1(self):
        self.logger.info("====== step 1: load data ======")
        self.logger.info('Iniciando o processo de consolidação de cobranças...')
        
        FileUtils.create_directory(f'{Path.cwd()}/data/generated_csv')
        

        convenio = self.data_loader.load_data('data/cobrancas_convenio.csv')
        internas = self.data_loader.load_data('data/cobrancas_internas.xlsx')

        convenio['nome_beneficiario'] = convenio['nome_beneficiario'].apply(NormalizeUtils.normalize_name)
        internas['paciente'] = internas['paciente'].apply(NormalizeUtils.normalize_name)
        
        convenio['ans'] = convenio['ans'].astype('Int64')
        internas['registro_ans'] = internas['registro_ans'].astype('Int64')

        convenio['vl_liquido'] = convenio['vl_liquido'].apply(NormalizeUtils.normalize_value_csv_to_float)
        internas['valor'] = internas['valor'].astype(float)

        internas = NormalizeUtils.rename_columns(internas, {"id_cobranca": "num_guia"})

        merged_df = self.processing.merge_dataFrames(convenio, internas, key='num_guia')

        merged_df['divergencias'] = merged_df.apply(self.processing.check_divergences, axis=1)

        merged_df.to_csv('data/generated_csv/merged_data.csv', index=False)

        self.logger.info(f'Arquivo salvo em: data/generated_csv/merged_data.csv')
            
        self.logger.info('Processo finalizado.')
        self.logger.info("====== step 1: finished ======")

    def step2(self):
        merged_df = pd.read_csv('data/generated_csv/merged_data.csv')
        self.logger.info("====== step 2: rename pdf files ======")
        self.logger.info('Iniciando o processo de renomeação de arquivos pdf...')
    
        results = self.file_manager.rename_pdf_files('data/laudos', 'data/laudos_renomeados', merged_df)
        self.logger.info(f'Arquivo salvo em: data/laudos_renomeados')
            
        self.logger.info('Processo finalizado.')
        self.logger.info("====== step 2: finished ======")
      
    def step3(self):
        self.logger.info("====== step 3: generate report ======")
        self.logger.info('Iniciando o processo de geração de relatórios...')
        
        df = pd.read_csv("data/generated_csv/data_with_renamed_files.csv")
        reporter = Reporter(df, "data/relatorio")
        reporter.generate_report()
              
        self.logger.info('Processo finalizado.')
        self.logger.info("====== step 3: finished ======")
        
    def step4(self):
        self.logger.info("====== step 4: send email ======")
        self.logger.info('Iniciando o processo de envio de e-mail...')
        
        report_files = list(Path(f"{Path.cwd()}/data/relatorio/").glob("*.xlsx"))
        report_df = pd.read_excel(report_files[-1])
        normalize_dict = dict(zip(report_df['Descrição'], report_df['Valor']))
        
        self.mailer.send_email(normalize_dict, report_files[-1])
        self.logger.info(f'E-mail enviado com sucesso para: {self.mailer.to_email}') 
        
        self.logger.info('Processo finalizado.')
        self.logger.info("====== step 4: finished ======")

    def run(self):
        self.step1()
        self.step2()
        self.step3()
        self.step4()