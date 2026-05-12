import logging
import shutil
from importlib import resources
from pathlib import Path


class FileUtils:
    @staticmethod
    def create_directory(path: str | Path) -> None:
        try:
            dir_path = Path(path)
            dir_path.mkdir(parents=True, exist_ok=True)
            logging.info(f"Diretório verificado/criado com sucesso: {dir_path}")
        except Exception as e:
            logging.error(f"Erro ao criar/verificar diretório {path}: {e}")
            raise

    @staticmethod
    def copy_file(source: str | Path, destination: str | Path) -> bool:
        try:
            shutil.copy2(source, destination)
            return True
        except FileNotFoundError:
            logging.error(f"Arquivo não encontrado para cópia: {source}")
            return False
        except PermissionError:
            logging.error(f"Sem permissão para copiar {source} para {destination}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado ao copiar {source} para {destination}: {e}")
            return False
