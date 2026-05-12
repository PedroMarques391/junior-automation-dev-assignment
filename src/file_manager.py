import logging
import os
import re
from pathlib import Path

import pandas as pd
from pypdf import PdfReader
from rapidfuzz import fuzz, process

from src.utils.file_utils import FileUtils
from src.utils.normalize_utils import NormalizeUtils


class FileManager:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        
    def _reader_pdf(self, file_path: str) -> str:
        self.logger.info(f'Carregando arquivo: {file_path}')
        pdf_reader = PdfReader(file_path).pages[0].extract_text()
        match = re.search(r'COB\d+', pdf_reader)
        if match:
            self.logger.info(f'Arquivo carregado com sucesso: {file_path}')
            return match.group(0)
        return ""
        
    def create_pdf_names_list(self, folder_path: str) -> list:
        pdf_names = []
        self.logger.info(f'Criando lista de nomes de arquivos PDF...')
        for file in Path(folder_path).glob('*.pdf'):
            name = Path(file).stem
            normalized_name = NormalizeUtils.normalize_name(name)
            pdf_names.append(normalized_name) 
        self.logger.info(f'Lista de nomes de arquivos PDF criada: {pdf_names}')
        return pdf_names 
    
    def rename_pdf_files(self, folder_path: str, output_folder: str, df_data: pd.DataFrame, min_score: float = 75.0):
        results: list[dict] = []
        new_df = df_data.copy()
        new_df['arquivo_renomeado'] = None
        
        output_path = Path(output_folder)
        FileUtils.create_directory(output_path)
        
        unique_clients = df_data['key'].dropna().unique().tolist()
        
        for file_path in Path(folder_path).glob('*.pdf'):
            original_file = file_path.name
            normalized_name = NormalizeUtils.normalize_name(file_path.stem)

            patient_match = process.extractOne(
                normalized_name,
                unique_clients,
                scorer=fuzz.token_set_ratio, 
                score_cutoff=min_score,
            )        
           
            if patient_match is None:
                self.logger.warning(f"Sem match de paciente para: '{original_file}'")
                results.append({
                    "arquivo_original": original_file,
                    "arquivo_renomeado": None,
                    "status": "não renomeado",
                    "renomeados": False,
                    "score": None,
                })
                continue 
        
            patient_found, patient_score, _ = patient_match
            
            patient_df = df_data[df_data['key'] == patient_found].copy()
            patient_df['search_string'] = patient_df['descricao_servico'] + " " + patient_df['dt_realizacao'].str.replace("-", " ")
            charges_list = patient_df['search_string'].tolist()
            
            charge_match = process.extractOne(
                normalized_name, 
                charges_list, 
                scorer=fuzz.partial_ratio
            )
            
            if not charge_match:
                self.logger.warning(f"Sem match de cobrança para: '{original_file}'")
                results.append({
                    "arquivo_original": original_file,
                    "arquivo_renomeado": None,
                    "status": "não renomeado",
                    "renomeados": False,
                    "score": patient_score,
                })
                continue
                
            charge_found, charge_score, _ = charge_match
            row = patient_df[patient_df['search_string'] == charge_found].iloc[0]
            
            cpf = str(row["cpf_beneficiario"]).replace(".", "").replace("-", "")
            patient_name = str(row["nome_beneficiario"]).replace(" ", "")
            charge_id = str(row["num_guia"])
            
            try:
                date_obj = pd.to_datetime(row["dt_realizacao"])
                mm_yyyy = date_obj.strftime("%m%Y")
            except Exception as e:
                self.logger.error(f"Erro ao converter data de {charge_id}: {e}")
                results.append({
                    "arquivo_original": original_file,
                    "arquivo_renomeado": None,
                    "status": "não renomeado",
                    "renomeados": False,
                    "score": patient_score,
                })
                continue

            new_name = f"{cpf}-{patient_name}-{charge_id}-{mm_yyyy}.pdf"
            destination = output_path / new_name
            new_df.loc[row.name, 'arquivo_renomeado'] = new_name
            
            if destination.exists():
                self.logger.warning(f"Destino já existe, pulando: '{new_name}'")
                results.append({
                    "arquivo_original": original_file,
                    "arquivo_renomeado": new_name,
                    "status": "não renomeado",
                    "renomeados": False,
                    "score": patient_score,
                })
                continue

            try:
                FileUtils.copy_file(file_path, destination) 
                self.logger.info(f"'{original_file}' → '{new_name}' (score {patient_score:.1f})")
                results.append({
                    "arquivo_original": original_file,
                    "arquivo_renomeado": new_name,
                    "status": "renomeado",
                    "renomeados": True,
                    "score": patient_score,
                })
            except Exception as e:
                self.logger.error(f"Falha ao copiar '{original_file}' para '{new_name}': {e}")
                results.append({
                    "arquivo_original": original_file,
                    "arquivo_renomeado": None,
                    "status": "não renomeado",
                    "renomeados": False,
                    "score": patient_score,
                })
            
        new_df.to_csv('data/generated_csv/data_with_renamed_files.csv', index=False)
        return results
