# Como executar o projeto manualmente

### Necessário ter o python instalado

## 1. Instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

## 2. Descompactar o zip de dados necessário:

```bash
unzip "data.zip"
```

## 3. Configurar variáveis de ambiente:

Copie o arquivo .env.example para .env e preencha as variáveis de ambiente:

```bash
cp .env.example .env
```

## 4. Executar a pipeline:

```bash
python main.py
```

## 5. Verificar os logs:

```bash
tail -f logs/execution_YYYY-MM-DD_HH-MM-SS.log
```

---

# Como executar o projeto com o shell script

## 1. Instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

## 2. Configurar variáveis de ambiente:

Copie o arquivo .env.example para .env e preencha as variáveis de ambiente:

```bash
cp .env.example .env
```

## 3. Configurar permissão de execução:

```bash
chmod +x run.sh
```

## 4. Executar a pipeline:

```bash
./run.sh
```

## 5. Verificar os logs:

```bash
tail -f logs/shell/execution_YYYY-MM-DD_HH-MM-SS.log
```
