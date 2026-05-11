#!/bin/bash

# Verificando se o Python está instalado

if ! command -v python &> /dev/null; then
    echo "Python não encontrado" >> "$LOG_FILE"
    exit 1
fi

# Verificando se o pip está instalado

if ! command -v pip &> /dev/null; then
    echo "Pip não encontrado" >> "$LOG_FILE"
    exit 1
fi

# Configurações iniciais

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$PROJECT_DIR/logs/shell/execution_$(date +%Y-%m-%d_%H-%M-%S).log"
VENV_PATH="$PROJECT_DIR/venv/bin/activate"

# Cria o diretório de logs se não existir

mkdir -p "$(dirname "$LOG_FILE")"

echo "Iniciando Pipeline: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

# Ativando o ambiente virtual

if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    echo "Ambiente virtual ativado com sucesso" >> "$LOG_FILE"
else
    echo "Ambiente virtual não encontrado em $VENV_PATH" >> "$LOG_FILE"
    exit 1
fi

# Descompactando os arquivos zipados

if [ -d "/data/" ]; then
    echo "Os arquivos já estão descompactados"
else
    unzip data.zip -d data
    echo "Os arquivos foram descompactados com sucesso"
fi

## Executando o Script

python3 "$PROJECT_DIR/main.py" >> "$LOG_FILE" 2>&1

# Verificando o código de saída

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Pipeline finalizado com sucesso em $(date '+%H:%M:%S')" >> "$LOG_FILE"
    exit 0
else
    echo "[CRITICAL] Falha na execução do pipeline em $(date '+%H:%M:%S')" >> "$LOG_FILE"
    exit 1
fi