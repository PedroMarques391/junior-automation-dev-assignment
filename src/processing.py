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
    def merge_dataFrames(df1: pd.DataFrame, df2: pd.DataFrame, key1: str, key2: str) -> pd.DataFrame:
        merged_df = pd.merge(df1, df2, left_on=key1, right_on=key2, how='outer')
        return merged_df
    
    @staticmethod
    def rename_columns(df: pd.DataFrame, columns_mapping: dict) -> pd.DataFrame:
        return df.rename(columns=columns_mapping)