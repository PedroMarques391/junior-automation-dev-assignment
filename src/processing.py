from unidecode import unidecode
import re
import pandas as pd


class Processing:
    @staticmethod
    def normalize_name(name: str) -> str:
        if not isinstance(name, str):
            return ""

        name = unidecode(name).upper().strip()

        if ',' in name:
            partes = name.split(',')
            name = f"{partes[1].strip()} {partes[0].strip()}"
    
        name = re.sub(r'\s+', ' ', name)
    
        return name
    
    @staticmethod
    def normalize_value(value: int) -> str:
        intToFloat = round(float(value), 2)
        normalized_value = f"{intToFloat:.2f}".replace('.', ',')
        return normalized_value
            
    
    @staticmethod
    def merge_dataFrames(df1: pd.DataFrame, df2: pd.DataFrame, key: str) -> pd.DataFrame:
        merged_df = pd.merge(df1, df2, on=key, how="outer", indicator=True, suffixes=('_excel', '_csv'))
        return merged_df
    
    @staticmethod
    def rename_columns(df: pd.DataFrame, columns: dict) -> pd.DataFrame:
        return df.rename(columns=columns)
    