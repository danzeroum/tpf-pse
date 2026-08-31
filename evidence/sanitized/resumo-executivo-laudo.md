# Resumo executivo do laudo PSE — FastETL (sanitizado)

**Laudo:** `laudo-pse-1.0` · modo `pse_inventory` · exit code **11** (violação com ALTO, sem CRÍTICO)
**Alvo:** clone local de `gestaogovbr/FastETL` @ `9fb5d596cd8c3d4d0efcf6cdd1ca0c7b5e24afc1`
**Suite:** pse-suite 0.20.0 · `catalog_hash 4682a4ae…a0ac` · executado em 2026-08-31T21:22:26Z (re-execução determinística da rodada, após padronização de nomenclatura) · duração 2,0 s

## Números

| Grandeza | Valor |
|---|---|
| Catálogo total | 58 checks |
| Executados | **18** (18/58 do catálogo — ver indicadores abaixo) |
| Com achado | 4 checks distintos (8 findings) |
| Sem achado | 14 checks executados limpos |
| Pulados (N/A declarativo com motivo) | **25** (25/58) |
| Não habilitados (Trabalho A sem target) | **15** (15/58) |
| Indeterminados | **0** |
| Previstos não implementados | 0 |
| Findings | **8** — 6 ALTO, 2 MÉDIO, 0 CRÍTICO |

### Indicadores de cobertura (refinamento do parecer — detalhes no relatório 03)

| Indicador | Valor | O que mostra |
|---|---|---|
| Cobertura bruta do catálogo | 18/58 | Parcela do catálogo executada no clone |
| Cobertura dos checks potencialmente aplicáveis ao perfil | 18/29 (62%) | Aderência da suite ao tipo de projeto (exclui 14 de ética/IA fora de escopo e 15 do Trabalho A) |
| Checks não aplicáveis ao corpus observado | 17 | Adequação do corpus (14 ética/IA + 3 com vetor estruturalmente ausente), não falha do alvo |
| Checks dependentes de contexto | 23 | Limite da análise local estática (8 por artefato declarativo ausente + 15 do Trabalho A) |

## Findings (sanitizados)

| # | Check | Pilar | Severidade | Local (arquivo:linha) | Assunto |
|---|---|---|---|---|---|
| 1 | P-04 | privacy | ALTO | `tests/qa/catalog.yaml:1` | Não foi localizado, no clone analisado, o artefato declarativo de catálogo de dados esperado pelo perfil PSE |
| 2 | P-07 | privacy | ALTO | `tests/qa/consent-model.yaml:1` | Não foi localizado um modelo de consentimento compatível com o perfil PSE; não permite concluir sobre base legal, governança ou tratamento fora do repositório |
| 3 | S-04 | security | ALTO | `fastetl/custom_functions/config.py:4` | Regra identificou host externo sem manifesto; inspeção manual deve determinar se é integração operacional, documentação, exemplo ou metadado (URL do próprio projeto em User-Agent) |
| 4 | S-04 | security | ALTO | `fastetl/custom_functions/sharepoint.py:56` | Regra identificou host de API de terceiro (Graph) sem manifesto; inspeção manual deve classificar o uso |
| 5 | S-04 | security | ALTO | `fastetl/custom_functions/sharepoint.py:53` | Regra identificou host de autenticação de terceiro sem manifesto; inspeção manual deve classificar o uso |
| 6 | S-04 | security | ALTO | `fastetl/hooks/gsheet_hook.py:92` | Regra identificou escopo OAuth de API de planilhas de terceiro sem manifesto; inspeção manual deve classificar o uso |
| 7 | P-06 | privacy | MÉDIO | `tests/conftest.py:43` | Regra identificou padrão de credencial em fixture de teste; classificação deve registrar se é exemplo sintético ou segredo real — valor não divulgado (`[REDACTED]`) |
| 8 | P-06 | privacy | MÉDIO | `tests/conftest.py:50` | idem (`[REDACTED]`) |

## Estados e limites

- **Pacote de ética fora de escopo** por decisão da guarda E-00: "nenhum indício de decisão automatizada sobre pessoas no código… e nada foi declarado em decision_making" — os 14 checks do pack (E-00 a E-13) pulados com esse motivo (próprio da guarda e herdado pelos demais). É **resultado de aplicabilidade do corpus**, não deficiência de nenhuma das partes.
- **Cobertura de linguagem:** Python 43 arquivos (AST stdlib), YAML 5, SQL 5, shell 1; fora de alcance: 2 arquivos (`.zip`, `.xcf`) — a ausência de achado neles **não** é atestado de conformidade (declaração do próprio laudo).
- **Cobertura parcial declarada:** P-07 e P-09 executaram apenas a metade estática (metade runtime exige Trabalho A habilitado).
- **Correlações estático×dinâmico:** P-06×S-20 e S-04×S-18 no cenário `so_na_camada_estatica` — "defeito que a observação não exercitou", sem dinâmica executada nesta rodada.
- Nenhum segredo, literal sensível ou dado pessoal no presente material: credenciais apontadas pela suite foram substituídas por `[REDACTED-SNIPPET-CREDENCIAL]` (a própria PSE já entregava o valor mascarado na origem).

## Leitura responsável (antecipação da Fase 7)

Cada achado é **achado que requer validação humana** — nenhum é problema confirmado do FastETL. Os ALTO de P-04/P-07 são `ausencia-de-evidencia-pse` (artefato declarativo não localizado no clone — não concluem ausência de controle organizacional; em bibliotecas/pipelines esses artefatos podem pertencer ao operador). Os S-04 são majoritariamente `confirmado-no-escopo` (integração de terceiro existe em código, sem manifesto — fato técnico, não violação) com um caso de possível falso positivo (URL de autopresentação em User-Agent). Os P-06 estão em fixture de teste com sintética de ambiente Docker (a própria suite rebaixou para MÉDIO pela ratificação 11 — contexto de teste) e demandam classificação humana como `possivel-falso-positivo`.

> Esta avaliação foi realizada sobre clone local de código público, em modo estático e somente leitura, limitada aos commits e artefatos observados. Não constitui auditoria, certificação, parecer jurídico ou comprovação de ausência de riscos.
