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
        
   