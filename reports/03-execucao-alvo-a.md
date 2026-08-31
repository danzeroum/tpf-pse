# 03 — Execução e resultados do alvo A — API PGD (recuperação por re-execução local)

> **Contexto de recuperação:** os insumos originais da rodada 1 (API PGD) não estavam disponíveis neste ambiente (registro no relatório 05 da v2). Conforme a sequência recomendada pelo parecer da orientação, a rodada A foi recuperada por **re-execução local com a mesma instrumentação congelada da rodada B**: mesmo clone da suite (`pse-suite` @ `443da92`, v0.20.0), mesmo `catalog_hash`, mesmo venv (Python 3.12.14), mesmo SO, mesmas regras de sanitização e de classificação humana, mesmo formato de laudo. **Emenda de protocolo declarada:** um quarto clone público (`gestaogovbr/api-pgd` @ `9d4b774c`) foi acrescentado aos três originais, sob as mesmas restrições — estático, somente leitura, sem execução da aplicação, sem banco, sem rede além do clone, sanitização integral, `git status` verificado limpo ao final. Quando os insumos originais da rodada 1 forem localizados, esta execução deverá ser reconciliada com eles (ameaça à comparabilidade declarada no relatório 05, §5).

**Execução:** modo `pse_inventory` (Trabalho B — sem rede, sem autorização), a mesma forma permitida pelo protocolo da rodada B.
**Comando exato** (executado a partir de `/home/z/my-project/tpf-pse-fastetl`):

```bash
./.venv-pse/bin/pse --path repos/api-pgd --modo pse_inventory \
    --output evidence/raw/laudo-alvo-a-bruto.json
```

| Métrica de execução | Valor |
|---|---|
| Código de saída | **11** (violação com ALTO, sem CRÍTICO — semântica da suite, não veredito jurídico ou de segurança) |
| Duração | **2,4 s** (`duracao_s` do laudo) |
| Veredito da suite | `violacao` |
| Laudo bruto | `evidence/raw/laudo-alvo-a-bruto.json` — sha256 `9242263a6cf7bf1759edd0e5e1adf535c9cab9fed028646fb8dc47a9f64d1c3e` |
| Laudo sanitizado | `evidence/sanitized/laudo-alvo-a-sanitizado.json` — sha256 `dc7850c70fd918e18447602bbb04894dc88ee00437801b3819459acc8e71532d` |
| Procedência do laudo | suite pse-suite · 0.20.0 · schema `laudo-pse-1.0` · `catalog_hash 4682a4ae1115e577e95e2ddbd666bfd041efb2fca4b3d77e7683e2055571a0ac` · `repo_commit 9d4b774cc6763b234372999a1d1c4baf248e3080` · `config_fingerprint null` · timestamp 2026-08-31T21:48:06Z · modo `pse_inventory` · autorização `null` |

> `config_fingerprint: null` é observável e coerente, e espelha a rodada B: nenhum `pse-config.yaml` foi criado no alvo (o clone não foi alterado — regra mandatória). Consequência observada idêntica: artefatos declarativos exigidos pela suite não existem, e os checks os cobram como achado de ausência (P-04/P-07) ou como pulo com motivo.

## 1. Distribuição de estados dos 58 checks do catálogo

| Estado | N | Fração do catálogo | Interpretação no escopo observado |
|---|---|---|---|
| Executados | 18 | 18/58 | rodaram e decidiram sobre o substrato lido |
| — com achado | 3 | | P-04, P-07, S-04 — 3 checks distintos, 4 findings no total |
| — sem achado | 15 | | P-01, P-03, P-06, P-09, P-13, P-14, P-17, P-20, S-06, S-09, S-10, S-11, S-13, S-14, S-15 (substrato lido, nada emitido) |
| Pulados (N/A declarativo) | 25 | 25/58 | motivo obrigatório emitido (ver §2) |
| Não habilitados | 15 | 15/58 | Trabalho A sem `target` declarado — previsto e não pedido |
| Indeterminados | 0 | 0/58 | nenhuma tentativa falhou em decidir |
| Previstos não implementados | 0 | 0/58 | catálogo inteiro implementado |
| **Total** | **58** | 58/58 | `cobertura.catalogo_total = 58` |

### 1.1 Indicadores de cobertura (mesma metodologia da rodada B)

Os indicadores seguem a definição formal registrada no relatório 07, §10.1 — mesma regra de classificação com precedência declarada, codificada em `scripts/11_analise_alvo_a.py` e verificada por asserção de partição:

| Indicador | Valor | Como se calcula | O que mostra |
|---|---|---|---|
| Cobertura bruta do catálogo | **18/58** | executados ÷ catálogo total | Parcela total dos checks executados no clone |
| Cobertura dos checks potencialmente aplicáveis ao perfil | **18/29 (62%)** | executados ÷ (58 − 14 de ética/IA fora de escopo pela guarda E-00 − 15 dependentes do Trabalho A) | Aderência real da suite ao tipo de projeto (API Python, sem IA, sem alvo autorizado) |
| Checks não aplicáveis ao corpus observado | **17** | 14 de ética/IA (guarda E-00) + 3 com vetor estruturalmente ausente (P-15/P-16 treino, P-19 barramento) | Adequação do corpus ao perfil, não falha do alvo |
| Checks dependentes de contexto | **23** | 8 por artefato declarativo ausente (catálogo 3, manifesto 2, contrato 1, residência 1, finalidade 1) + 15 do Trabalho A | Limite da análise local estática |

**Partição verificada:** 18 + 17 + 23 = 58 — as três categorias são mutuamente exclusivas e exaustivas neste alvo (asserção do script de análise). A distribuição é **idêntica à da rodada B** sob a mesma instrumentação: mesmo denominador aplicável (29), mesma fração executada (18/29 = 62%), mesma partição. O que difere entre os alvos não é a estrutura de estados, e sim os findings (4 × 8) e a natureza das superfícies apontadas (§3).

`cobertura.por_dominio` (checks por domínio no catálogo): frontend 11 · api 16 · backend 16 · data 15 · ai 15 (idêntico à rodada B — é propriedade do catálogo congelado, não do alvo).

## 2. Motivos declarados dos pulados (amostra integral dos motivos próprios)

| Grupo | Checks | Motivo emitido pela suite |
|---|---|---|
| Ética fora de escopo (guarda E-00) | E-00…E-13 (14) | guarda E-00 emite o motivo do pack; E-01…E-13 herdam: "pack 'ethics' fora de escopo por E-00: nenhum indício de decisão automatizada sobre pessoas no código (sem dependência de ML, rotina de decisão ou chamada de inferência) e nada foi declarado em decision_making" |
| Catálogo de dados ausente | P-02, P-08, P-18 | "catálogo de dados ausente — cobrado por P-04" (P-18 acrescenta: "sem inventário não há campo sensível a confrontar") |
| Sem chamada de treino | P-15, P-16 | "nenhuma chamada de treino no código — não há feature a confrontar com o catálogo" / "…não há dataset de treino a inventariar" |
| Sem barramento append-only | P-19 | "nenhuma produção de evento em barramento append-only no código" |
| Manifesto de terceiros ausente | S-05, S-08 | "manifesto de terceiros ausente — cobrado por S-04" |
| Sem contrato de API | S-12 | "nenhum arquivo se declara contrato de API (sem chave `openapi` nem `swagger` de topo)" |
| Sem política de residência | S-16 | "nenhuma política de residência de dados declarada (`data_residency` na config ou no manifesto)" |
| Sem finalidade no servidor | S-22 | "nenhuma finalidade entra no servidor: nenhum ponto do código lê `X-Purpose` nem chave equivalente da requisição" |

Cada motivo é específico e computado a partir do corpus — nenhum pulo é silencioso, como na rodada B. Nota comparativa: S-12 pulou com "sem contrato de API" mesmo o alvo sendo uma API — a chave que a suite procura é a **declaração formal** (`openapi`/`swagger` de topo), e o contrato servido pelo FastAPI em runtime não é um artefato de arquivo no clone; é outro exemplo de controle que pertence à camada de operação/execução, não ao par arquivo-linha estático.

## 3. Achados (4) — visão sanitizada com formulação responsável e triagem humana

| # | Check | Severidade | Local | Assunto (sem literal) | Classificação humana |
|---|---|---|---|---|---|
| 1 | P-04 | ALTO | `tests/qa/catalog.yaml:1` | Artefato declarativo de catálogo de dados esperado pelo perfil PSE **não foi localizado** no clone analisado (o laudo aponta o local convencionado pelo perfil) | `ausencia-de-evidencia-pse` |
| 2 | P-07 | ALTO | `tests/qa/consent-model.yaml:1` | Modelo de consentimento compatível com o perfil PSE **não foi localizado** no clone analisado; não permite concluir sobre base legal, governança ou tratamento de dados fora do repositório | `ausencia-de-evidencia-pse` |
| 3 | S-04 | ALTO | `src/response_schemas.py:141` | Regra identificou host externo sem manifesto — host de documentação de biblioteca de terceiros (página de erros de validação) referenciado em schema de resposta; a inspeção manual deve determinar se é integração operacional, documentação, exemplo ou metadado (valor `[REDACTED-HOST]`) | `possivel-falso-positivo` (leitura preliminar: referência de documentação/metadado) |
| 4 | S-04 | ALTO | `docs/examples/get_token_example.py:4` | Regra identificou host externo sem manifesto — URL de hospedagem de código em arquivo de **exemplo** sob `docs/examples/`; a inspeção manual deve classificar o uso (valor `[REDACTED-HOST]`) | `possivel-falso-positivo` (leitura preliminar: exemplo de documentação) |

**Formulação responsável (mesmo padrão da rodada B):** nenhum achado desta tabela deve ser lido como "problema confirmado" da API PGD. P-04/P-07: *"não foi localizado, no clone analisado, o artefato declarativo esperado pelo perfil PSE — isso não permite concluir sobre controles organizacionais fora do repositório"*. S-04: *"a regra identificou hosts externos; a inspeção manual deve determinar se são integrações operacionais, documentação, exemplos ou metadados"* — e, nos dois casos deste alvo, a inspeção preliminar indica superfícies de documentação/exemplo, não integrações operacionais; a dúvida permanece visível na classificação, conforme o princípio da ratificação 11. Nenhum valor, host ou literal sensível é reproduzido neste material.

Distribuição por pilar: privacy 2 (P-04, P-07) · security 2 (S-04×2) · ethics 0 (pack fora de escopo).
Distribuição por severidade: ALTO 4 · MÉDIO 0 · CRÍTICO 0.
Divergências notáveis em relação à rodada B: **P-06 não emitiu achado** (nenhum padrão de credencial no substrato — na rodada B foram 2 MÉDIO em fixture de teste) e **S-04 apontou superfícies de documentação/exemplo** (na rodada B, integrações operacionais em código + 1 URL de autopresentação). O padrão P-04/P-07 de ausência declarativa, por outro lado, reproduziu-se de forma idêntica — é o resultado central da comparação (relatório 05).

## 4. Cobertura por linguagem (bloco `alcance` do laudo)

| Linguagem | Arquivos | Ferramenta | Estado |
|---|---|---|---|
| Python | 31 | `ast (stdlib)` | lido |
| YAML | 3 | PyYAML | lido |
| JSON | 3 | PyYAML | lido |
| SQL | 1 | regex sobre código efetivo | lido |
| fora de alcance | 0 | — | **nenhum arquivo fora de alcance** |

O laudo declara textualmente: "Todo arquivo de codigo ou declaracao do alvo esta em linguagem que a suite le, ou em linguagem de alcance parcial declarado" — e a nota padrão de que ausência de achado não é atestado de conformidade vale na íntegra. Comparação factual com a rodada B: o alvo B teve 2 arquivos fora de alcance (`.zip`, `.xcf`); o alvo A teve nenhum. Os demais arquivos do clone (markdown, imagens, Dockerfile, Makefile) não aparecem no bloco `lidos` nem em `fora_de_alcance` — mesma observação registrada na rodada B: tratados como não lidos/não declarados no escopo observado.

## 5. Observações de comportamento relevantes

1. **Cobertura parcial explícita, idêntica à rodada B:** P-07 e P-09 executaram a metade estática no inventário e a suite registrou em `relatorios.cobertura_parcial`: "metade runtime nao executada: Trabalho A nao habilitado…". O estado "executado" novamente não significou "totalmente executado".
2. **Correlação estático×dinâmico:** o bloco `correlacoes` veio populado com o par S-04×S-18 ("terceiro tratando dado do titular sem estar declarado") no cenário `so_na_camada_estatica`, com a mesma leitura honesta da rodada B — "defeito que a observação não exercitou"; nenhum finding foi removido por falta da dinâmica. (A correlação P-06×S-20, presente na rodada B, não veio — não há P-06 neste alvo.)
3. **Sanitização com as mesmas regras:** os hosts externos apontados por S-04 foram mascarados como `[REDACTED-HOST]` no material sanitizado — inclusive quando a própria suite os insere em títulos de findings — por consistência com o protocolo da rodada B, ainda que a inspeção preliminar os classifique como documentação/exemplo. Nenhum segredo, literal sensível ou dado pessoal consta dos anexos sanitizados.
4. **Sem config, a suite não fabrica:** `config_fingerprint: null`; packs declarados `[ethics, privacy, security]`; `packs_desabilitados` vazio; `packs_fora_de_escopo` com o motivo computado do ethics — observação idêntica à da rodada B.
5. **Recusa versus laudo:** a execução não foi recusada (exit ≠ 30) mesmo sem config; a suite registrou as ausências declarativas como achado (P-04/P-07) em vez de calar — mesmo comportamento estrutural observado no alvo B, agora confirmado em um segundo perfil arquitetural.

## 6. Tempo de execução e esforço

A execução completa do inventário levou **2,4 s** sobre 38 arquivos em linguagens lidas (31 Python + 3 YAML + 3 JSON + 1 SQL), com 0 arquivos fora de alcance declarado. O padrão de custo da rodada B repete-se: o esforço de *preparação* (clone, venv, estudo de contratos, congelamento e registro de proveniência) domina o custo total, e a execução é uma fração de segundos — assimetria favorável à adoção como etapa de CI contínuo, agora observada em dois perfis arquiteturais distintos sob a mesma instrumentação.
