# Questionário — Desenvolvedor de Automação Júnior

Responda este questionário no arquivo `RESPOSTAS.md` na raiz do seu repositório.

Não existe resposta certa ou errada. O objetivo é entender como você pensa, quais trade-offs você reconhece e como você comunica decisões técnicas. Seja direto e objetivo — respostas longas demais não valem mais pontos.

---

## Parte 1 — Sobre o que você construiu

**1.1** Descreva em até 5 linhas o que o seu pipeline faz, como se estivesse explicando para alguém da equipe de faturamento que não é técnico.

---

**1.2** Qual foi a etapa mais difícil de implementar? O que tornou ela difícil e como você resolveu?

---

**1.3** A reconciliação entre o Excel e o CSV exigiu decisões sobre o que fazer quando os dados divergem. Descreva as principais decisões que você tomou:

- Quando o valor de uma cobrança difere entre as fontes, qual prevalece e por quê?
- O que você faz com uma cobrança que está só no CSV e não tem correspondente no Excel?
- Como você identificou que dois registros se referem ao mesmo paciente mesmo com grafias diferentes?

---

**1.4** Como você fez o vínculo entre os arquivos PDF e os registros de cobrança? Descreva a lógica de similaridade que usou, qual foi o maior risco dessa abordagem e como você o mitigou.

---

**1.5** Houve algum dado nos arquivos que te surpreendeu ou que você não esperava encontrar? Como você tratou?

---

## Parte 2 — Sobre as decisões técnicas

**2.1** Por que você escolheu a linguagem e as bibliotecas que usou? Quais alternativas considerou e por que descartou?

---

**2.2** Como você organizou o código? Explique brevemente a estrutura que criou e por que ela faz sentido para este problema.

---

**2.3** O pipeline lida com arquivos que podem chegar com problemas. Para cada cenário abaixo, descreva o que acontece no seu código:

- O Excel chega com uma coluna faltando
- Uma linha do CSV tem o campo `vl_liquido` vazio ou com texto no lugar do valor
- Dois PDFs na pasta `laudos/` têm nomes tão parecidos que o algoritmo de similaridade empata — ele não consegue decidir com certeza a qual cobrança cada um pertence
- O pipeline roda duas vezes seguidas sem que os arquivos de entrada tenham mudado

---

**2.4** Se o pipeline fosse rodar em produção todo mês com arquivos reais, o que você mudaria ou reforçaria em relação ao que entregou?

---

**2.5** Tem alguma parte do código que você sabe que não está boa, mas deixou assim por limitação de tempo? O que está errado e como você corrigiria?

---

## Parte 3 — Visão de evolução

**3.1** Hoje o pipeline é disparado manualmente via shell script. Se você fosse propor a próxima evolução de infraestrutura — considerando que a empresa usa servidores Linux (VPS) e não tem cloud — o que você sugeriria e por quê? Que problema concreto isso resolve que o cron não resolve?

---

**3.2** Imagine que, além dos arquivos atuais, o departamento passasse a receber um XML de retorno do convênio com o resultado do processamento de cada cobrança — aprovada, glosada parcialmente ou negada, com o motivo. Como você integraria essa nova fonte ao pipeline existente? O que mudaria no relatório final?

---

**3.3** O relatório Excel hoje é enviado por e-mail para um gestor. Se a empresa quisesse evoluir para um painel web simples onde o gestor pudesse consultar o histórico de relatórios e filtrar por mês, convênio ou tipo de alerta — como você estruturaria isso? Não precisa implementar, só descrever a abordagem técnica.

---

**3.4** Quais métricas ou condições você monitoraria se esse pipeline estivesse em produção? Dê exemplos concretos do que deveria disparar uma notificação imediata para a equipe — e do que não deveria.

---

## Parte 4 — Uso de agentes de IA
**4.1** Você usou algum agente de IA para te ajudar a resolver o desafio? Se sim, para quais partes do processo você o utilizou e como?

---

## Parte 5 — Contexto pessoal

**5.1** Já trabalhou com automação de processos antes, mesmo que fora de um contexto profissional? Descreva brevemente o problema, o que você fez e qual foi o resultado.

---

**5.2** O que você faria diferente se tivesse o dobro do tempo para resolver este desafio?

---

**5.3** Teve alguma parte do desafio que você achou mal especificada ou ambígua? O que estava faltando e como você lidou com a ambiguidade?