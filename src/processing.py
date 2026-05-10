import logging
import re

import pandas as pd
from unidecode import unidecode

logger = logging.getLogger(__name__)

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
    def normalize_value_csv_to_float(value) -> float:
        if pd.isna(value):
            return 0.0
        if isinstance(value, str):
            value = value.replace('.', '').replace(',', '.')
            return float(value)
        return float(value)
            
    
    @staticmethod
    def merge_dataFrames(df1: pd.DataFrame, df2: pd.DataFrame, key: str) -> pd.DataFrame:
        logger.info(f"Iniciando o cruzamento dos dados (merge) utilizando a chave '{key}'...")
        merged_df = pd.merge(df1, df2, on=key, how="outer", indicator=True)
        merged_df['key'] = merged_df['nome_beneficiario'].apply(Processing.normalize_name)
        return merged_df 
     
    @staticmethod
    def rename_columns(df: pd.DataFrame, columns: dict) -> pd.DataFrame:
        logger.info(f"Renomeando colunas: {columns}")
        return df.rename(columns=columns)
    
    @staticmethod
    def check_divergences(row: pd.Series) -> str :
        notes = []
        if row['_merge'] == 'right_only':
            notes.append("Não encontrado no sistema do convênio")
            logger.error(f"Não encontrado no sistema do convênio: {row}")
        elif row['_merge'] == 'left_only':
            notes.append("Não lançado na planilha interna")
            logger.error(f"Não lançado na planilha interna: {row}")
        elif row['_merge'] == 'both':
            if float(row['vl_liquido']) != float(row['valor']):
                notes.append(f"Divergência de valor: CSV {row['vl_liquido']} vs Excel {row['valor']}")
                logger.warning(f"Divergência de valor: CSV {row['vl_liquido']} vs Excel {row['valor']}")
                logger.warning(f"Diferença: R$ {float(row['valor']) - float(row['vl_liquido'])}")
            if row['nome_beneficiario'] != row['paciente']:
                notes.append("Nome do paciente com erro de digitação")
                logger.warning(f"Nome do paciente com erro de digitação: {row['nome_beneficiario']} vs {row['paciente']}")
            if str(row['ans']) != str(row['registro_ans']):
                notes.append("Divergência no código de convênio")
                logger.warning(f"Divergência no código de convênio: {row['ans']} vs {row['registro_ans']}")
                
        return " | ".join(notes)
    