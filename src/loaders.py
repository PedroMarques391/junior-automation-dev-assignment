import logging

import pandas as pd


class DataLoader:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def _load_csv(self, file_path: str) -> pd.DataFrame:
        self.logger.info(f"Carregando CSV: {file_path}")
        df = pd.read_csv(file_path, sep=';')
        self.logger.info(f"CSV lido com sucesso. Linhas: {len(df)}")
        return df
    
    def _load_excel(self, file_path: str) -> pd.DataFrame:
        self.logger.info(f"Carregando Excel: {file_path}")
        df = pd.read_excel(file_path)
        self.logger.info(f"Excel lido com sucesso. Linhas: {len(df)}")
        return df
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        if file_path.endswith('.csv'):
            df = self._load_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = self._load_excel(file_path)
        else:
            raise ValueError(f"Formato de arquivo não suportado: {file_path}")
        self.logger.info(f"Dados carregados com sucesso. Total de linhas: {len(df)}")
        return df
