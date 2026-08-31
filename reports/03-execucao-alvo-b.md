# 03 — Execução e resultados (Fase 6)

**Execução:** modo `pse_inventory` (Trabalho B — sem rede, sem autorização), única forma permitida pelo protocolo desta rodada.
**Comando exato** (executado a partir de `/home/z/my-project/tpf-pse-fastetl`):

```bash
./.venv-pse/bin/pse --path repos/FastETL --modo pse_inventory \
    --output evidence/raw/laudo-alvo-b-bruto.json
```

> **Nota de revisão:** o laudo foi re-executado (mesmo comando, mesmo commit, mesma suite e `catalog_hash`) após padronização de nomenclatura dos anexos. A re-execução é determinística: findings, estados e cobertura idênticos aos da execução original; diferem apenas `timestamp_utc` e `duracao_s` (2,07 s → 2,0 s). Nomenclatura neutra "alvo-b" adotada conforme parecer da revisão; no texto, o projeto é sempre referido por seu nome, FastETL.

| Métrica de execução | Valor |
|---|---|
| Código de saída | **11** (violação com ALTO, sem CRÍTICO — não equivale a veredito jurídico ou de segurança) |
| Duração | **2,0 s** (`duracao_s` do laudo; 2,07 s na execução original) |
| Veredito da suite | `violacao` |
| Laudo bruto | `evidence/raw/laudo-alvo-b-bruto.json` — sha256 `7201c25c0bfd8afa6555cd5a983413d36806afad12ae336d4c541a0517f1a61d` |
| Laudo sanitizado | `evidence/sanitized/laudo-alvo-b-sanitizado.json` — sha256 `4942afe81f3aa31b4892d4ed4c456ed1aa4025753cef528913b70197a0df3b0f` |
| Procedência do laudo | suite pse-suite · 0.20.0 · schema `laudo-pse-1.0` · `catalog_hash 4682a4ae1115e577e95e2ddbd666bfd041efb2fca4b3d77e7683e2055571a0ac` · `repo_commit 9fb5d596cd8c3d4d0efcf6cdd1ca0c7b5e24afc1` · `config_fingerprint null` · timestamp 2026-08-31T21:22:26Z (re-execução determinística; original 20:25:22Z) · modo `pse_inventory` · autorização `null` |

> `config_fingerprint: null` é observável e coerente: nenhum `pse-config.yaml` foi criado no alvo (o clone não foi alterado — regra mandatória). Consequência observada: artefatos declarativos exigidos pela suite não existem, o que os checks cobram como achado de ausência (P-04/P-07) ou como pulo com motivo.

## 1. Distribuição de estados dos 58 checks do catálogo

| Estado | N | Fração do catálogo | Interpretação no escopo observado |
|---|---|---|---|
| Executados | 18 | 18/58 | rodaram e decidiram sobre o substrato lido |
| — com achado | 4 | | P-04, P-06, P-07, S-04 — 4 checks distintos, 8 findings no total |
| — sem achado | 14 | | P-01, P-03, P-09, P-13, P-14, P-17, P-20, S-06, S-09, S-10, S-11, S-13, S-14, S-15 (substrato lido, nada emitido) |
| Pulados (N/A declarativo) | 25 | 25/58 | motivo obrigatório emitido (ver §2) |
| Não habilitados | 15 | 15/58 | Trabalho A sem `target` declarado — previsto e não pedido |
| Indeterminados | 0 | 0/58 | nenhuma tentativa falhou em decidir |
| Previstos não implementados | 0 | 0/58 | catálogo inteiro implementado |
| **Total** | **58** | 58/58 | `cobertura.catalogo_total = 58` |

### 1.1 Indicadores de cobertura (refinamento do parecer)

A divisão simples `executados/total` não deve ser lida como "cobertura de 31%": ela mistura checks aplicáveis, não aplicáveis, dependentes de manifesto/catálogo, dependentes de execução dinâmica e checks que exigem um sistema de IA. Os indicadores abaixo separam esses conjuntos (denominadores distintos; as linhas 3 e 4 particionam os 58 checks, a linha 2 é uma razão com denominador próprio):

| Indicador | Valor | Como se calcula | O que mostra |
|---|---|---|---|
| Cobertura bruta do catálogo | **18/58** | executados ÷ catálogo total | Parcela total dos checks executados no clone |
| Cobertura dos checks potencialmente aplicáveis ao perfil | **18/29 (62%)** | executados ÷ (58 − 14 de ética/IA fora de escopo pela guarda E-00 − 15 dependentes do Trabalho A) | Aderência real da suite ao tipo de projeto (Python + Airflow, sem IA, sem alvo autorizado) |
| Checks não aplicáveis ao corpus observado | **17** | 14 de ética/IA (guarda E-00) + 3 com vetor estruturalmente ausente (P-15/P-16 treino, P-19 barramento) | Adequação do corpus ao perfil, não falha do alvo |
| Checks dependentes de contexto | **23** | 8 por artefato declarativo ausente (catálogo 3, manifesto 2, contrato 1, residência 1, finalidade 1) + 15 do Trabalho A | Limite da análise local estática: exigem manifesto, catálogo, alvo autorizado ou ambiente |

`cobertura.por_dominio` (checks por domínio no catálogo): frontend 11 · api 16 · backend 16 · data 15 · ai 15.

## 2. Motivos declarados dos pulados (amostra integral dos motivos próprios)

| Grupo | Checks | Motivo emitido pela suite |
|---|---|---|
| Ética fora de escopo (guarda E-00) | E-00…E-13 (14) | guarda E-00 emite o motivo do pack; E-01…E-13 herdam: "pack 'ethics' fora de escopo por E-00: nenhum indício de decisão automatizada sobre pessoas no código (sem dependência de ML, rotina de decisão ou chamada de inferência) e nada foi declarado em decision_making" |
| Catálogo de dados ausente | P-02, P-08, P-18 | "catálogo de dados ausente — cobrado por P-04" |
| Sem chamada de treino | P-15, P-16 | "nenhuma chamada de treino no código" |
| Sem barramento append-only | P-19 | "nenhuma produção de evento em barramento append-only no código" |
| Manifesto de terceiros ausente | S-05, S-08 | "manifesto de terceiros ausente — cobrado por S-04" |
| Sem contrato de API | S-12 | "nenhum arquivo se declara contrato de API (sem chave openapi/swagger de topo)" |
| Sem política de residência | S-16 | "nenhuma política de residência de dados declarada (data_residency)" |
| Sem finalidade no servidor | S-22 | "nenhum ponto do código lê X-Purpose nem chave equivalente" |

Cada motivo é específico e computado a partir do corpus — nenhum pulo é silencioso. Este é um resultado central da rodada: **a pré-triagem (Fase 5) foi confirmada na direção geral** (sem IA, sem API, sem declarações), com uma divergência interessante documentada no §5.

## 3. Achados (8) — visão sanitizada com formulação responsável

| # | Check | Severidade | Local | Assunto (sem literal) |
|---|---|---|---|---|
| 1 | P-04 | ALTO | `tests/qa/catalog.yaml:1` | Artefato declarativo de catálogo de dados esperado pelo perfil PSE **não foi localizado** no clone analisado |
| 2 | P-07 | ALTO | `tests/qa/consent-model.yaml:1` | Modelo de consentimento compatível com o perfil PSE **não foi localizado** no clone analisado |
| 3 | S-04 | ALTO | `fastetl/custom_functions/config.py:4` | Regra identificou host externo sem manifesto — inspeção manual deve determinar se é integração, documentação, exemplo ou metadado (caso apontado: URL de autopresentação em User-Agent) |
| 4 | S-04 | ALTO | `fastetl/custom_functions/sharepoint.py:56` | Regra identificou host de API de terceiro sem manifesto — inspeção manual deve classificar o uso |
| 5 | S-04 | ALTO | `fastetl/custom_functions/sharepoint.py:53` | Regra identificou host de autenticação de terceiro sem manifesto — inspeção manual deve classificar o uso |
| 6 | S-04 | ALTO | `fastetl/hooks/gsheet_hook.py:92` | Regra identificou escopo OAuth de API de terceiro sem manifesto — inspeção manual deve classificar o uso |
| 7 | P-06 | MÉDIO | `tests/conftest.py:43` | Regra identificou padrão de credencial em fixture de teste — classificação deve registrar se é exemplo sintético ou segredo real; valor não divulgado (`[REDACTED-SNIPPET-CREDENCIAL]`) |
| 8 | P-06 | MÉDIO | `tests/conftest.py:50` | idem — snippet `[REDACTED-SNIPPET-CREDENCIAL]` |

**Formulação responsável (parecer da revisão):** nenhum achado desta tabela deve ser lido como "problema confirmado" do FastETL. As formulações apropriadas são — P-04: *"não foi localizado, no clone analisado, o artefato declarativo de catálogo esperado pelo perfil PSE"*; P-07: *"não foi localizado um modelo de consentimento compatível com o perfil PSE; isso não permite concluir sobre base legal, governança ou tratamento de dados fora do repositório"*; S-04: *"a regra identificou hosts externos; a inspeção manual deve determinar se são integrações operacionais, documentação, exemplos ou metadados"*; P-06: *"a regra identificou um padrão em fixture; a classificação deve registrar se é exemplo sintético, teste ou segredo real — sem divulgar o valor"*. O resultado principal da rodada não é "o alvo falhou em privacidade", e sim: **checks declarativos exigem adaptação ao perfil de um projeto biblioteca/pipeline, pois certos artefatos de governança podem pertencer ao operador do pipeline, à organização usuária ou a outro nível da arquitetura**.

Distribuição por pilar: privacy 4 (P-04, P-07, P-06×2) · security 4 (S-04×4) · ethics 0 (pack fora de escopo).
Distribuição por severidade: ALTO 6 · MÉDIO 2 · CRÍTICO 0.

## 4. Cobertura por linguagem (bloco `alcance` do laudo)

| Linguagem | Arquivos | Ferramenta | Estado |
|---|---|---|---|
| Python | 43 | `ast (stdlib)` | lido |
| YAML | 5 | PyYAML | lido |
| SQL | 5 | regex sobre código efetivo | lido |
| shell | 1 | linha a linha | lido |
| `.zip`, `.xcf` | 2 | — | **fora de alcance** |

O laudo declara textualmente: "AUSENCIA DE ACHADO NAS LINGUAGENS ACIMA NAO E ATESTADO DE CONFORMIDADE… Este bloco existe porque um laudo silencioso sobre o que nao foi olhado e indistinguivel de um laudo que olhou e nao achou nada." Não houve `alcance_parcial` de linguagem (0 arquivos). Nota: os 4 arquivos sem extensão (Dockerfile, LICENSE etc.) não aparecem no bloco `lidos` nem em `fora_de_alcance` — a suite não declarou leitura deles; tratamos como não lidos/não declarados no escopo observado.

## 5. Observações de comportamento relevantes

1. **Cobertura parcial explícita:** P-07 e P-09 (catalogados como modo `active`) executaram a **metade estática** no inventário e a suite registrou em `relatorios.cobertura_parcial`: "metade runtime nao executada: Trabalho A nao habilitado…". O laudo, portanto, distingue "executado" de "totalmente executado" — o estado nunca é simples.
2. **Correlações estático×dinâmico:** o bloco `correlacoes` veio populado com P-06×S-20 ("credencial fora do cofre") e S-04×S-18 ("terceiro tratando dado do titular sem estar declarado"), ambos no cenário `so_na_camada_estatica`, com a leitura honesta: "defeito que a observação não exercitou" — nenhum finding foi removido por falta da dinâmica.
3. **Sanitização nativa funcionou:** os snippets de credencial chegaram parcialmente mascarados pela própria suite (`password='oz***'`); nesta rodada o protocolo elevou a redação para `[REDACTED]` integral no material sanitizado. Nenhum segredo, literal sensível ou dado pessoal consta dos anexos sanitizados.
4. **Sem config, a suite não fabrica:** `config_fingerprint: null`; packs declarados `[ethics, privacy, security]`; `packs_desabilitados` vazio; `packs_fora_de_escopo` com o motivo computado do ethics.
5. **Recusa versus laudo:** a execução não foi recusada (exit ≠ 30) mesmo sem config — a suite opera sobre o corpus e registra as ausências declarativas como achado (P-04/P-07), o que é uma decisão de desenho relevante para a pergunta de pesquisa: **sem artefato declarativo, a suite registra a ausência como achado em vez de calar.**

## 6. Tempo de execução e esforço

A execução completa do inventário levou **2,0 s** sobre 54 arquivos em escopo (54 lidos + 2 fora de alcance de 64 no clone, excluindo `.git`). O esforço de *preparação* (clone, venv, instalação, estudo de contratos) foi o componente dominante do custo total — estimado na ordem de horas de trabalho humano para adoção séria, contra segundos de máquina por rodada. Esta assimetria é favorável à adoção como etapa de CI contínuo.
