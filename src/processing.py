import logging

import pandas as pd

from src.utils.normalize_utils import NormalizeUtils

logger = logging.getLogger(__name__)

class Processing:
    @staticmethod
    def merge_dataFrames(df1: pd.DataFrame, df2: pd.DataFrame, key: str) -> pd.DataFrame:
        logger.info(f"Iniciando o cruzamento dos dados (merge) utilizando a chave '{key}'...")
        merged_df = pd.merge(df1, df2, on=key, how="outer", indicator=True)
        merged_df['key'] = merged_df['nome_beneficiario'].apply(NormalizeUtils.normalize_name)
        return merged_df 
    
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
                notes.append(f"Divergência de valor: CSV {row['vl_liquido']} vs Excel {row['valor']} = {float(row['valor']) - float(row['vl_liquido'])}")
                logger.warning(f"Divergência de valor: CSV {row['vl_liquido']} vs Excel {row['valor']}")
                logger.warning(f"Diferença: R$ {float(row['valor']) - float(row['vl_liquido'])}")
            if row['nome_beneficiario'] != row['paciente']:
                notes.append(f"Nome do paciente com erro de digitação: CSV {row['nome_beneficiario']} vs Excel {row['paciente']}")
                logger.warning(f"Nome do paciente com erro de digitação: {row['nome_beneficiario']} vs {row['paciente']}")
            if str(row['ans']) != str(row['registro_ans']):
                notes.append(f"Divergência no código de convênio: CSV {row['ans']} vs Excel {row['registro_ans']}")
                logger.warning(f"Divergência no código de convênio: {row['ans']} vs {row['registro_ans']}")
                
        return " | ".join(notes) if notes else "Ok"
    