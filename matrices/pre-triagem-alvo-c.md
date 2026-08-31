# Pré-triagem do alvo C (rodada de IA/ética) — matriz pré-registrada

> Registrada antes da enumeração final de candidatos e antes de qualquer execução da suite sobre o alvo C, conforme o critério pré-registrado no relatório 05 (§3) e os oito critérios mínimos estabelecidos pelo parecer da v3. A escolha **não é motivada por "parecer ter mais falhas"**: é motivada pela superfície de controles que os alvos A e B não ativaram (guarda E-00 fechada: 14 checks de ética fora de escopo; vetores estruturais de treino P-15/P-16 ausentes).

## 1. Critérios pré-registrados (parecer da v3)

| # | Critério | Requisito |
|---|---|---|
| 1 | Uso explícito de IA | README, código ou dependências devem evidenciar LLM, modelo, agente, classificação, decisão ou inferência |
| 2 | Linguagem compatível | Preferencialmente Python; TypeScript só após pré-triagem cuidadosa |
| 3 | Escopo administrável | Projeto pequeno ou médio; evitar monorepos gigantes |
| 4 | Código e documentação | README, testes, configuração e dependências suficientes para interpretar achados |
| 5 | Licença pública | Licença clara e permissiva ou adequada ao uso de pesquisa |
| 6 | Sem necessidade de execução | Deve permitir análise estática útil sem chamar API, modelo ou serviço externo |
| 7 | Aplicabilidade ética | Deve possuir pelo menos um fluxo observável de decisão, prompt, resposta, modelo, classificação, review ou audit log |
| 8 | Reprodutibilidade | Commit ou tag que possa ser congelado |

**Critério técnico adicional, derivado do instrumento congelado (registrado após leitura do código da suite, antes da execução):** a guarda E-00 (`pse/checks/ethics/e00_escopo.py`) computa indícios de decisão automatizada **somente em arquivos `.py`**, por três vias — (a) dependências de ML (`sklearn|torch|tensorflow|xgboost|lightgbm|keras|transformers|catboost|statsmodels`); (b) rotinas de decisão por nome de função (`score|predict|classific|triagem|decidir|decisao|recomend|negar_|aprovar_|bloquear_|avaliar_risco`); (c) chamadas de inferência (`predict|predict_proba|fit|transform|infer|score`) ou chamadas a modelos de linguagem (módulo que demonstra falar com LLM por hosts da categoria `llm` da régua — `api.openai.com`, `api.anthropic.com`, `generativelanguage.googleapis.com` — ou import de fornecedor, com verbo de invocação em objeto de LLM). Consequência de pré-triagem: um alvo sem nenhum `.py` com esses indícios **manteria a guarda E-00 fechada** e a rodada C não atingiria seu objetivo metodológico.

## 2. Censo de candidatos (enumeração ampla, sem execução da suite)

Fontes: organizações do ecossistema gov.br (mesma origem das rodadas A/B), repositórios amplamente adotados de aplicações/frameworks de IA, e busca estruturada na API do GitHub (topic `llm`, linguagem Python, licenças MIT/Apache-2.0, ativos).

| Candidato | Linguagem | Licença | Porte | Avaliação contra os critérios | Desfecho |
|---|---|---|---|---|---|
| `gestaogovbr/etica-ia-governanca` (AIE — Avaliação de Impacto Ético) | TypeScript + Java | MIT | 3 subprojetos | Crit. 1 parcial (a IA é objeto da avaliação humana, não há inferência no código); **crit. 2 frágil** (sem `.py` — a guarda E-00 não varre TS/Java → pacote de ética permaneceria fora de escopo e a rodada não atingiria o objetivo); crit. 3 frágil (front Next.js + 2 back-ends) | **Rejeitado** — instrui o registro: a preferência temática por repositório gov.br foi examinada e descartada por critério técnico do instrumento |
| `gestaogovbr/subnucleo-da-plataforma-de-ia`, `gestaogovbr/glossario-ia-setor-publico` | docs | — | ~MB | Sem código executável (documentação/glossário); crit. 4 falha | Rejeitados |
| `langchain-ai/langchain` | Python | MIT | ~593 MB | Monorepo gigante; crit. 3 falha | Rejeitado |
| `huggingface/transformers` | Python | Apache-2.0 | ~509 MB | Monorepo gigante; crit. 3 falha | Rejeitado |
| `vllm-project/vllm`, `unslothai/unsloth` | Python | Apache-2.0 | ~259–271 MB | Porte grande; crit. 3 frágil | Reserva |
| `crewAIInc/crewAI` | Python | MIT | ~291 MB | Porte grande; crit. 3 frágil | Reserva |
| `Mintplex-Labs/anything-llm` | JavaScript/TS | MIT | ~92 MB | Linguagem fora da preferência; crit. 2 | Rejeitado |
| `Skyvern-AI/skyvern` | Python+TS | AGPL-3.0 | ~625 MB | Licença copyleft forte + porte; crit. 3/5 frágeis | Rejeitado |
| `argilla-io/argilla` (HITL/anotação) | Python+TS | Apache-2.0 | ~809 MB | Porte; crit. 3 falha | Rejeitado |
| `openai/evals` | Python | **NOASSERTION** | ~7 MB | Licença não declarada; crit. 5 falha | Rejeitado |
| `vanna-ai/vanna` (text-to-SQL) | Python | MIT | ~9 MB | **Arquivado** (2026-02); adotável mas enfraquece discussão de adoção; reserva | Reserva |
| `AntonOsika/gpt-engineer` | Python | MIT | ~20 MB | **Arquivado** (precursor comercial); reserva | Reserva |
| `Azure-Samples/azure-search-openai-demo` | Python | MIT | ~85 MB | Passa em todos; RAG com documentação de IA responsável | Finalista |
| `lm-sys/FastChat` | Python | Apache-2.0 | ~35 MB | Passa; plataforma de serving + Arena (revisão humana) | Finalista |
| `assafelovic/gpt-researcher` | Python | Apache-2.0 | ~45 MB | Passa; agente de pesquisa com chamadas LLM | Finalista |
| `browser-use/browser-use` | Python | MIT | ~35 MB | Passa; agente de navegação | Reserva |
| `bytedance/deer-flow` | Python | MIT | ~60 MB | Passa; superagente de pesquisa | Reserva |
| `zylon-ai/private-gpt` | Python | Apache-2.0 | ~65 MB (888 `.py`) | Passa; camada de API para IA privada (RAG) | Finalista |
| `hiyouga/LlamaFactory` | Python | Apache-2.0 | ~14 MB (311 `.py`) | Passa; framework de fine-tuning de LLMs (ACL 2024) | **Finalista** |

## 3. Triagem fina dos finalistas (evidência computada contra o instrumento)

Inspeção estática dos clones rasos de pré-triagem (`/tmp/prescreen`, descartados após a decisão; o clone oficial do alvo C foi feito novo, com histórico completo, em `repos/`):

| Evidência (condição de abertura da guarda E-00 / vetores) | LlamaFactory | private-gpt | gpt-researcher |
|---|---|---|---|
| Dependência de ML (RX_ML: torch/transformers/…) | **Sim — `import torch` ×100+; `from transformers …` ×40+** | Não (usa llama-index) | Não |
| Rotinas de decisão por nome (RX_DECISAO) | **Sim — `get_scores`, `create_score_evaluation`, cabeças de reward/classification** | Parcial (`score_term`, `structured_predict`) | Não localizado na amostra |
| Chamadas de inferência (RX_INFERENCIA) | **Sim — `trainer.predict(...)` em múltiplos workflows; `trainer.train()`, `trainer.fit()`** | Sim — `self._llm.predict(...)` | Via abstração (langchain) |
| Chamada a LLM por hosts/import da régua | Parcial (2× `from openai import OpenAI` em avaliação) | **Sim — imports `openai`/`anthropic` + hosts da régua em código efetivo** | **Sim — `from langchain_openai import …` (token `openai` casa no padrão da suite)** |
| Chamadas de treino (vetor P-15/P-16) | **Sim — `trainer.train()`, `trainer.fit()`** | Não | Não |
| Linguagem | Python (311 `.py`, ~63 mil LOC) | Python (888 `.py`, ~156 mil LOC) | Python (331 `.py`, ~32 mil LOC) |
| Documentação/testes | README ~1.000 linhas; `tests/` + `tests_v1/` | README; `tests/` | README; `tests/` |
| Licença | Apache-2.0 | Apache-2.0 | Apache-2.0 |
| Atividade | pushed 2026-08-31; 74 mil estrelas | pushed 2026-08-31 | pushed 2026-08-27 |
| Fluxo observável p/ crit. 7 | treino, prompts de instrução/dados, predict/avaliação, scores | chat/RAG, prompts, respostas | prompts, planejamento, relatórios |

## 4. Decisão e justificativa (pré-registrada antes da execução)

**Alvo C selecionado: `hiyouga/LlamaFactory`**, congelado em `main` @ `d6bb97ddff5d752d8b05aa099a168127c7253562`.

Justificativa, em ordem de peso:

1. **É o único finalista que ativa os dois conjuntos de controles que A e B não exerceram**: (i) todo o pacote de ética (E-00 abre por dependência de ML computada — `torch`/`transformers` — além de rotinas `score` e chamadas `predict`), elevando E-01…E-13 de "fora de escopo" para execução efetiva; (ii) os vetores de treino P-15/P-16 ("nenhuma chamada de treino"), que passam de não aplicáveis a substrato real (`trainer.train()`/`trainer.fit()`). private-gpt e gpt-researcher abririam apenas (i).
2. Passa integralmente nos oito critérios do parecer, com o **menor porte entre os finalistas que maximizam a superfície avaliada** (311 `.py`, ~63 mil LOC; Apache-2.0; README extenso; duas suítes de testes; ativo e amplamente adotado — 74 mil estrelas, ACL 2024).
3. **Perfil arquitetural terceiro e distinto** (framework de treinamento/afinamento de LLMs) — complementa API (A) e biblioteca/pipeline (B) e testará a interpretação registrada no relatório 05 (§2.1): a partição do catálogo é propriedade da interação catálogo×perfil; um perfil com IA **deve** deslocar a partição (menos N/A por guarda E-00). Se não deslocar, a observação também será informativa.
4. A escolha não decorre de expectativa de "mais falhas": nenhum critério considerou findings, severidades ou notícias de incidentes; a evidência usada foi exclusivamente a superfície de controles observável estaticamente.

## 5. Efeitos esperados no método (hipóteses pré-registradas, a verificar no laudo)

- A guarda E-00 deve manter o pack de ética **em escopo por fato computado** ("em escopo, por fato computado" — nada declarado + indícios), alterando a partição: os 14 checks E-00…E-13 migram de *não aplicáveis* para *executados*.
- P-15/P-16 devem executar sobre chamadas de treino reais.
- O denominador da cobertura aplicável muda por construção (29 → mais checks potencialmente aplicáveis); as comparações com A/B devem usar a partição, nunca a fração 18/29 isolada (formulação do relatório 07, §10.1).
- Toda classificação humana continua nas três categorias pré-registradas, com dúvida preservada; nenhum valor, host ou literal sensível será reproduzido nos materiais sanitizados.
