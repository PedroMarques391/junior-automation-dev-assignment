import pandas as pd


class DataLoader:
    
    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path, sep=';')
        
        return pd.read_excel(file_path)
