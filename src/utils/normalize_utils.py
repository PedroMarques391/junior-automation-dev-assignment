import logging
import re

import pandas as pd
from unidecode import unidecode


class NormalizeUtils:
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
    def normalize_value_csv_to_float(value) -> float:
        if pd.isna(value):
            return 0.0
        if isinstance(value, str):
            value = value.replace('.', '').replace(',', '.')
            return float(value)
        return float(value)
    
    @staticmethod
    def rename_columns(df: pd.DataFrame, columns: dict) -> pd.DataFrame:
        return df.rename(columns=columns)
            