# Pré-triagem de aplicabilidade — PSE Suite (modo estático) × FastETL

**Quando:** produzida ANTES da execução completa (Fase 5), como hipótese de trabalho.
**Regra de ouro:** não se presume que todos os checks se apliquem. A ausência de IA não é deficiência do FastETL nem falha da PSE Suite — é um **resultado de aplicabilidade do corpus**. Hipóteses aqui serão confrontadas com o laudo da Fase 6 e revisadas na Fase 9.

## 1. Perguntas de aplicabilidade por pilar

### Privacidade
**Há logs, schemas, SQL, armazenamento, campos, catálogo, retenção, pseudonimização ou integração de dados que possam ser inspecionados?**
Sim, parcialmente: (i) logging extensivo em Python (`patchwork.py`, `fast_etl.py`, `copy_db_extensions.py`) — superfície para P-01; (ii) SQL mínimo, apenas em fixtures de teste (`tests/sql/`) — superfície fraca para P-03; (iii) integrações de dados (replicação Postgres/SQL Server/MySQL, GSheets, CKAN, dados.gov.br) — superfície de egresso para S-04/S-05/S-08; (iv) **não há catálogo de dados declarado** (`catalog.yaml` ausente), o que deve levar P-02/P-04/P-08/P-18 a estado `pulado` (pré-condição declarativa ausente), salvo comportamento distinto observado; (v) pseudonimização: nenhum indício de chave de pseudonimização no código — P-06 esperado sem achado ou sem vetor.

### Segurança
**Há credenciais, configuração, Docker, CI, egressos, endpoints ou integrações que possam ser inspecionados estaticamente?**
Sim: (i) padrões de leitura de `conn.password` em hooks (ckan, gsheet, dadosgovbr) — contexto legítimo de hook Airflow, mas é o vetor textual que S-06 opera; (ii) `Dockerfile` com `curl`/`apt-key` da Microsoft — leitura declarativa, cobertura depende de check específico; (iii) workflows GitHub Actions (3 arquivos) — inspeção declarativa; (iv) integrações externas com hosts nomeados (ckan, dados.gov.br, osrm, googleapis, microsoft) — vetor de S-04/E-13, **mas sem manifesto de terceiros no alvo o comportamento esperado é `pulado` com motivo**; (v) sem endpoints HTTP próprios — S-01/S-02/S-12/S-13 (domínio api) tendem a não aplicável; (vi) sem node_modules/site-packages vendidos no clone — E-13 depende do que o check varre de fato.

### Ética/IA
**Há IA, ML, pontuação, decisão automatizada, modelo ou LLM observável?**
**Não há** indício declarado de modelo, treino, LLM, score ou decisão automatizada no corpus observado. Conforme o desenho da própria suite, o E-00 é a guarda de escopo do pacote de ética: sem declaração `decision_making` (não há config no alvo), o comportamento esperado é o pack de ética ficar com motivo computado, e E-04/E-05/E-06/E-07/E-10/E-11/E-12/E-05 tendem a `não aplicável` ou `pulado`. **Marcado formalmente como não aplicável neste corpus**, sujeito à confirmação do laudo — uma declaração `none` divergente de fato viraria achado de E-00, mas aqui nem há declaração.

## 2. Matriz de hipóteses por check (35 do modo inventory)

| Check | Domínio(s) | Hipótese pré-execução | Justificativa resumida |
|---|---|---|---|
| P-01 | backend | **aplicável** | logging denso em Python; PII real não se afirma — só o vetor |
| P-02 | data | pulado (sem catálogo) | pré-condição: retenção declarada |
| P-03 | data | pulado ou sem achado | substrato SQL só em fixture de teste |
| P-04 | data | pulado (sem catálogo) | pré-condição: catálogo vivo |
| P-06 | backend | sem achado ou sem vetor | nenhum indício de chave de pseudonimização |
| P-08 | data | pulado (sem catálogo) | pré-condição: base legal no catálogo |
| P-13/P-14/S-09 | frontend | **não aplicável** | sem artefato web/cliente no corpus |
| P-15/P-16 | ai | **não aplicável** | sem treino/dataset de ML |
| P-17 | api | **não aplicável** | sem endpoint de busca |
| P-18 | backend,data | pulado (sem catálogo) | pré-condição: campo sensível declarado |
| P-19 | backend,data | sem achado ou sem vetor | sem padrão de tópico/evento append-only observado |
| P-20 | data | sem achado ou sem vetor | sem indício de hash de identificador tratado como anônimo |
| S-04 | backend | **aplicável com risco de pulado** | hosts de terceiro no código; manifesto ausente no alvo |
| S-06 | backend | **aplicável** | literais de credencial em código e testes (rebaixamento a MÉDIO em testes) |
| S-08 | data,backend | pulado (sem manifesto) | transferência internacional depende do manifesto |
| S-10/S-11 | ai | **não aplicável** | sem LLM/modelo |
| S-12 | api | **não aplicável** | sem contrato OpenAPI |
| S-13 | api | **não aplicável** | sem borda HTTP servida |
| S-14 | backend | pulado (sem declaração) | pré-condição: declaração de dump/ambiente |
| S-15 | backend,data | sem achado ou sem vetor | só SQL de fixture; sem role/GRANT observável |
| S-16 | backend | pulado (sem data_residency) | pré-condição: residência declarada |
| E-00 | ai | aplicável (guarda) | comportamento sem config a observar |
| E-04 | ai,backend | **não aplicável** | sem decisão automatizada |
| E-05 | ai | **não aplicável** | sem pipeline de features de modelo |
| E-06 | ai,data | pulado/indeterminado | tipo `ci`; exige dataset+report de disparidade |
| E-07 | ai | **não aplicável** | sem model card/datasheet aplicável |
| E-08 | data | pulado (sem lineage) | pré-condição: `lineage.jsonl` ou equivalente |
| E-10 | ai | **não aplicável** | sem decisão pontual automatizada |
| E-11 | ai,backend | **não aplicável** | sem prompt de LLM |
| E-12 | ai,data | sem achado ou sem vetor | sem exportação de embedding/hash observada |
| E-13 | backend | **aplicável (a confirmar)** | dependências Python declaradas; sem deps vendidas |

## 3. Hipóteses por artefato (compatibilidade)

| Artefato | Superfície para a PSE | Expectativa |
|---|---|---|
| `fastetl/custom_functions/` (5.400 linhas) | P-01, P-06, S-06, E-13 | principal zona de execução efetiva |
| `fastetl/hooks/` (853 linhas) | S-06 (contexto de credencial de Connection), S-04 | padrões legítimos de hook podem não disparar; a confirmar |
| `fastetl/operators/` (885 linhas) | P-01, E-04 | idem |
| `fastetl/example_dags/`, `tests/dags/` | vetores Python; risco de falso positivo em exemplo | classificação humana obrigatória |
| `tests/sql/`, `tests/docker-compose.yml` | P-03/S-15 (fraco) | fixtures — possível falso positivo |
| `requirements.txt`, `setup.py` | inventário, E-13 | sem análise de vulnerabilidade |
| `Dockerfile`, `.github/workflows/` | leitura declarativa | cobertura dependente de check específico |
| `docs/` (só imagens) | evidência de processo ausente | não comprova operação; não é achado contra o alvo |

## 4. Limites do método desta fase

Esta pré-triagem é hipótese qualificada, não veredito. Ela será confrontada com o laudo bruto (Fase 6); divergências (checks que executaram sem vetor esperado, ou que ficaram indeterminados) serão documentadas na Fase 9, nunca "corrigidas" silenciosamente.
