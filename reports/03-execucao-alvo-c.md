# 03 — Execução e resultados do alvo C — LlamaFactory (rodada de IA/ética)

> **Emenda de protocolo nº 2 (declarada):** a rodada C acrescenta um **quinto clone público** (`hiyouga/LlamaFactory` @ `d6bb97d`) ao conjunto de clones do estudo, após pré-triagem pré-registrada (`matrices/pre-triagem-alvo-c.md`) e autorizada pelo parecer da v3 ("terceira rodada, previamente delimitada, em um repositório com uso explícito de IA"). Mesmas restrições das rodadas anteriores: estático, somente leitura, sem execução da aplicação/treino, sem banco, sem rede além dos clones, sanitização integral, `git status` verificado limpo ao final. Nenhum `pse-config.yaml` foi criado no alvo (clone intocado).

**Execução:** modo `pse_inventory` (Trabalho B — sem rede, sem autorização), a mesma forma permitida pelo protocolo desde a rodada B.
**Comando exato** (executado a partir de `/home/z/my-project/tpf-pse-fastetl`):

```bash
./.venv-pse/bin/pse --path repos/llamafactory --modo pse_inventory \
    --output evidence/raw/laudo-alvo-c-bruto.json
```

| Métrica de execução | Valor |
|---|---|
| Código de saída | **20** — veredito `indeterminado`: 2 checks não puderam ser decididos e o laudo **bloqueia** igual a violação (comportamento fail-closed; semântica da suite, não classificação jurídica) |
| Duração | **31,62 s** (campo `duracao_s` do laudo; re-execução determinística medida em ~30,8 s) |
| Laudo bruto | `evidence/raw/laudo-alvo-c-bruto.json` — sha256 `81999d73fc0c5c4dc78c971215e82b4da4754cddbd0760084b8c5987045d6259` |
| Laudo sanitizado | `evidence/sanitized/laudo-alvo-c-sanitizado.json` — sha256 `cf7eb33db4d3dee37d695e850544e37fbed39b6d263ee67433d57a063fd69a6c` |
| Procedência do laudo | suite pse-suite · 0.20.0 · schema `laudo-pse-1.0` · `catalog_hash 4682a4ae1115e577e95e2ddbd666bfd041efb2fca4b3d77e7683e2055571a0ac` · `repo_commit d6bb97ddff5d752d8b05aa099a168127c7253562` · `config_fingerprint null` · timestamp 2026-08-31T22:31:17Z · modo `pse_inventory` · autorização `null` |

**Equivalência determinística:** re-execução com o mesmo comando produziu laudo idêntico em todos os campos substantivos (divergências observadas apenas em `duracao_s` e `timestamp_utc`) — mesmo padrão documentado na rodada B. O pack de ética ficou **em escopo por fato computado** (`packs_fora_de_escopo` vazio), confirmando a hipótese pré-registrada na pré-triagem: nenhum check de ética foi excluído pela guarda E-00 neste alvo.

## 1. Distribuição de estados dos 58 checks do catálogo

| Estado | N | Fração do catálogo | Interpretação no escopo observado |
|---|---|---|---|
| Executados | **25** | 25/58 | rodaram e decidiram sobre o substrato lido |
| — com achado | 6 | | E-07, E-10, P-04, P-07, P-16, S-04 — 21 findings no total |
| — sem achado | 19 | | inclui E-00, E-04, E-05, E-11 (ética, substrato lido) e P-06 limpo |
| Pulados | **12** | 12/58 | 2 por vetor estrutural ausente (E-12, P-19) + 10 por artefato declarativo ausente |
| Não habilitados | **19** | 19/58 | Trabalho A sem `target` — inclui 4 checks de ética/runtime (E-01, E-02, E-03, E-09) que em A/B estavam cobertos pela guarda E-00 |
| Indeterminados | **2** | 2/58 | **E-06** (fairness sem dataset declarado) e **P-15** (treino sem catálogo de dados) — a suite recusou-se a decidir sem substrato e o veredito global virou `indeterminado` (exit 20) |
| Previstos não implementados | 0 | 0/58 | catálogo inteiro implementado |
| **Total** | **58** | 58/58 | `cobertura.catalogo_total = 58` |

### 1.1 Indicadores de cobertura (mesma metodologia das rodadas A/B, com extensões declaradas a priori)

Os indicadores seguem a definição formal do relatório 07, §10.1. Duas **extensões declaradas** foram necessárias neste perfil e estão codificadas em `scripts/14_analise_alvo_c.py`: (a) o laudo tem indeterminados ≠ 0, logo a partição é **quadriforme** (o estado indeterminado nunca é colapsado em outra categoria); (b) o motivo do pulo E-12 ("nenhuma exportação de embedding/hash derivado no código") tem a mesma forma dos vetores estruturais do §10.1 e foi classificado como não aplicável, a priori.

| Indicador | Valor | Como se calcula | O que mostra |
|---|---|---|---|
| Cobertura bruta do catálogo | **25/58** | executados ÷ catálogo total | Crescimento estrutural frente a A/B (18/58): checks de ética e de treino migraram de não aplicáveis para execução |
| Cobertura dos checks potencialmente aplicáveis ao perfil | **25/39** | executados ÷ (58 − guarda E-00 (0) − 19 do Trabalho A) | A guarda E-00 não excluiu nenhum check neste perfil; os 2 indeterminados permanecem no denominador por terem tentado decidir |
| Checks não aplicáveis ao corpus observado | **2** | E-12 + P-19 (vetores estruturalmente ausentes, classificação por forma de motivo) | Redução de 17 (em A/B) para 2 — o perfil com IA praticamente extingue a classe |
| Checks dependentes de contexto | **29** | 10 por artefato declarativo ausente + 19 do Trabalho A | Mesmo padrão declarativo das rodadas anteriores |
| Indeterminados (estado próprio) | **2** | E-06, P-15 | Primeira ocorrência do estado no corpus; a suite prefere bloquear (exit 20) a decidir sem substrato |

**Partição verificada:** **25 + 2 + 29 + 2 = 58** — categorias mutuamente exclusivas (asserção do script de análise). **A partição do alvo C difere da de A/B** (18 + 17 + 23 = 58, 0 indeterminados): o deslocamento foi previsto na pré-triagem e confirma a interpretação registrada no relatório 05, §2.1 — a partição é propriedade da interação catálogo×perfil. A razão 25/39 tem denominador próprio e não é aditiva com a partição (formulação segura do relatório 07, §10.1).

`cobertura.por_dominio` (propriedade do catálogo congelado, não do alvo): frontend 11 · api 16 · backend 16 · data 15 · ai 15.

## 2. Motivos declarados dos pulados (íntegros por grupo)

| Grupo | Checks | Motivo emitido pela suite |
|---|---|---|
| Vetor estrutural ausente (não aplicável) | E-12, P-19 | "nenhuma exportação de embedding/hash derivado no código" / "nenhuma produção de evento em barramento append-only no código" |
| Catálogo de dados ausente (dependente de contexto) | P-02, P-08, P-18, E-08 | "catálogo de dados ausente — cobrado por P-04" (E-08: "o catálogo não declara campo personal/sensitive"; P-18 acrescenta a consequência para confronto de campos) |
| Manifesto de terceiros ausente (dependente de contexto) | S-05, S-08, E-13 | "manifesto de terceiros ausente — cobrado por S-04" (E-13 acrescenta: "sem ele todo host de dependência seria achado, e ruído não é evidência") |
| Sem contrato de API | S-12 | "nenhum arquivo se declara contrato de API (sem chave `openapi` nem `swagger` de topo)" |
| Sem política de residência | S-16 | "nenhuma política de residência de dados declarada (`data_residency` na config ou no manifesto)" |
| Sem finalidade no servidor | S-22 | "nenhum ponto do código lê `X-Purpose` nem chave equivalente da requisição" |

Cada motivo é específico e computado a partir do corpus — nenhum pulo é silencioso. O motivo do E-13 merece registro: o check reconhece que, sem o manifesto declarativo, emitir achados para todo host de dependência produziria **ruído, não evidência** — calibração explícita de precisão embutida na própria regra.

## 3. Achados (21) — visão sanitizada com formulação responsável e triagem humana

| # | Check | Severidade | Local | Assunto (sem literal) | Classificação humana |
|---|---|---|---|---|---|
| 1 | P-04 | ALTO | `tests/qa/catalog.yaml:1` | Artefato declarativo de catálogo de dados esperado pelo perfil PSE **não foi localizado** no clone analisado | `ausencia-de-evidencia-pse` |
| 2 | P-07 | ALTO | `tests/qa/consent-model.yaml:1` | Modelo de consentimento compatível com o perfil PSE **não foi localizado** no clone; não permite concluir sobre base legal, governança ou tratamento fora do repositório | `ausencia-de-evidencia-pse` |
| 3 | E-07 | ALTO | `scripts/bench_qwen.py:20` | Código de ML sem **Model Card** versionado no repositório | `ausencia-de-evidencia-pse` (mesma forma de P-04/P-07: model cards de modelos treinados/avaliados pelos usuários do framework residem na camada do operador/publicador — a ausência no clone não conclui sobre o ecossistema) |
| 4 | P-16 | ALTO | `src/llamafactory/train/mca/workflow.py:97` | Dataset de treino sem entrada de governança — nome extraído `mca_config` | `possivel-falso-positivo` (leitura preliminar: arquivo de configuração de checkpoint — `mca_config.json` — interpretado como dataset de treino) |
| 5–6 | P-16 | ALTO ×2 | `src/llamafactory/train/megatron_bridge/workflow.py:84` | Dataset de treino sem entrada de governança — nomes extraídos `w` e `utf-8` | `possivel-falso-positivo` ×2 (leitura preliminar: argumentos da chamada `open()` — modo de abertura e encoding — interpretados como nomes de dataset; artefato de parsing) |
| 7–9 | E-10 | MÉDIO ×3 | `train/sft/workflow.py:41`, `train/rm/workflow.py:35`, `train/hyper_parallel/workflow.py:129` | Decisão de `run_sft`/`run_rm` **sem incerteza quantificada** | `possivel-falso-positivo` (leitura preliminar: rotinas de treino/avaliação de modelo, não decisão automatizada sobre pessoas; a dúvida permanece visível) |
| 10–15 | S-04 | ALTO ×6 | `.github/workflows/publish.yml:17`, `docker.yml:41`, `tests.yml:70`, `tests_npu.yml:45,57,79` | Regra identificou hosts externos sem manifesto — alvos reais de egresso de **CI** (índice de publicação de pacotes, registry de imagens, índices de dependências, mirror de modelos, cache interno de cluster) | `confirmado-no-escopo` (integrações de CI reais — fato técnico, não violação; superfície de CI, não runtime) |
| 16–18 | S-04 | ALTO ×3 | `src/llamafactory/webui/locales.py:37,38,2074` | Regra identificou hosts externos sem manifesto — strings de UI referenciando documentação do próprio projeto, blog oficial e serviço opcional de experiment tracking | `possivel-falso-positivo` ×3 (documentação/autopresentação/metadado de integração em texto de UI) |
| 19 | S-04 | ALTO | `src/llamafactory/model/patcher.py:406` | Regra identificou host externo sem manifesto — URL de **exemplo** em mensagem de orientação ao usuário | `possivel-falso-positivo` (mensagem de ajuda; a integração real de download existe em outras superfícies do código, registrada como indício, não como achado neste par arquivo:linha) |
| 20 | S-04 | ALTO | `.github/ISSUE_TEMPLATE/1-bug-report.yml:8` | Regra identificou host externo sem manifesto — link de template de issue | `possivel-falso-positivo` (metadado) |
| 21 | S-04 | ALTO | `scripts/api_example/test_image.py:37` | Regra identificou host externo sem manifesto — URL de imagem de exemplo em script de exemplo de API | `possivel-falso-positivo` (exemplo) |

**Formulação responsável (mesmo padrão das rodadas A/B):** nenhum achado desta tabela deve ser lido como "problema confirmado" do LlamaFactory. P-04/P-07/E-07: *"não foi localizado, no clone analisado, o artefato esperado pelo perfil PSE — isso não permite concluir sobre controles fora do repositório"*. S-04 confirmados: *"a regra identificou hosts externos reais de egresso de CI sem manifesto declarativo — fato técnico de inventário, não violação"*. Possíveis falsos positivos: a inspeção preliminar indica superfícies de documentação/exemplo/metadado ou artefatos de parsing — e é justamente essa a evidência de calibração que o corpus buscava para o perfil de IA. Nenhum valor, host ou literal sensível é reproduzido neste material.

Distribuição por pilar: privacy 5 (P-04, P-07, P-16×3) · security 12 (S-04×12) · ethics 4 (E-07, E-10×3).
Distribuição por severidade: ALTO 18 · MÉDIO 3 · CRÍTICO 0.
Distribuição por triagem: 3 `ausencia-de-evidencia-pse` · 6 `confirmado-no-escopo` · 12 `possivel-falso-positivo`.

## 4. Cobertura por linguagem (bloco `alcance` do laudo)

| Linguagem | Arquivos | Ferramenta | Estado |
|---|---|---|---|
| Python | 311 | `ast (stdlib)` | lido |
| YAML | 113 | PyYAML | lido |
| JSON | 20 | PyYAML | lido |
| shell | 4 | linha a linha sobre código efetivo | lido |
| JavaScript | 1 | tree-sitter | lido |
| fora de alcance | 21 | — | 14 tipos (`.jsonl` ×5 — inclui datasets demonstrativos; mídia ×8; `TOML` — **inclui o `pyproject.toml`**; `.cff`; outros) |

Nota factual relevante para evolução da suite: o `pyproject.toml` — fonte única de metadados do projeto — ficou **fora de alcance** por ser TOML (a suite lê YAML/JSON/Python/shell/JS). Nos alvos A/B não havia TOML, então este limite é observável apenas neste perfil.

## 5. Observações de comportamento relevantes (inéditas neste perfil)

1. **Primeiro veredito `indeterminado` do corpus (exit 20).** E-06 (fairness) e P-15 (treino × catálogo) encontraram metade do indício (treino/fairness em código) sem a outra metade do substrato (dataset declarado/catálogo). A suite **recusou-se a decidir** e o laudo bloqueou — coerente com o princípio anti-colapso de estados e com o comportamento fail-closed observado apenas artificialmente na mutação M6 da rodada B.
2. **Guarda E-00 aberta por fato computado, sem declaração.** `packs_fora_de_escopo` vazio; E-00, E-04, E-05, E-07, E-10, E-11 executaram sobre substrato real; E-06 ficou indeterminado; E-08/E-12/E-13 pularam com motivo próprio; E-01/E-02/E-03/E-09 (superfícies de runtime: explicação ao titular, decision log, contestação, kill switch) migraram da "guarda" para "não habilitado — Trabalho A". Nenhum estado foi colapsado.
3. **Cobertura parcial explícita, como em A/B:** P-07 e P-09 registraram "metade runtime não executada: Trabalho A não habilitado". Executado ≠ totalmente executado.
4. **Calibração exposta pelo perfil:** os 12 possíveis falsos positivos preliminares (6 S-04 de documentação/exemplo/UI, 3 P-16 de parsing de `open()`/config, 3 E-10 de rotinas de treino) são insumo direto para os perfis de aplicação da suite — em especial a qualificação de "decisão" para contextos de treino e a extração de nomes de dataset.
5. **Custo por porte:** 31,62 s sobre 449 arquivos lidos (311 Python + 113 YAML + 20 JSON + 4 shell + 1 JS) com 21 fora de alcance — a execução continua em segundos, mas o gradiente de custo aparece pela primeira vez no corpus (A: 2,4 s/38 arquivos; B: 2,0 s/57 arquivos), reforçando a viabilidade de CI com margem de crescimento.
6. **Sem config, a suite não fabrica:** `config_fingerprint: null`; packs declarados `[ethics, privacy, security]`; `packs_desabilitados` vazio; recusa versus laudo: a execução não foi recusada (exit ≠ 30) e as ausências declarativas continuaram registradas como achado (P-04/P-07) — terceiro perfil arquitetural consecutivo com esse comportamento.
