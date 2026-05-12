#!/bin/bash
LOG_FILE="$PROJECT_DIR/logs/shell/execution_$(date +%Y-%m-%d_%H-%M-%S).log"

if !command -v python &> /dev/null; then
    echo "Python não encontrado" >> "$LOG_FILE"
    exit 1
fi


if !command -v pip &> /dev/null; then
    echo "Pip não encontrado" >> "$LOG_FILE"
    exit 1
fi


PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROGRAM_LOG_FILE="$PROJECT_DIR/logs/"
VENV_PATH="$PROJECT_DIR/.venv/bin/activate"

mkdir -p "$(dirname "$LOG_FILE")"

echo "Iniciando Pipeline: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"


if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    echo "Ambiente virtual ativado com sucesso" >> "$LOG_FILE"
else
    echo "Ambiente virtual não encontrado em $VENV_PATH, instalando agora" >> "$LOG_FILE"
    python3 -m venv .venv
    source "$VENV_PATH"
fi


if [ -d "/data/" ]; then
    echo "Os arquivos já estão descompactados"
else
    unzip -o data.zip 
    echo "Os arquivos foram descompactados com sucesso"
fi


if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements.txt" >> "$LOG_FILE" 2>&1
    echo "Dependências instaladas com sucesso" >> "$LOG_FILE"
else
    echo "Arquivo requirements.txt não encontrado em $PROJECT_DIR" >> "$LOG_FILE"
    exit 1
fi


python3 "$PROJECT_DIR/main.py" >> "$LOG_FILE" 2>&1


if [ $? -eq 0 ]; then
    echo "[SUCCESS] Pipeline finalizado com sucesso em $(date '+%H:%M:%S')" >> "$LOG_FILE"
    echo "logs de main.py disponíveis em $PROGRAM_LOG_FILE" >> "$LOG_FILE"
    exit 0
else
    echo "[CRITICAL] Falha na execução do pipeline em $(date '+%H:%M:%S')" >> "$LOG_FILE"
    exit 1
fi


# 30 06 * * 1 /bin/bash $PROJECT_DIR/run.sh