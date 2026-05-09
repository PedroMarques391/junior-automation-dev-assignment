import os
import re
from pathlib import Path

from pypdf import PdfReader


class FileManager:
    @staticmethod 
    def _reader_pdf(file_path: str) -> str:
        pdf_reader = PdfReader(file_path).pages[0].extract_text()
        match = re.search(r'COB\d+', pdf_reader)
        if match:
            return match.group(0)
        return None
        
    @classmethod
    def create_guias_cob_list(cls, folder_path: str) -> list:
        pdf_files = Path(folder_path).glob('*.pdf')
        result = []
        for pdf_file in pdf_files:
            result.append(cls._reader_pdf(pdf_file))
        return result