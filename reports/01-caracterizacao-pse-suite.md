# 01 — Caracterização da PSE Suite (e princípios do consumidor de referência)

**Estudo:** TPF — PSE Suite × FastETL (rodada 2, perfil engenharia de dados / Airflow)
**Natureza:** avaliação exploratória, estática e somente leitura
**Commit congelado da PSE Suite:** `443da92dbdb22a9af18aa6eebb51aac2da901458` (branch `main`, tag descritiva `v0.3.0-53-g443da92`)
**Versão instalada em venv isolado:** pse-suite **0.20.0** · schema `laudo-pse-1.0` · `catalog_hash 4682a4ae1115e577e95e2ddbd666bfd041efb2fca4b3d77e7683e2055571a0ac`

---

## 1. Propósito

A PSE Suite descreve-se como uma **suíte de evidências de Privacidade, Segurança e Ética por Design**: um padrão externo e versionado que um repositório consumidor declara como dependência (`pse-suite==0.20.0` em `requirements-qa.txt`), nunca copia. O princípio declarado no README é o contrato que estrutura toda a arquitetura:

> "O projeto declara configuração e autorização; o padrão fornece o motor e as verificações."

E o corolário que justifica a separação:

> "Uma trava que o vigiado pode desligar em silêncio não é uma trava."

O propósito não é emitir certificação nem parecer jurídico: é produzir **laudos técnicos com evidência sanitizada** (`arquivo:linha`, nunca o literal) que diferenciem, de forma não binária, o que foi verificado, o que não pôde ser decidido e o que está fora de alcance. Três decisões de desenho sustentam esse propósito: (i) a régua (`pse/data/`) vive no pacote versionado — se cada consumidor editasse sua cópia, remover uma linha faria o laudo dizer "nenhum achado" sem erro; (ii) o veredito tem cinco códigos de saída distintos, para que "não consegui auditar" nunca compartilhe código com "conforme"; (iii) a autoprova embutida (`--self-test`) exige que cada check comprove, com mutação canônica, que ainda morde.

## 2. Arquitetura resumida

A cadeia observada no commit congelado é:

```
pse/data/*.yaml (réguas curadas: pii-patterns, credenciais, legal-basis,
                 anonimizacao, prohibited-filters, rastreadores, ...)
        ↓
pse/data/checks-catalog.yaml  (catálogo declarativo: 58 checks com pack,
        ↓                      domínio, tipo, modo, severidade, mutação canônica)
pse/engine/ (runner, context, scan, jsast [tree-sitter], rustscan,
        ↓    registry, limites, autorizacao, sanitize, fingerprint)
pse/checks/** (implementação por check, prefixada por pilar)
        ↓
laudo JSON (schema laudo-pse-1.0, bloco artifact de procedência,
        ↓    evidência sanitizada pela própria régua antes de serializar)
CI do consumidor (gate por exit_code; política "ALTO bloqueia em main"
        ↓    vive no CI do consumidor, não na suite)
evidence bundle (adapter laudo-pse-1.0 → evidence-bundle/v1 draft,
             consumido pelo repositório de referência em regime de fixture)
```

A sanitização é parte do motor, não pós-processamento: o README afirma que "a evidência é sanitizada com a própria régua antes de ser serializada — o laudo não republica o CPF, o e-mail ou a chave que acabou de denunciar". O localizador de achado é `arquivo:linha`.

## 3. Separação padrão × consumidor

A fronteira observada é rigorosa e tem três camadas com donos de verdade distintos:

| Camada | Dona da verdade | Contém |
|---|---|---|
| **Padrão (pse-suite)** | julgamento técnico | motor, catálogo, réguas, gates fail-closed, sanitização, autoprova |
| **Consumidor** | autorização + configuração | alvo, thresholds (só apertar), escopo, versão pinada |
| **Harness** | orquestração | qual modo pode rodar, quem dispara, onde arquivar evidência |

Do lado da suite, o consumidor só pode **apertar** os thresholds dentro de faixas validadas (`k_anonymity_min` piso 5; `dpd_max_delta` teto 0,10 — declarar fora da faixa é **recusa de execução**, exit 30, e threshold desconhecido idem). Do lado do consumidor, a versão da régua tem fonte única (`version_source: requirements-qa.txt`) e o pin é a única ocorrência do número. Desabilitar todos os packs é entrada inválida: "laudo vazio não é laudo conforme".

## 4. Números exatos observados no commit congelado

| Grandeza | Valor observado | Fonte da observação |
|---|---|---|
| Checks implementados | **58** (22 P, 22 S, 14 E) | `pse --manifesto` executado no venv (58 IDs listados); `checks_previstos` vazio |
| Checks por modo (catálogo) | **35 inventory · 11 passive · 12 active** | parse de `pse/data/checks-catalog.yaml` |
| Autoprova | OK · **58 mutações canônicas do catálogo congelado (`catalog_hash 4682a4ae…a0ac`), 0 falhas**; E-06 indeterminado na fixture embutida (comportamento esperado: medição de disparidade exige dataset) | `pse --self-test`, exit 0 |
| Testes oficiais (`pytest -q`) | **809 passaram, 10 pulados** em 157,78 s — contagem da configuração local descrita na proveniência (Python 3.12.14), associada ao commit e ao ambiente congelados, não propriedade permanente do produto | log em `evidence/raw/pytest-pse-suite.txt` |
| Motivo dos pulos | 8 × Playwright ausente (camada dinâmica é opcional); 2 × alvo de aceite `btv` ausente (PENDENTE com motivo datado, nunca verde) | `pytest -rs` |
| Schema do laudo | `laudo-pse-1.0` | manifesto + `pse/schemas/` |
| Versão | 0.20.0, fonte única `pyproject.toml` | `pip show pse-suite` |

Observação de proveniência: o `MANIFESTO-v0.20.0.md` registra "798 passaram, 8 puladas"; neste ambiente (Python 3.12) a suíte congela em 809/10. A diferença é de ambiente/execução, não de catálogo — e é exatamente o tipo de divergência que o bloco `artifact` do laudo existe para tornar visível.

## 5. Pilares, domínios e modos de execução

**Pilares** (prefixo do ID, univalorado): `privacy` (P), `security` (S), `ethics` (E).
**Domínios** (lista, multivalorado): `frontend`, `api`, `backend`, `data`, `ai`. O prefixo codifica o pilar; o domínio vive em `domain` porque um check pode examinar mais de um estrato (ex.: S-07 é api+backend; P-18 é backend+data).

**Modos** (`--modo`, contrato de autorização em `docs/COMO-ADOTAR.md` §5):

| Modo | Checks | Rede | Autorização |
|---|---|---|---|
| `pse_inventory` (Trabalho B, padrão) | os 35 estáticos do catálogo | nenhuma | não; agente pode disparar |
| `pse_passive` (A) | 11 (S-03, E-01, E-02, e os dinâmicos P-22/P-23/P-24/S-17…S-21) | leitura com a própria identidade | atestação de escopo `pse_passive` |
| `pse_active` (A) | 12 sondas (S-01, S-02, S-07, P-05, P-07, P-09, P-10, P-11, E-03, E-09, S-05, S-22) | sonda de autorização | só `workflow_dispatch` com revisores + escopo `pse_active`; produção é recusada (exit 30) |

A ausência de autorização nunca é verde: Trabalho A não habilitado aparece em `checks_nao_habilitados` com motivo; habilitado com atestação inválida vira `checks_indeterminados` com **exit 20** — nunca uma requisição.

## 6. Por que esta rodada usará exclusivamente `pse_inventory`

A pergunta de pesquisa da rodada é o comportamento da suite **aplicada estaticamente** a um repositório público de engenharia de dados (FastETL). O protocolo mandatório do TPF proíbe rede, execução de DAGs, Airflow, Docker, serviços, credenciais e qualquer interação com ambientes externos. O modo `pse_inventory` é o único que satisfaz simultaneamente: (i) o contrato da própria suite — é o modo que "não toca rede" e que "o agente pode disparar"; (ii) o desenho ético do TPF — alvo é repositório de terceiros, sem autorização de sondagem; (iii) a reprodutibilidade — inventário estático é determinístico sobre um commit congelado. Os modos `pse_passive`/`pse_active` exigem um **alvo publicado e atestado**, que não existe e não será provisionado nesta rodada; os checks correspondentes entrarão no laudo como `checks_nao_habilitados`, estado legítimo e visível.

## 7. Estados possíveis do laudo e seu significado

A suite é explícita em **não colapsar estados** — quatro níveis de leitura nunca se misturam:

| Estado | Significado | Bloqueia CI? |
|---|---|---|
| **Achado (executado com violação)** | o check rodou, leu o substrato e encontrou o padrão que reprova | 10 (CRÍTICO) / 11 (ALTO) |
| **Sem achado sobre substrato auditado (`AUDITADO`)** | leu o substrato; "olhei e está limpo" | 0 |
| **Auditado parcial** | leu parte do substrato; "olhei metade", e a outra parte é nomeada | conforme severidade |
| **Pulado (`checks_pulados`)** | N/A declarativo: a pré-condição declarativa não existe (ex.: sem manifesto de terceiros não há o que conferir em S-08); motivo obrigatório | não |
| **Não habilitado (`checks_nao_habilitados`)** | previsto e não pedido: consumidor não pediu Trabalho A ou o modo não inclui o check | não |
| **Indeterminado (`checks_indeterminados`)** | tentou e não decidiu: fato não decidível estaticamente, arquivo ilegível, atestação inválida. **Bloqueia igual ao CRÍTICO** (exit 20) | sim |
| **Fora de alcance (bloco `alcance`)** | o vetor existe em linguagem sem parser — "sem achado" significa **não olhei**; é **estado**, não achado | não |
| **Não aplicável** | o vetor não existe neste alvo (medido por sonda do código efetivo quando possível) | não |
| **Previsto não implementado (`checks_previstos`)** | declarado no catálogo e ainda não implementado — hoje vazio | — |

Códigos de saída: `0` conforme · `10` violação com CRÍTICO · `11` violação com ALTO sem CRÍTICO · `20` indeterminado (bloqueia) · `30` entrada inválida (path/config/catálogo/versão irresolvíveis). Precedência: `30 > 10 > 20 > 11 > 0`. Não existe flag que rebaixe o gate.

## 8. Cobertura por linguagem — e o que isso significa para um alvo Python

O substrato declarado de cada check está no catálogo (`python`, `sql`, `declaracao`, `web`, `runtime`, `qualquer_backend`, `rust`…). Para esta rodada o alvo é **Python**: os checks estáticos com substrato `python`/`declaracao`/`qualquer_backend` são os candidatos naturais; `web`/`runtime` ficam fora de alcance sem a camada dinâmica e sem alvo no ar (que não será provisionado). A suite declara alcance a Rust por vetores textuais (S-06, P-18, P-19, S-16) e usa tree-sitter para JS/TS/JSX/TSX; **não há parser próprio de Python declarado na documentação como diferencial** — os checks Python operam por leitura de código (imports, chamadas, literais) e por declarações YAML/JSON. Limitação metodológica registrada: todo resultado desta rodada está **limitado à regra, ao arquivo e ao contexto observado** — ausência de achado não significa ausência de risco, e "não aplicável" é resultado de aplicabilidade do corpus, não mérito nem deficiência.

## 9. Limitações declaradas e "buracos assumidos"

A suite documenta honestamente o que não verifica (`docs/BURACOS-ASSUMIDOS.md` e seção equivalente de `docs/matriz-dominio.md`):

1. **P-21 — zona bruta de data lake sem restrição** (investigado, não implementado): a restrição vive em IAM/policy de bucket fora do repositório; a identificação viria do *nome* do bucket (menção, não fato — D-01); sem parser de HCL. "Buraco honesto é melhor que check que não verifica nada real."
2. **Endpoint de acesso do titular (Art. 18 II)**: "existe rota" já é P-10 (runtime); "responde com os dados certos, no prazo" não é verificável sem impersonar titular real — proibido pelo contrato.
3. **Efeito downstream de revogação (Art. 18 IX)**: comportamento distribuído (filas, réplicas, parceiros), não observável a partir do alvo.
4. **E-09 nunca aciona kill switch de verdade** (só dry-run constante); **E-06 nunca roda inferência** (exige medição existente, fresca e com condições).
5. Ética × frontend: célula vazia da matriz, "falta check" — dark patterns exigem julgamento que AST não dá.
6. Pendências abertas registradas em `docs/RATIFICACOES.md` (A-01 sobre PAN bloqueia P-12; A-02/D-07 bloqueiam refino de sigilo em E-11).

Para pipelines de dados, o buraco nº 1 é diretamente relevante: a superfície típica de restrição de data lake (IAM, policies, zones) está **fora do alcance estático declarado** — e o FastETL, como plugin de Airflow, vive justamente no domínio `data`/`backend` onde esses buracos foram assinados.

## 10. Procedência do laudo

Cada laudo carrega o bloco `artifact`:

```
suite · suite_version · schema_version · catalog_hash · repo_commit
· config_fingerprint · timestamp_utc
```

O `catalog_hash` cobre `pse/data/` **e** o código dos checks: dois laudos com a mesma `suite_version` mas hashes divergentes foram produzidos por réguas diferentes — visível sem depender da palavra de ninguém. `pse --manifesto` emite o mesmo conjunto no release, com o resultado da autoprova. A versão nunca é fabricada: ambiente com versão irresolvível é exit 30, não `0.8.0-dev`.

## 11. CI da própria suite (autoproteção da régua)

`.github/workflows/ci.yml`: instalação `pip install -e ".[dev]"`, trava de documentação gerada **antes** da suíte (`pytest tests/test_indice.py` — regenera `docs/TESTES.md`/`docs/INDICE-DE-TESTES.md` e compara byte a byte), e suíte completa sem `continue-on-error`, sem `|| true`, sem flag de desligar. `tests/test_ratificacao.py` sela as 15 ratificações e reprova ledger alterado sem teste; `tests/test_orfao.py` reprova check sem teste.

## 12. Subseção — princípios do consumidor de referência (`danzeroum/project`)

O repositório `project` (commit congelado `991e2d0f28d746e40a80c89280bdd9060f5a0311`) é a carcaça consumidora de referência. **Não foi executado nem ativado nesta rodada** (protocolo da Fase 3). Princípios observados que contribuem para o TPF:

1. **Evidência mínima e rastreabilidade.** O ledger (`harness/state/ledger.jsonl`) é allowlist estrutural: `additionalProperties: false`, sem nenhum campo textual livre — só hash, SHA, ID opaco, enum, timestamp, ID de CP e referência canônica. Minimização **estrutural**, não prometida.
2. **Versionamento e proveniência.** Fonte única de versão (`version_source`); a procedência evolui por versão de schema (`1.0` → `1.1` adiciona bloco `artifact`); fingerprint de escopo (`scope_fingerprint`) faz parecer de privacidade "envelhecer" auditavelmente.
3. **Pseudonimização de atores.** `actor_ref` no formato `^anon:[0-9a-f]{16}$`, com tabela de reidentificação fora do repositório. O ledger é mais estrito que `business.stakeholders` (que aceita handle) porque é append-only e versionado — "de onde não se apaga".
4. **Separação do que pode ser versionado.** `harness/runs/`, `harness/reports/`, `harness/state/` são gitignored (evidência bruta não entra no histórico); a única exceção versionada é o ledger, minimizado por construção.
5. **Release verificável antes de integração.** ADR-032 + `harness/policies/assurance-evidence.md`: produtor PSE em `merged_unreleased` (PR #2 mergeada em 17/08/2026 sem tag) tem evidência permitida **apenas em fixture/preparação**; `blocked` para CI estrito e produção; `release_eligible: false`; enum fechado de três estados — `released` sem tag/version/manifest/hash verificáveis é **inexpressível**, não proibido.
6. **Testes negativos e regras que "mordem".** `tests/governance/test_assurance_evidence_contract.py` contém ~20 testes de mordida que injetam estados proibidos e exigem reprovação (enum inválido, `released` sem hash, source commit divergente, `CTRL-DEP-001` satisfeito sem release, situação extra na matriz). "Assertion cujo alvo não existe vira `assertion_unresolvable`: uma trava que não encontra o que vigiar está quebrada, não satisfeita."
7. **Referência ≠ adoção.** O padrão PSE é **referência** no `project` (contrato, adapter, fixtures), não dependência ativa: não há `requirements-pse.txt` ativo nem suite registrada em `harness/suites/`. A diferença entre citar um produtor e adotá-lo é declarada, fiscalizada e testada.
8. **Parecer proporcional (não RIPD completo)** com papel LGPD `controller.role: none`, controles descartados com justificativa e gatilhos explícitos de reavaliação — modelo de documentação de limites que esta rodada TPF adota como boa prática.

## 13. Síntese para a rodada

A PSE Suite é um padrão de governança como código com separação régua/consumidor, veredito não binário, autoprova obrigatória, sanitização nativa e procedência verificável. Seu catálogo declara 58 checks, dos quais **35 são aplicáveis no modo estático** desta rodada. Para o perfil FastETL (Python + Airflow, sem frontend, sem API, sem IA), a expectativa metodológica é: vários checks `não aplicáveis` ou `pulados` por ausência de pré-condições declarativas (catálogo, manifesto de terceiros, modelo de consentimento), e foco de aplicabilidade em P-01 (PII em logs), P-06/S-06 (credenciais), S-04/S-05/S-08 (terceiros e egresso), E-13 (dependência), P-18/P-19/P-20 (persistência e hashing), E-08 (lineage) — sempre como hipótese a conferir, nunca como veredito sobre o alvo.
