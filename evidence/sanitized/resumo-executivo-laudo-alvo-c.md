# Resumo executivo do laudo PSE — LlamaFactory (sanitizado — rodada C, alvo de IA)

**Laudo:** `laudo-pse-1.0` · modo `pse_inventory` · exit code **20** (veredito `indeterminado` — 2 checks não puderam ser decididos; bloqueia igual a violação, comportamento fail-closed)
**Alvo:** clone local de `hiyouga/LlamaFactory` @ `d6bb97ddff5d752d8b05aa099a168127c7253562` (`main`, congelado) — framework de fine-tuning de LLMs (Apache-2.0, 311 `.py`, ~63 mil linhas)
**Suite:** pse-suite 0.20.0 · `catalog_hash 4682a4ae…a0ac` · executado em 2026-08-31T22:31:17Z · duração 31,62 s (re-execução determinística verificada, ~30,8 s)

## Números

| Grandeza | Valor |
|---|---|
| Catálogo total | 58 checks |
| Executados | **25** (25/58 do catálogo) |
| — com achado | 6 checks distintos (21 findings) |
| — sem achado | 19 checks executados limpos |
| Pulados (com motivo computado) | **12** (2 por vetor estrutural ausente + 10 por artefato declarativo ausente) |
| Não habilitados (Trabalho A sem target) | **19** (15 como em A/B + 4 de ética/runtime que em A/B estavam cobertos pela guarda E-00) |
| Indeterminados | **2** (E-06, P-15 — estado próprio, nunca colapsado) |
| Previstos não implementados | 0 |
| Findings | **21** — 18 ALTO, 3 MÉDIO, 0 CRÍTICO |
| Packs fora de escopo | **nenhum** — a guarda E-00 manteve o pack de ética **em escopo por fato computado** (dependência de ML, rotinas de decisão e chamadas de treino/inferência no código) |

### Indicadores de cobertura (definição formal no relatório 07, §10.1; extensões declaradas em `scripts/14_analise_alvo_c.py`)

| Indicador | Valor | O que mostra |
|---|---|---|
| Cobertura bruta do catálogo | 25/58 | Parcela do catálogo executada no clone |
| Cobertura dos checks potencialmente aplicáveis ao perfil | 25/39 | Aderência da suite ao tipo de projeto (exclui os 19 do Trabalho A; a guarda E-00 não excluiu nenhum — pack de ética em escopo; os 2 indeterminados permanecem no denominador por terem tentado decidir) |
| Checks não aplicáveis ao corpus observado | 2 | Vetores estruturalmente ausentes (E-12 sem exportação de embedding/hash; P-19 sem barramento append-only) — classificação por forma de motivo, declarada a priori |
| Checks dependentes de contexto | 29 | 10 por artefato declarativo ausente (catálogo ×3, manifesto ×3, contrato, residência, finalidade, embasamento de catálogo do E-08) + 19 do Trabalho A |
| Indeterminados (estado próprio) | 2 | E-06 (fairness sem dataset declarado) e P-15 (treino sem catálogo de dados) — a suite recusou-se a decidir sem substrato |

**Partição verificada:** 25 + 2 + 29 + 2 = 58 — categorias mutuamente exclusivas (asserção em `scripts/14_analise_alvo_c.py`). **A partição do alvo C difere da de A/B (18+17+23=58, 0 indeterminados)** — deslocamento previsto na pré-triagem (`matrices/pre-triagem-alvo-c.md`): um perfil com IA move checks de "não aplicável" para "executado/indeterminado".

## Findings (sanitizados, com triagem humana preliminar)

| # | Check | Pilar | Severidade | Local | Assunto | Triagem humana |
|---|---|---|---|---|---|---|
| 1 | P-04 | privacy | ALTO | `tests/qa/catalog.yaml:1` | Não foi localizado, no clone analisado, o artefato declarativo de catálogo de dados esperado pelo perfil PSE | `ausencia-de-evidencia-pse` |
| 2 | P-07 | privacy | ALTO | `tests/qa/consent-model.yaml:1` | Não foi localizado um modelo de consentimento compatível com o perfil PSE; não permite concluir sobre base legal, governança ou tratamento fora do repositório | `ausencia-de-evidencia-pse` |
| 3 | E-07 | ethics | ALTO | `scripts/bench_qwen.py:20` | Código de ML sem Model Card versionado no repositório | `ausencia-de-evidencia-pse` (mesma forma de P-04/P-07: model cards de modelos treinados/avaliados por usuários residem na camada do operador/publicador, não no framework) |
| 4–6 | P-16 | privacy | ALTO ×3 | `train/mca/workflow.py:97`, `train/megatron_bridge/workflow.py:84` ×2 | Dataset de treino sem entrada de governança — nomes extraídos: `mca_config`, `w`, `utf-8` | `possivel-falso-positivo` ×3 (artefatos de parsing: config de checkpoint e argumentos de `open()` — modo e encoding — interpretados como nomes de dataset; dúvida preservada sobre o substrato real de datasets) |
| 7–9 | E-10 | ethics | MÉDIO ×3 | `train/{sft,rm,hyper_parallel}/workflow.py` | Decisão de `run_sft`/`run_rm` sem incerteza quantificada | `possivel-falso-positivo` (leitura preliminar: rotinas de treino/avaliação de modelo, não decisão automatizada sobre pessoas; dúvida preservada) |
| 10–15 | S-04 | security | ALTO ×6 | `.github/workflows/*` (publish, docker, tests, tests_npu ×3) | Host externo sem manifesto — alvos reais de egresso de **CI** (registry, índices de pacotes, mirror) | `confirmado-no-escopo` (integrações de CI reais; superfície de CI, não runtime) |
| 16–21 | S-04 | security | ALTO ×6 | `webui/locales.py` ×3, `model/patcher.py:406`, ISSUE_TEMPLATE, `scripts/api_example/` | Host externo sem manifesto — strings de UI sobre blog/docs/integração opcional, URL de exemplo em mensagem de erro, link de template de issue, imagem de exemplo | `possivel-falso-positivo` ×6 (documentação/autopresentação/exemplo/metadado) |

Distribuição por pilar: privacy 5 (P-04, P-07, P-16×3) · security 12 (S-04×12) · ethics 4 (E-07, E-10×3).
Distribuição por triagem: 3 `ausencia-de-evidencia-pse` · 6 `confirmado-no-escopo` · 12 `possivel-falso-positivo` (dúvida preservada em todos).

**Formulação responsável:** nenhum achado deve ser lido como "problema confirmado" do LlamaFactory. Os achados de ausência declarativa (P-04/P-07/E-07) não permitem concluir sobre controles organizacionais fora do repositório; os S-04 confirmados são fatos técnicos de egresso de CI sem manifesto — não violação; e os possíveis falsos positivos evidenciam oportunidades de calibração da suite no perfil de IA (extração de nomes de dataset e qualificação de "decisão" para rotinas de treino). Nenhum valor, host ou literal sensível é reproduzido neste material.

## Alcance

| Linguagem | Arquivos | Ferramenta |
|---|---|---|
| Python | 311 | `ast (stdlib)` |
| YAML | 113 | PyYAML |
| JSON | 20 | PyYAML |
| shell | 4 | linha a linha sobre código efetivo |
| JavaScript | 1 | tree-sitter |
| **fora de alcance** | **21** (`.jsonl` ×5, mídia ×8, `TOML` — inclui o `pyproject.toml` — e outros) | — |

A nota padrão vale na íntegra: ausência de achado não é atestado de conformidade; pulado, não habilitado, fora de alcance e indeterminado são estados distintos e permanecem distintos no laudo — nesta rodada, pela primeira vez no corpus, com um veredito global `indeterminado` (exit 20) que bloqueia por recusa honesta de decisão, não por erro.
