import os
import re
from pathlib import Path

import pandas as pd
from pypdf import PdfReader
from unidecode import unidecode


class FileManager:
    @staticmethod 
    def _reader_pdf(file_path: str) -> str:
        pdf_reader = PdfReader(file_path).pages[0].extract_text()
        match = re.search(r'COB\d+', pdf_reader)
        if match:
            return match.group(0)
        return None
    
    @staticmethod
    def normalize_pdf_name(file_name: str) -> str:
        name = unidecode(file_name).upper().strip()
        name = re.sub(r'\s+', ' ', name)
        return name
        
    @classmethod
    def create_pdf_names_list(cls, folder_path: str) -> list:
        pdf_names = []
        for file in Path(folder_path).glob('*.pdf'):
            name = Path(file).stem
            normalized_name = cls.normalize_pdf_name(name)
            pdf_names.append(normalized_name) 
        return pdf_names 