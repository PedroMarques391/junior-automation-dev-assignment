# Desafio Técnico — Desenvolvedor de Automação Júnior

## Instruções de Submissão

- **Entrega:** Repositório público no GitHub — envie o link por e-mail
- **Prazo:** Quinta-feira, 14/05/2026 às 12:00 (horário de Brasília)
- Commits realizados após o prazo desclassificarão a submissão
- Faça commits incrementais com mensagens claras — o histórico faz parte da avaliação

---

## Contexto

Você integra o time de automação de um departamento de faturamento hospitalar. Todo mês, a equipe executa manualmente um conjunto de tarefas que consome horas de trabalho. Seu objetivo é automatizar esse fluxo de ponta a ponta.

Os arquivos de trabalho estão na pasta `data/` deste repositório:

```
data/
├── cobrancas_internas.xlsx     ← planilha preenchida pela equipe interna
├── cobrancas_convenio.csv      ← exportação do sistema legado do convênio
└── laudos/                     ← laudos em PDF com nomes inconsistentes
    └── *.pdf
```

---

## Os Arquivos

### `cobrancas_internas.xlsx`

Planilha preenchida manualmente pela equipe com as cobranças do mês. Contém os campos:
`id_cobranca`, `paciente`, `registro_ans`, `procedimento`, `data_atendimento`, `valor`

Por ser preenchida à mão, pode conter erros de digitação — nomes truncados, valores incorretos, códigos ANS errados, descrições com typos.

---

### `cobrancas_convenio.csv`

Exportação do sistema legado do convênio. Separador: ponto-e-vírgula. Contém os mesmos registros que o Excel, mas com diferenças de formatação e campos adicionais:

| Campo | Descrição |
|---|---|
| `num_guia` | Identificador da cobrança |
| `nome_beneficiario` | Nome no formato `SOBRENOME, NOME`, em maiúsculas sem acento |
| `cpf_beneficiario` | CPF do paciente (não existe no Excel) |
| `ans` | Registro ANS do convênio |
| `nome_operadora` | Nome do convênio por extenso |
| `descricao_servico` | Procedimento em maiúsculas sem acento |
| `cod_tuss` | Código do procedimento na tabela TUSS (não existe no Excel) |
| `dt_realizacao` | Data no formato `YYYY-MM-DD` |
| `dt_lancamento` | Data de lançamento no sistema (não existe no Excel) |
| `vl_servico` | Valor bruto (decimal com vírgula) |
| `vl_glosa` | Valor glosado pelo convênio |
| `vl_liquido` | Valor líquido após glosa |

O sistema legado arredonda valores em múltiplos de R$ 0,25. O CSV pode ter cobranças a mais em relação ao Excel — registros que a equipe interna ainda não lançou. **O CSV é a fonte mais completa e confiável.**

---

### `laudos/*.pdf`

Laudos médicos nomeados de forma inconsistente pela equipe. Cada laudo pertence a um paciente e a um atendimento específico presentes nos arquivos de cobrança. O padrão de renomeação esperado pelo departamento é:

```
CPF-NOMEPACIENTE-IDCOBRANCA-MMYYYY.pdf
```

Exemplos:
- `10400032408-MARIAOLIVEIRA-COB001-112024.pdf`
- `00710022409-JOAOSOUSA-COB002-112024.pdf`

---

## O que precisa ser feito

### 1. Consolidar as cobranças

Leia os dois arquivos, normalize as diferenças de formato e consolide as informações em um único dataset. O dataset consolidado deve incorporar os campos exclusivos do CSV.

Identifique e registre em log todas as divergências encontradas:
- Cobranças presentes em apenas uma das fontes
- Diferenças de valor entre as fontes (use `vl_liquido` do CSV como referência)
- Diferenças de nome de paciente (indicativo de erro de digitação)
- Diferenças no código `registro_ans`

---

### 2. Verificar os registros ANS

Consulte o portal público da ANS para verificar a situação de cada `registro_ans` presente nas cobranças — incluindo os que parecem incorretos.

---

### 3. Renomear os laudos

Para cada PDF da pasta `laudos/`, identifique a qual paciente e cobrança ele pertence — usando os dados consolidados como referência — e renomeie para o padrão `CPF-NOMEPACIENTE-IDCOBRANCA-MMYYYY.pdf`.

O vínculo deve ser feito por similaridade entre o nome do arquivo e os nomes dos pacientes. Não hardcode mapeamentos. Nunca sobrescreva um arquivo já existente com o nome de destino.

---

### 4. Gerar o relatório Excel

Gere um arquivo `relatorio_faturamento_YYYYMM.xlsx` com no mínimo três seções:

**Resumo** — totais do processamento: cobranças por fonte, valor líquido total, total de glosas, situação dos registros ANS, resultado da renomeação dos laudos.

**Detalhamento** — todas as cobranças consolidadas com os campos enriquecidos (CPF, TUSS, datas, valores por fonte, nome da operadora, situação ANS, nome do PDF renomeado) e uma coluna descrevendo o que diverge em cada linha.

**Alertas** — apenas as cobranças que apresentam algum tipo de inconsistência (divergência de valor, nome, ANS inválido, fonte única).

Aplique formatação adequada: cabeçalhos destacados, alertas sinalizados visualmente, colunas com largura ajustada ao conteúdo.

---

### 5. Enviar o relatório por e-mail

Ao final do pipeline, envie por e-mail o relatório gerado como anexo. O corpo do e-mail deve estar em HTML e conter um resumo das informações principais.

Configure remetente, destinatário e credenciais SMTP via variáveis de ambiente (`.env`). Documente no README como configurar para envio real — pode usar Mailtrap ou Gmail com App Password para testes.

---

### 6. Automatizar a execução

Crie um script shell que execute o pipeline completo, registre logs com timestamp e encerre com código de saída `1` em caso de falha. Inclua, comentado no script, o comando cron necessário para execução automática toda segunda-feira às 06h30.

---

## Entrega

O repositório deve conter:

- **README** com instruções claras de instalação, configuração (`.env.example`) e execução
- Os arquivos de dados em `data/` (já fornecidos neste repositório)
- O código-fonte organizado da forma que você julgar mais adequada
- Os arquivos gerados **não** devem ser versionados (configure o `.gitignore`)

Não existe uma estrutura de pastas ou arquitetura obrigatória. Organize da forma que fizer mais sentido para você — isso faz parte do que será avaliado.

---

## O que será avaliado

- Corretude: o pipeline roda, produz os outputs esperados e detecta as inconsistências dos arquivos
- Qualidade do código: legibilidade, organização, ausência de repetição desnecessária
- Tratamento de erros: o pipeline é resiliente a dados ruins e falhas de rede
- Logs: mensagens úteis que permitem entender o que aconteceu em cada execução
- README: claro o suficiente para alguém reproduzir o ambiente do zero
- Histórico de commits: evidência de raciocínio incremental

> Estamos mais interessados em como você estrutura o raciocínio e lida com problemas reais do que em um código perfeito.
