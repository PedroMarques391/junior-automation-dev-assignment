import logging

import pandas as pd

logger = logging.getLogger(__name__)

class DataLoader:
    
    @staticmethod
    def _load_csv(file_path: str) -> pd.DataFrame:
        logger.info(f"Carregando CSV: {file_path}")
        df = pd.read_csv(file_path, sep=';')
        logger.info(f"CSV lido com sucesso. Linhas: {len(df)}")
        return df
    
    @staticmethod
    def _load_excel(file_path: str) -> pd.DataFrame:
        logger.info(f"Carregando Excel: {file_path}")
        df = pd.read_excel(file_path)
        logger.info(f"Excel lido com sucesso. Linhas: {len(df)}")
        return df
    
    @classmethod
    def load_data(cls, file_path: str) -> pd.DataFrame:
        if file_path.endswith('.csv'):
            df = cls._load_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = cls._load_excel(file_path)
        else:
            raise ValueError(f"Formato de arquivo não suportado: {file_path}")
        logger.info(f"Dados carregados com sucesso. Total de linhas: {len(df)}")
        return df
        
