import logging
import pandas as pd

logger = logging.getLogger(__name__)

class DataLoader:
    
    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        logger.info(f"Carregando dados de: {file_path}")
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, sep=';')
        else:
            df = pd.read_excel(file_path)
            
        logger.info(f"Dados carregados com sucesso de {file_path}. Total de linhas: {len(df)}")
        return df
