# Questionário — Desenvolvedor de Automação Júnior

Responda este questionário no arquivo `RESPOSTAS.md` na raiz do seu repositório.

Não existe resposta certa ou errada. O objetivo é entender como você pensa, quais trade-offs você reconhece e como você comunica decisões técnicas. Seja direto e objetivo — respostas longas demais não valem mais pontos.

---

## Parte 1 — Sobre o que você construiu

**1.1** Descreva em até 5 linhas o que o seu pipeline faz, como se estivesse explicando para alguém da equipe de faturamento que não é técnico.

O pipeline lê as duas tabelas iniciais, normaliza nomes e valores, e junta as duas tabelas criando um CSV com cobranças internas e convênio. Após isso, percorre a pasta de laudos e compara os nomes dos PDFs com as colunas de nome, descrição e data de serviço para achar a que mais combina e poder renomeá-los. Em seguida, cria uma tabela com 3 seções: uma com resumo, uma com detalhes e outra com alertas. Essa tabela é usada na última etapa, quando enviamos por e-mail usando informações da seção resumo para preencher o corpo do e-mail.

---

**1.2** Qual foi a etapa mais difícil de implementar? O que tornou ela difícil e como você resolveu?

A etapa dois (renomear PDFs) foi a mais complicada porque não existia um padrão na nomenclatura original e, sem um padrão definido, a comparação era quase impossível. Para poder concluir, precisei fazer uma pequena normalização dos nomes, onde deixei todos em caixa alta (no CSV os nomes estão nesse formato) e separei data e exame. Como isso não bastaria para comparar, usei a RapidFuzz, que é uma biblioteca em Python que compara a similaridade de texto. Para esse caso, usei um score mínimo de 75%; ou seja, se as strings tivessem 75% de similaridade, o PDF era copiado e renomeado.

---

**1.3** A reconciliação entre o Excel e o CSV exigiu decisões sobre o que fazer quando os dados divergem. Descreva as principais decisões que você tomou:

- Quando o valor de uma cobrança difere entre as fontes, qual prevalece e por quê?
  - O CSV prevalece. A tabela em XLSX foi escrita manualmente, o que explica vários erros de digitação e registro, tornando o CSV mais confiável.

- O que você faz com uma cobrança que está só no CSV e não tem correspondente no Excel?
  - Todas as divergências estão registradas na tabela, na coluna de "Divergência", informando que não foi encontrado no sistema do convênio ou não foi encontrado na planilha interna.

- Como você identificou que dois registros se referem ao mesmo paciente mesmo com grafias diferentes?
  - Com os nomes normalizados e comparando a similaridade com RapidFuzz.

---

**1.4** Como você fez o vínculo entre os arquivos PDF e os registros de cobrança? Descreva a lógica de similaridade que usou, qual foi o maior risco dessa abordagem e como você o mitigou.

Eu normalizei os nomes dos PDFs que precisam ser renomeados e fiz a comparação de similaridade usando RapidFuzz. Para ter uma comparação mais assertiva, criei uma string que junta o nome com o procedimento e data de realização (campos normalmente usados na nomenclatura inicial dos PDFs). O maior risco é dar um match incorreto; tentei diminuir esse risco usando um match mínimo de 75%. Menos que isso, o sistema registra o erro e passa para o próximo..

---

**1.5** Houve algum dado nos arquivos que te surpreendeu ou que você não esperava encontrar? Como você tratou?

O que mais me surpreendeu foi a inconsistência nos campos de valores e nos nomes dos exames, que variavam entre siglas e nomes por extenso. Tratei isso criando uma camada de limpeza de dados logo no início do pipeline, onde padronizei as strings para caixa alta, removi acentuações e padronizei os valores para ponto flutuante (0.00). Isso garantiu que a lógica de comparação subsequente não fosse afetada por ruídos de digitação."

---

## Parte 2 — Sobre as decisões técnicas

**2.1** Por que você escolheu a linguagem e as bibliotecas que usou? Quais alternativas considerou e por que descartou?

Eu escolhi usar Python com Pandas e Openpyxl por serem o padrão de mercado para automação de dados. Além de ser Python ser uma linguagem que domino, o Pandas oferece recursos nativos de cruzado entre tabelas. Pensei em usar TypeScript com Node.js e ExcelJS, mas, embora JavaScript seja ótimo para muitas situações, o desenvolvimento de uma automação para análise de dados exigiria uma complexidade desnecessária.

---

**2.2** Como você organizou o código? Explique brevemente a estrutura que criou e por que ela faz sentido para este problema.

Eu organizei o código em camadas, onde cada classe é responsável por fazer algo específico; por ser uma pipeline, cada etapa depende da anterior:

```bash
    src/
      --- file_manager.py --> responsável pela manipulação de arquivos e PDFs.
      --- loaders.py --> responsável por ler as tabelas.
      --- mailer.py --> classe responsável pelo envio do e-mail usando smtplib.
      --- processing.py --> classe responsável por todo o processamento de dados (normalização, renomeação, verificação de divergências).
      --- pipeline.py --> responsável pela execução da pipeline e registro dos logs, dividida em 4 métodos (etapas) e um método principal que une todos.
      --- reporter.py --> classe responsável por gerar o relatório, com métodos para criar as seções e um método principal que consolida tudo usando openpyxl.
    main.py --> arquivo principal na raiz, responsável por inicializar os logs e executar a pipeline.
```

---

**2.3** O pipeline lida com arquivos que podem chegar com problemas. Para cada cenário abaixo, descreva o que acontece no seu código:

- O Excel chega com uma coluna faltando:

As duas tabelas são mescladas (merge) mantendo as colunas específicas. Como usamos o CSV como referência, uma coluna faltando no Excel não deve quebrar o processamento.

Uma linha do CSV tem o campo vl_liquido vazio ou com texto no lugar do valor:

Todos os valores são convertidos para float (para normalização). Se estiver vazio ou for uma string inválida, o valor torna-se 0.00.

Dois PDFs na pasta laudos/ têm nomes tão parecidos que o algoritmo de similaridade empata:

Quando os nomes são parecidos, ele compara com Nome + Exame. Se o empate persistir, ele compara com Nome + Exame + Data.

O pipeline roda duas vezes seguidas sem que os arquivos de entrada tenham mudado:

A parte crítica é a criação dos PDFs renomeados. Na primeira execução, todos são criados e salvos em data/laudos_renomeados. Na segunda execução, o programa verifica se o arquivo já existe no destino; se existir, ele pula. Além disso, o e-mail é enviado nas duas vezes, mas a segunda execução é instantânea, já que os arquivos já estão processados.

---

**2.4** Se o pipeline fosse rodar em produção todo mês com arquivos reais, o que você mudaria ou reforçaria em relação ao que entregou?

Eu garantiria que o processo fosse idempotente: se o pipeline cair na metade e eu rodar de novo, ele deve ser capaz de "limpar a sujeira" da tentativa anterior e recomeçar sem duplicar registros ou corromper arquivos.

---

**2.5** Tem alguma parte do código que você sabe que não está boa, mas deixou assim por limitação de tempo? O que está errado e como você corrigiria?

A organização dos esquemas de classes e construtores. Como eu iniciei rápido, não dei tanto foco em criar classes utilitárias como deveria. Além disso, o método para checar divergências pode ter ficado meio confuso, embora funcione perfeitamente. Uma refatoração simples resolveria esses pontos.

---

## Parte 3 — Visão de evolução

**3.1** Hoje o pipeline é disparado manualmente via shell script. Se você fosse propor a próxima evolução de infraestrutura — considerando que a empresa usa servidores Linux (VPS) e não tem cloud — o que você sugeriria e por quê? Que problema concreto isso resolve que o cron não resolve?

Eu sugeriria containerizar a aplicação com Docker. Isso faria com que a aplicação rodasse em qualquer máquina, pois garantiria que o ambiente local fosse idêntico à VPS. O problema do cron é que ele vai rodar no horário especificado e pronto. Sem logs (com exceção do que já adicionei no script), com Docker temos acesso a todos os logs em tempo de execução, podemos ver o erro em tempo real e podemos adicionar o cron no próprio Docker, então, ainda teríamos a execução programada.

---

**3.2** Imagine que, além dos arquivos atuais, o departamento passasse a receber um XML de retorno do convênio com o resultado do processamento de cada cobrança — aprovada, glosada parcialmente ou negada, com o motivo. Como você integraria essa nova fonte ao pipeline existente? O que mudaria no relatório final?

O fato de eu usar o Pandas para leitura e processamento faz com que o programa consiga ler diversos tipos de arquivos, incluindo arquivos XML. Bastaria eu ler esse arquivo na Etapa 1, normalizar os dados e fazer a junção da tabela em XML na Etapa 2 (Processamento), e o programa seguiria normalmente. No relatório final, eu adicionaria uma seção exibindo apenas o resultado do processamento e indicando o status por cores.

---

**3.3** O relatório Excel hoje é enviado por e-mail para um gestor. Se a empresa quisesse evoluir para um painel web simples onde o gestor pudesse consultar o histórico de relatórios e filtrar por mês, convênio ou tipo de alerta — como você estruturaria isso? Não precisa implementar, só descrever a abordagem técnica.

Precisaria adicionar uma etapa a mais na pipeline. Essa etapa seria responsável por importar as tabelas criadas para um banco de dados SQL e adicionaria uma coluna para a data de criação para os filtros. Consultar por convênio ou tipo de alerta bastaria executar um SELECT com WHERE especificando o campo e o valor. Todo esse processo seria feito criando uma API usando Node.js com Express ou até mesmo FastAPI para manter no mesmo ecossistema, e faria um fetch em GET /relatorios no painel com os filtros selecionados.

---

**3.4** Quais métricas ou condições você monitoraria se esse pipeline estivesse em produção? Dê exemplos concretos do que deveria disparar uma notificação imediata para a equipe — e do que não deveria.

Eu monitoraria se o arquivo ZIP dos dados está sendo lido corretamente, já que ele é a base da pipeline. Além disso, faria verificações para ver se os arquivos CSV foram gerados corretamente, já que eles são a base para a última etapa da pipeline. Qualquer falha nesses arquivos resulta no encerramento do programa. Para avisar que tem algo errado, eu dispararia um e-mail para a equipe em caso de erro. A maioria dos erros estão bem tratados e não interrompem o processamento de dados, logo não precisam ser notificados imediatamente.

---

## Parte 4 — Uso de agentes de IA

**4.1** Você usou algum agente de IA para te ajudar a resolver o desafio? Se sim, para quais partes do processo você o utilizou e como?

Usei o Gemini 3.1 Pro no Antigravity para ajudar na organização do projeto e autocomplete. Além disso, em alguns casos, usei para verificar se a etapa que eu estava fazendo estava de acordo com o que foi pedido no desafio.

---

## Parte 5 — Contexto pessoal

**5.1** Já trabalhou com automação de processos antes, mesmo que fora de um contexto profissional? Descreva brevemente o problema, o que você fez e qual foi o resultado.

Já trabalhei em um projeto que consistia em pegar um relatório em Excel de um Drive, editar alguns valores, estilizar e enviar para o WhatsApp. Fiz isso usando Selenium, Python e Pandas. A etapa mais complicada foi o envio para o WhatsApp, mas o resultado final foi satisfatório.

---

**5.2** O que você faria diferente se tivesse o dobro do tempo para resolver este desafio?

Eu consegui fazer o desafio em 2 dias e reservei 1 dia para refatorar o projeto. Com o dobro do tempo, eu me organizaria melhor para iniciar o projeto: levantaria os requisitos com calma e criaria um fluxograma no Excalidraw para ir seguindo etapa por etapa. A preparação demoraria mais, mas o desenvolvimento seria mais fluido; além disso, adicionaria testes unitários, que ajudariam a ter um código mais seguro na hora de mandar para a produção.

---

**5.3** Teve alguma parte do desafio que você achou mal especificada ou ambígua? O que estava faltando e como você lidou com a ambiguidade?

Apenas a última fase do desafio. A parte que diz para 'comentar o cron' pareceu, inicialmente, que era para deixar comentários no código todo explicando as etapas da execução do shell script, foi o que eu fiz inicialmente descrevendo cada etapa da execução do script. No entanto, depois lendo melhor, removi os comentários e deixei apenas o cron comentado, como deveria. De maneira geral, o desafio foi bem claro e objetivo.
