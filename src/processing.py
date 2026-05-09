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
    def normalize_value_csv_to_float(value) -> float:
        if pd.isna(value):
            return 0.0
        if isinstance(value, str):
            value = value.replace('.', '').replace(',', '.')
            return float(value)
        return float(value)
            
    
    @staticmethod
    def merge_dataFrames(df1: pd.DataFrame, df2: pd.DataFrame, key: str) -> pd.DataFrame:
        merged_df = pd.merge(df1, df2, on=key, how="outer", indicator=True)
        return merged_df
    
    @staticmethod
    def rename_columns(df: pd.DataFrame, columns: dict) -> pd.DataFrame:
        return df.rename(columns=columns)
    
    @staticmethod
    def check_divergences(row: pd.Series) -> str :
        notes = []
        if row['_merge'] == 'right_only':
            notes.append("Não encontrado no sistema do convênio")
        elif row['_merge'] == 'left_only':
            notes.append("Não lançado na planilha interna")
        elif row['_merge'] == 'both':
            if float(row['vl_liquido']) != float(row['valor']):
                notes.append(f"Divergência de valor: CSV {row['vl_liquido']} vs Excel {row['valor']}")
            if row['nome_beneficiario'] != row['paciente']:
                notes.append("Nome do paciente com erro de digitação")
            if str(row['ans']) != str(row['registro_ans']):
                notes.append("Divergência no código de convênio")
                
        return " | ".join(notes)
    