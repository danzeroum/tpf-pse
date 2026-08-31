# Matriz central — requisito → check → evidência → limite (PSE Suite × FastETL)

**Base:** laudo sanitizado `evidence/sanitized/laudo-alvo-b-sanitizado.json` (exit 11) + validação manual (relatório 04) + mutações (matriz da Fase 8). Estados do laudo são do commit congelado; classificações humanas seguem o vocabulário obrigatório da rodada.

**Convenção de classificação humana:** CES = confirmado-no-escopo · AEP = ausencia-de-evidencia-pse · PFP = possivel-falso-positivo · RCE = requer-contexto-externo · NAP = nao-aplicavel · IND = indeterminado · FDA = fora-de-alcance.

## 1. Privacy (22 checks no catálogo)

| Check | Requisito técnico | Artefato FastETL observado | Estado no laudo | Evidência sanitizada | Classif. humana | Limite / ameaça à validade | Recomendação |
|---|---|---|---|---|---|---|---|
| P-01 | PII não vai crua a logs | logging denso em `custom_functions/`, `operators/`, `hooks/` (Python lido por AST) | executado | sem achado | — | Sem achado vale só para os 43 `.py` lidos; conteúdo real em runtime não é observável | Manter no piloto; monitorar novas chamadas de log |
| P-02 | Retenção declarada com job de purga | sem catálogo declarativo | pulado — "catálogo ausente — cobrado por P-04" | — | AEP | Sem declaração não há o que confrontar; controle pode existir fora do repo | Operadores do plugin devem adotar o catálogo (hipótese de piloto) |
| P-03 | Soft-delete com eliminação definitiva | SQL só em fixture (`tests/sql/`) | executado | sem achado | — | Substrato SQL de teste; não prova comportamento de banco real | — |
| P-04 | Catálogo vivo de dados | `tests/qa/catalog.yaml` inexistente | **achado ALTO** | `tests/qa/catalog.yaml:1` | **AEP** | Ausência de artefato PSE ≠ ausência de controle organizacional; plugin não é operador de dados | Adotar catálogo por instância operadora; revisar se check deveria ter modo "biblioteca sem catálogo" |
| P-05 | Minimização por jornada (DTO) | sem borda HTTP | não habilitado (Trabalho A) | — | NAP | Vetor runtime; exigiria alvo atestad | Fora do perfil estático |
| P-06 | Chave de pseudonimização segregada | fixtures de teste com conexões sintéticas | **2 achados MÉDIO** | `tests/conftest.py:43` e `:50`, snippet `[REDACTED]` | **PFP** (com ressalva) | Suite rebaixou por caminho de teste (ratif. 11) e mantém a dúvida visível; validação humana não pôde aprofundar | Piloto: inventariar literais de fixture; housekeeping de fixtures |
| P-07 | Consentimento granular declarado | `tests/qa/consent-model.yaml` inexistente | **achado ALTO** (metade estática; cobertura parcial declarada) | `tests/qa/consent-model.yaml:1` | **AEP** | Metade runtime não executada (sem target); mesmo limite do P-04 | Idem P-04 |
| P-08 | Dado sensível sem base "legítimo interesse" | sem catálogo | pulado — catálogo ausente | — | AEP | Depende inteiramente de declaração | Idem P-04 |
| P-09 | k-anonimato em agregações | sem agregação de BI no corpus | executado (metade estática) | sem achado | — | Cobertura parcial declarada no laudo | — |
| P-10 | Portabilidade (endpoint) | sem borda HTTP | não habilitado | — | NAP | Vetor runtime | — |
| P-11 | Oráculo de existência | sem borda HTTP | não habilitado | — | NAP | Vetor runtime | — |
| P-13 | Consentimento pré-marcado (front) | sem artefato web | executado | sem achado | — | A suite executou mesmo sem frontend; ausência de vetor = sem achado legítimo | Avaliar estado "não aplicável" explícito para frontend ausente |
| P-14 | PII no cliente/URL (front) | idem | executado | sem achado | — | idem | idem |
| P-15 | PII como feature de treino | sem chamada de treino | pulado — "nenhuma chamada de treino" | — | NAP | Guarda computada funcionou | — |
| P-16 | Dataset de treino sem governança | idem | pulado — idem | — | NAP | idem | — |
| P-17 | Filtro sensível em busca | sem endpoint de busca | executado | sem achado | — | Sem rota alguma, o vetor não existe | — |
| P-18 | Campo sensível sem cifra | sem catálogo | pulado — catálogo ausente | — | AEP | M4 mostrou: com catálogo, o check depende de `class: sensitive`; com `personal` não dispara (vetor correto, mas operador pode subdeclarar) | Evolução: sinalizar no laudo quando catálogo existir e nenhuma classe sensitive for declarada (possível subdeclaração) |
| P-19 | Evento append-only com crypto-shredding | sem barramento de eventos | pulado — "nenhuma produção de evento" | — | NAP | Correto para o corpus; operadores com Kafka/topicos ficariam fora da leitura deste repo | — |
| P-20 | Hash determinístico ≠ anonimização | sem vetor no corpus | executado | sem achado | — | M5 provou que o check morde quando o vetor existe (ALTO na mutação) | Manter |
| P-22/23/24 | Camada dinâmica (navegador) | sem alvo no ar | não habilitado | — | NAP | Proibidos por protocolo nesta rodada | Somente em homologação autorizada (piloto futuro) |

## 2. Security (22 checks no catálogo)

| Check | Requisito técnico | Artefato FastETL observado | Estado no laudo | Evidência sanitizada | Classif. humana | Limite / ameaça à validade | Recomendação |
|---|---|---|---|---|---|---|---|
| S-01 | BOLA/IDOR | sem borda HTTP | não habilitado | — | NAP | Sonda ativa | — |
| S-02 | Rate limit + cursor | idem | não habilitado | — | NAP | idem | — |
| S-03 | PII em payload de erro | sem borda HTTP | não habilitado | — | NAP | idem | — |
| S-04 | Terceiro registrado com DPA | 4 hosts/integrações em código (MSAL/Graph, Google Drive, URL de autopresentação); sem manifesto | **4 achados ALTO** | `config.py:4` · `sharepoint.py:53` · `sharepoint.py:56` · `gsheet_hook.py:92` | 3 × **CES**; 1 × **PFP** (User-Agent) | Fato técnico (integração existe) ≠ violação; manifesto é do operador; M3 confirmou sensibilidade a hosts sintéticos | Evolução: distinguir URL de autopresentação (User-Agent) de egresso; no piloto, adotar manifesto |
| S-05 | Payload mínimo de egresso | sem manifesto (pré-condição) | pulado — "manifesto ausente — cobrado por S-04" | — | AEP | Sem o mapa destino→schema, nada a conferir | Adotar manifesto no piloto |
| S-06 | Sem API key global/hardcoded | credenciais de hook via Connection; fixture com literal sintético | executado | sem achado próprio (P-06 carregou os 2 MÉDIO) | — | M2 provou detecção CRÍTICO de `sk-` fora de teste | Manter |
| S-07 | X-Purpose + log de auditoria | sem leitura de finalidade | não habilitado (ativo) | — | RCE | Vetor runtime | — |
| S-08 | Transferência internacional com base declarada | sem manifesto | pulado — idem S-05 | — | AEP | Depende de declaração + contexto organizacional | Idem manifesto |
| S-09 | Token sensível no cliente | sem artefato cliente | executado | sem achado | — | — | — |
| S-10 | Injeção de prompt | sem LLM | executado | sem achado | — | Sem vetor; executou limpo | Poderia herdar a guarda E-00 |
| S-11 | Saída de modelo em sink | sem LLM | executado | sem achado | — | idem | idem |
| S-12 | Ontologia x-ethics no contrato | sem OpenAPI/swagger | pulado — "nenhum arquivo se declara contrato" | — | NAP | Correto | — |
| S-13 | Erro expõe internals | sem servidor HTTP | executado | sem achado | — | Vetor `api`; corpus não tem borda | idem S-10 |
| S-14 | Dump entre ambientes | sem declaração de dump | executado | sem achado | — | Check nasceu do estrato backend; sem declaração, nada a confrontar | — |
| S-15 | Privilégio excessivo de role | SQL só de fixture | executado | sem achado | — | `GRANT` amplo não observado; operadores reais teriam SQL/roles fora deste repo | — |
| S-16 | Residência na escrita | sem `data_residency` | pulado — "nenhuma política declarada" | — | RCE | Contexto organizacional; bucket `us-east-1` de operador não é visível | Idem manifesto |
| S-17…S-21 | Camada dinâmica | sem alvo no ar | não habilitado | — | NAP | Proibidos por protocolo | Piloto futuro em homologação |
| S-22 | Finalidade com base legal amarrada | sem leitura de X-Purpose | pulado — "nenhum ponto lê X-Purpose" | — | NAP | — | — |

## 3. Ethics (14 checks no catálogo)

| Check | Requisito técnico | Artefato FastETL observado | Estado no laudo | Evidência sanitizada | Classif. humana | Limite / ameaça à validade | Recomendação |
|---|---|---|---|---|---|---|---|
| E-00 | Guarda de escopo do pack | corpus sem IA, sem declaração | pulado (motivo próprio: guarda computou N/A) | motivo computado no laudo | NAP (resultado de aplicabilidade) | **A ausência de IA não é deficiência do FastETL nem da PSE**; M6 mostrou que declaração `automated` reabre o pack e E-06 vira indeterminado (exit 20) | Manter guarda; documentar efeito de declaração errada |
| E-01…E-13 (demais 13) | Explicação, decision log, contestação, HITL, proxy, disparidade, model card, lineage, kill switch, incerteza, PII em prompt, derivado anônimo, dependência exfiltradora | sem IA no corpus; sem `lineage.jsonl`; sem deps vendidas | pulados — motivo herdado do pack "ethics" fora de escopo por E-00 (a guarda E-00 emite o motivo próprio do pack) | — | NAP / AEP conforme o caso | E-08 e E-13 são os dois que *poderiam* ter vetor num projeto de dados; sem lineage e sem `node_modules/site-packages` vendidos, não houve o que ler | Piloto: fornecer `lineage.jsonl` tornaria E-08 executável — maior valor potencial para perfil Airflow |

## 4. Separação explícita exigida pelo TPF

| Grupo | Conteúdo |
|---|---|
| **O que a PSE verificou** | 54 arquivos em 4 linguagens (Python/YAML/SQL/shell) sobre 35 checks estáticos; 18 executaram e decidiram |
| **O que encontrou** | 8 findings: 2 ausências declarativas (P-04, P-07), 4 integrações de terceiro sem manifesto (S-04, sendo 1 provável falso positivo), 2 credenciais em fixture (P-06, rebaixadas) |
| **O que não conseguiu verificar** | Metade runtime de P-07/P-09; comportamento em execução de DAG; conteúdo de bancos; segredos de ambiente de operação; superfícies fora do repo (IAM, SCP, policies) |
| **O que não era aplicável** | Todo o estrato de IA (guarda E-00), borda HTTP (S-01/S-02/S-12/S-13/P-05/P-10/P-11/P-17), frontend estático (P-13/P-14/S-09), dinâmica (P-22…S-21) |
| **O que depende de contexto organizacional** | Manifesto de terceiros/DPA (S-04/S-05/S-08), residência (S-16), catálogo e base legal (P-02/P-04/P-08/P-18), lineage (E-08) — artefatos do operador, não da biblioteca |
| **O que sugere evolução da PSE** | (1) S-04 distinguir URL de autopresentação de egresso; (2) estado "biblioteca redistribuível" para checks declarativos (P-04/P-07/P-02) apontarão sempre ausência em plugins; (3) herdar a guarda E-00 para S-10/S-11/S-13; (4) sinalizar subdeclaração de catálogo (só `personal`, nenhum `sensitive`); (5) parser declarativo de Dockerfile/CI para checks de superfície de configuração; (6) E-08 com candidatos de lineage para pipelines Airflow (XCom/DAG-level provenance) |
