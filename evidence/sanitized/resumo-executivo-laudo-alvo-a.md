# Resumo executivo do laudo PSE — API PGD (sanitizado — rodada A, recuperação)

**Laudo:** `laudo-pse-1.0` · modo `pse_inventory` · exit code **11** (violação com ALTO, sem CRÍTICO)
**Alvo:** clone local de `gestaogovbr/api-pgd` @ `9d4b774cc6763b234372999a1d1c4baf248e3080` (tag `3.3.10`)
**Suite:** pse-suite 0.20.0 · `catalog_hash 4682a4ae…a0ac` · executado em 2026-08-31T21:48:06Z (recuperação da rodada A por re-execução local com a mesma instrumentação da rodada B — ver relatório 05, §1) · duração 2,4 s

## Números

| Grandeza | Valor |
|---|---|
| Catálogo total | 58 checks |
| Executados | **18** (18/58 do catálogo — ver indicadores abaixo) |
| Com achado | 3 checks distintos (4 findings) |
| Sem achado | 15 checks executados limpos |
| Pulados (N/A declarativo com motivo) | **25** (25/58) |
| Não habilitados (Trabalho A sem target) | **15** (15/58) |
| Indeterminados | **0** |
| Previstos não implementados | 0 |
| Findings | **4** — 4 ALTO, 0 MÉDIO, 0 CRÍTICO |

### Indicadores de cobertura (definição formal no relatório 07, §10.1)

| Indicador | Valor | O que mostra |
|---|---|---|
| Cobertura bruta do catálogo | 18/58 | Parcela do catálogo executada no clone |
| Cobertura dos checks potencialmente aplicáveis ao perfil | 18/29 (62%) | Aderência da suite ao tipo de projeto (exclui 14 de ética/IA fora de escopo e 15 do Trabalho A) |
| Checks não aplicáveis ao corpus observado | 17 | Adequação do corpus (14 ética/IA + 3 com vetor estruturalmente ausente), não falha do alvo |
| Checks dependentes de contexto | 23 | Limite da análise local estática (8 por artefato declarativo ausente + 15 do Trabalho A) |

**Partição verificada:** 18 + 17 + 23 = 58 — categorias mutuamente exclusivas (asserção em `scripts/11_analise_alvo_a.py`). Distribuição idêntica à da rodada B sob a mesma instrumentação.

## Findings (sanitizados)

| # | Check | Pilar | Severidade | Local (arquivo:linha) | Assunto |
|---|---|---|---|---|---|
| 1 | P-04 | privacy | ALTO | `tests/qa/catalog.yaml:1` | Não foi localizado, no clone analisado, o artefato declarativo de catálogo de dados esperado pelo perfil PSE |
| 2 | P-07 | privacy | ALTO | `tests/qa/consent-model.yaml:1` | Não foi localizado um modelo de consentimento compatível com o perfil PSE; não permite concluir sobre base legal, governança ou tratamento fora do repositório |
| 3 | S-04 | security | ALTO | `src/response_schemas.py:141` | Regra identificou host externo sem manifesto — host de documentação de biblioteca de terceiros referenciado em schema de resposta; inspeção manual deve classificar (`[REDACTED-HOST]`) |
| 4 | S-04 | security | ALTO | `docs/examples/get_token_example.py:4` | Regra identificou host externo sem manifesto — URL de hospedagem de código em arquivo de exemplo sob `docs/examples/`; inspeção manual deve classificar (`[REDACTED-HOST]`) |

## Estados e limites

- **Pacote de ética fora de escopo** por decisão da guarda E-00: "nenhum indício de decisão automatizada sobre pessoas no código… e nada foi declarado em decision_making" — os 14 checks do pack (E-00 a E-13) pulados com esse motivo. É **resultado de aplicabilidade do corpus**, não deficiência de nenhuma das partes.
- **Cobertura de linguagem:** Python 31 arquivos (AST stdlib), YAML 3, JSON 3, SQL 1; **0 arquivos fora de alcance** — a ausência de achado **não** é atestado de conformidade (declaração do próprio laudo).
- **Cobertura parcial declarada:** P-07 e P-09 executaram apenas a metade estática (metade runtime exige Trabalho A habilitado).
- **Correlação estático×dinâmico:** S-04×S-18 no cenário `so_na_camada_estatica` — "defeito que a observação não exercitou", sem dinâmica executada nesta recuperação.
- Nenhum segredo, literal sensível ou dado pessoal no presente material: hosts apontados por S-04 foram mascarados como `[REDACTED-HOST]` (regra de protocolo; a inspeção preliminar os lê como documentação/exemplo).

## Leitura responsável (triagem humana)

Cada achado é **achado que requer validação humana** — nenhum é problema confirmado da API PGD. Os ALTO de P-04/P-07 são `ausencia-de-evidencia-pse` (artefato declarativo não localizado no clone — não concluem ausência de controle organizacional). Os 2 S-04 são `possivel-falso-positivo` em leitura preliminar (host de documentação de biblioteca em schema de resposta; URL de hospedagem de código em arquivo de exemplo) — a inspeção manual deve determinar se são integrações operacionais, documentação, exemplos ou metadados, e a dúvida permanece registrada.

> Esta avaliação foi realizada sobre clone local de código público, em modo estático e somente leitura, limitada aos commits e artefatos observados. Não constitui auditoria, certificação, parecer jurídico ou comprovação de ausência de riscos.
