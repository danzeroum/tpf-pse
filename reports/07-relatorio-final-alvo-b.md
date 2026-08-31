# 07 — Relatório final da rodada (TPF — Projeto Técnico, rodada 2)

## Avaliação exploratória da aplicabilidade da PSE Suite em um projeto público de engenharia de dados baseado em Airflow

**Pós-Graduação em Arquitetura e Engenharia de Software — FIA Online**
**Modalidade:** Projeto Técnico · **Rodada:** 2 (perfil engenharia de dados / Airflow)
**Data de fechamento:** 2026-08-31 (UTC)
**Revisão v3:** nota metodológica formal dos quatro indicadores (§10.1), precisão das contagens de testes e mutações (§1, §6) e comparação A × B executada com a rodada A (API PGD) recuperada por re-execução local (§11).
**Revisão v3.1 (pós-parecer + rodada C):** notas de interpretação do parecer da v3 incorporadas (§10.1, §11 — formulação defensável da partição e complemento da métrica) e rodada C executada sobre alvo de IA (LlamaFactory @ `d6bb97d`, emenda de protocolo nº 2 — quinto clone), com pré-triagem pré-registrada (`matrices/pre-triagem-alvo-c.md`); síntese do corpus A × B × C no relatório 08.

---

## 1. Resumo executivo

Esta rodada aplicou a PSE Suite v0.20.0 — suite de evidências de Privacidade, Segurança e Ética por Design — em **avaliação exploratória, estática e somente leitura** sobre o repositório público `gestaogovbr/FastETL` (plugin Apache Airflow para pipelines de dados), commit congelado `9fb5d596`. A suite foi instalada em venv isolado, autoprova executada com êxito (58 mutações canônicas do catálogo congelado, 0 falhas) e, na configuração local descrita na proveniência, a execução da suíte retornou 809 testes aprovados e 10 pulados, sem falhas. O modo `pse_inventory` executou em 2,0 s e produziu laudo com **exit 11**: 18 checks executados, 25 pulados com motivo, 15 não habilitados, 0 indeterminados, **8 achados** (6 ALTO, 2 MÉDIO) — todos sanitizados e classificados por validação humana (3 confirmados-no-escopo, 2 ausência-de-evidência-PSE, 3 possíveis falsos positivos). Oito mutações controladas em cópias descartáveis provaram que a régua morde vetores plantados (P-01 CRÍTICO, S-06 CRÍTICO, S-04 ALTO, P-20 ALTO, trava de doc, declaração de alcance) e revelaram comportamento fail-closed relevante (declaração sem insumo → exit 20). A pergunta de pesquisa — *como uma suite de governança como código se comporta sobre um repositório público de engenharia de dados em Python/Airflow* — recebeu resposta empírica: o comportamento é dominado pela **ausência de artefatos declarativos** (catálogo, manifesto, consent, lineage), que a suite registra por achado ou pulo com motivo. No escopo e na versão avaliados, a PSE Suite preservou estados distintos para achados, itens pulados, checks não habilitados, cobertura parcial e superfícies fora de alcance; não foi observado, nesta rodada, colapso desses estados em uma conclusão global de conformidade. A guarda de escopo da ética funcionou; e a assimetria biblioteca × operador de dados é o principal limite de adoção. A contribuição central que esta rodada consolida, junto com a rodada A (API PGD, recuperada por re-execução local sob a mesma instrumentação — relatório 05), é: **a governança como código precisa distinguir controles inerentes ao componente de software de controles que dependem do contexto operacional do consumidor**. Nada neste estudo afirma vulnerabilidade, desconformidade ou falha do alvo.

## 2. Objetivo da rodada e pergunta de investigação

**Pergunta:** como uma suite de governança como código se comporta, em termos de cobertura, evidências, achados, limitações e esforço de adoção, quando aplicada estaticamente a um repositório público de engenharia de dados baseado em Python e Airflow? O foco não é encontrar falhas de um órgão público nem auditar: é avaliar a aplicabilidade, cobertura, precisão, limites e oportunidades de evolução da própria PSE Suite num perfil arquitetural distinto do da rodada A (API PGD, relatório 05).

## 3. Delimitação ética, técnica e operacional

- **Somente clones locais** dos três repositórios públicos; sem fork, commit, push, issue, PR ou qualquer interação remota além do clone.
- **Sem rede além do clone e do `pip install` da suite**; sem Docker, Airflow, banco, worker, scheduler, DAG, navegador ou qualquer serviço; sem credenciais de terceiros.
- **Sem alteração dos clones**; mutações apenas em cópias descartáveis (`evidence/raw/mutacoes/`), verificadas por `git status --porcelain` vazio ao final.
- **Sanitização obrigatória:** nenhum segredo, literal sensível, dado pessoal ou valor de configuração é reproduzido — `[REDACTED]` + tipo de indício + check + `arquivo:linha`.
- **Linguagem controlada:** nenhum veredito global de segurança, conformidade LGPD ou certificação; nenhuma afirmação sobre FastETL, mantenedores ou órgãos públicos.

## 4. Caracterização da PSE Suite

Síntese do relatório 01: padrão externo versionado (régua em `pse/data/`, consumida e nunca copiada), catálogo declarativo de **58 checks** (35 estáticos/inventory, 11 passivos, 12 ativos) sobre três pilares (privacy 22, security 22, ethics 14) e cinco domínios; veredito não binário com cinco exit codes; autoprova obrigatória com mutação canônica por check; sanitização nativa da evidência; procedência completa no bloco `artifact` (`suite_version`, `schema_version`, `catalog_hash`, `repo_commit`, `config_fingerprint`); travas de consistência de documentação gerada e de ratificações seladas (15); "buracos assumidos" documentados (P-21, acesso do titular, revogação downstream). Versão congelada estudada: **0.20.0**, `catalog_hash 4682a4ae…a0ac`, schema `laudo-pse-1.0`.

## 5. Caracterização factual do FastETL

Síntese do relatório 02: pacote de plugins/provider para Apache Airflow (≥2.3) para replicação de tabelas (SQL Server/Postgres/MySQL), cargas de GSheets/Samba, extração CSV, patching de dados, integrações CKAN/dados.gov.br/OSRM/DOU; 43 arquivos Python (~8.000 linhas) mais fixtures de teste, Dockerfile, Makefile (que provisiona Airflow via Docker — **não executado**), 3 workflows de CI; GPLv3 no `LICENSE` (divergência documental com o `setup.py` registrada de forma neutra). Superfícies estáticas relevantes: logging denso, uso idiomático de Connections do Airflow, integrações externas nomeadas, ausência total de catálogo/manifesto/declarações PSE.

## 6. Método e reprodutibilidade

Procedimento em 12 fases com proveniência congelada por SHA (`evidence/provenance/00-provenance.json`), comandos exatos com código de saída e duração registrados, e hashes SHA-256 de todos os anexos. Reprodução segura: seguir o `README.md` da raiz do estudo — ambiente, instalação, ordem de execução e regras de sanitização estão prescritos. Divergência ambiente×manifesto registrada (809/10 testes na configuração local descrita na proveniência vs. 798/8 no manifesto v0.20.0 — Python 3.12 vs. 3.11), como exemplo do que o bloco `artifact` torna visível: as contagens de teste — como as mutações canônicas — estão associadas ao commit, ao catálogo e ao ambiente congelados, e não são propriedade permanente do produto.

## 7. Resultado da execução estática

Comando: `pse --path repos/FastETL --modo pse_inventory --output evidence/raw/laudo-alvo-b-bruto.json` · exit **11** · 2,0 s · laudo bruto `evidence/raw/laudo-alvo-b-bruto.json` (sha256 `7201c25c…1a61d`; re-execução determinística após padronização de nomenclatura — detalhes no relatório 03).

| Estado | N | Observação |
|---|---|---|
| Executados | 18 | 4 com achado (checks distintos); 14 limpos sobre substrato lido |
| Pulados | 25 | motivos computados (guarda E-00, catálogo ausente, manifesto ausente, sem treino, sem API…) |
| Não habilitados | 15 | Trabalho A sem `target` (não pedido, por protocolo) |
| Indeterminados | 0 | — |
| Previstos não implementados | 0 | catálogo inteiro implementado |

Findings (8): P-04 ALTO (artefato declarativo de catálogo não localizado no clone) · P-07 ALTO (modelo de consentimento compatível com o perfil PSE não localizado — sem conclusão sobre base legal ou tratamento fora do repositório) · S-04 ALTO ×4 (regra identificou hosts de terceiro sem manifesto — 3 integrações reais em código + 1 URL de autopresentação; a inspeção manual deve determinar se são integrações operacionais, documentação, exemplos ou metadados) · P-06 MÉDIO ×2 (padrão de credencial em fixture de teste; classificação deve registrar se é exemplo sintético ou segredo real — valor `[REDACTED]`). Cobertura de linguagem: Python 43, YAML 5, SQL 5, shell 1 lidos; 2 arquivos fora de alcance declarados; nota anti-silêncio do laudo reproduzida no relatório 03.

## 8. Validação manual e classificação responsável

Relatório 04: cada achado recebeu classificação humana com justificativa — **ausencia-de-evidencia-pse** para P-04/P-07 (artefato do padrão não localizado no clone; não conclui ausência de controle organizacional nem permite concluir sobre base legal, governança ou tratamento fora do repositório); **confirmado-no-escopo** para 3 dos S-04 (integração de terceiro existe em código — fato técnico, não violação); **possivel-falso-positivo** para o S-04 de User-Agent e para os 2 P-06 de fixture (com a dúvida mantida visível, conforme ratificação 11). Discussão de validade explícita: ausência de achado ≠ ausência de risco; achado ≠ violação.

## 9. Mutações controladas

Matriz `matrices/mutacoes-e-resultados.md` (M1–M8, incluindo desdobramento M7a/M7b): 7 detecções exatas (P-01 CRÍTICO, S-06 CRÍTICO, S-04 sobre host sintético, P-20 ALTO, trava de doc no corpo, declaração de alcance, reabertura do pack ethics), 1 parcial analisada (M4: P-04 cessou, P-02 mordeu a nova declaração, P-18 não disparou porque a mutação plantou `personal` e o vetor do check é `sensitive` — erro de experimento documentado, não lacuna). Aprendizados: superfície declarativa nova ativa família de checks; declaração de escopo sem insumo vira bloqueio (exit 20); assimetria e-mail×URL de domínio reservado confirmada em execução.

## 10. Cobertura, aplicabilidade e limites

Matriz central (`matrices/requisito-check-evidencia-limite.md`) cobre os 58 checks com os grupos exigidos: verificado / encontrado / não verificável / não aplicável / dependente de contexto organizacional / sugestão de evolução. Limites estruturais observados: (i) **biblioteca × operador** — checks declarativos cobram do repositório artefatos que pertencem a quem opera pipelines, não a quem distribui o plugin; (ii) superfícies de data lake/IAM fora do alcance estático declarado ("buracos assumidos"); (iii) a metade runtime do corpus é inacessível sem Trabalho A; (iv) 0 indeterminados — no escopo desta rodada, a suite sempre decidiu ou explicou por que não decidiu.

### 10.1 Nota metodológica — definição formal dos quatro indicadores (parecer)

Conforme solicitado pelo parecer da orientação, os quatro indicadores usados nesta rodada e na rodada A têm definição formal única, com regra de classificação de precedência declarada e codificada em `scripts/10_analise_revisao.py` (alvo B) e `scripts/11_analise_alvo_a.py` (alvo A):

| Indicador | Fórmula | Valor (idêntico em A e B) | Interpretação |
|---|---|---|---|
| Cobertura bruta | executados ÷ catálogo total | 18/58 | Percentual de todos os checks do catálogo executados no alvo |
| Cobertura aplicável | executados ÷ (catálogo − guarda E-00 − Trabalho A) | 18/29 (62%) | Percentual executado entre checks potencialmente aplicáveis ao perfil observado |
| Não aplicáveis | guarda E-00 + vetor estrutural ausente | 17 (14 + 3) | Checks não pertinentes ao perfil do alvo (ética/IA; treino/barramento sem corpus de IA) |
| Dependentes de contexto | artefato declarativo ausente + Trabalho A | 23 (8 + 15) | Checks que exigem artefato, declaração, escopo autorizado ou ambiente não presente no clone |

**Regra de classificação (precedência declarada 1→4; cada regra só se aplica se a anterior não se aplicar):**
1. Check executado (com ou sem achado) → categoria *executados*.
2. Pulo emitido pela guarda E-00 (pack de ética fora de escopo) → *não aplicáveis*.
3. Pulo cujo motivo indica vetor estruturalmente ausente no perfil sem IA ("nenhuma chamada de treino…", "nenhuma produção de evento em barramento append-only…") → *não aplicáveis*.
4. Demais pulos (artefato declarativo ausente: catálogo, manifesto, contrato de API, residência, finalidade) e todos os não habilitados (Trabalho A sem alvo autorizado) → *dependentes de contexto*.

**Exclusividade mútua, declarada explicitamente conforme o parecer:** cada um dos 58 checks recebe exatamente um estado no laudo e exatamente uma categoria pela regra acima — nenhuma regra sobrepõe-se a outra. A soma **18 + 17 + 23 = 58 é, portanto, partição mutuamente exclusiva do catálogo**, verificada por asserção nos dois alvos. A razão 18/29 tem denominador próprio (29 = 58 − 14 − 15) e **não participa da partição**: os 3 checks de vetor estrutural ausente permanecem no denominador da cobertura aplicável por serem condicionalmente aplicáveis (o perfil poderia ter chamadas de treino/barramento), enquanto o indicador 3 os registra como não aplicáveis ao corpus efetivamente observado — as duas métricas respondem a perguntas distintas e não são aditivas. Os indicadores descrevem o que o instrumento conseguiu exercer neste perfil; não medem qualidade do alvo nem segurança do corpus.

**Formulação segura para citação (registrada a partir do parecer da v3; não altera resultados):** *"Na classificação metodológica adotada para os dois alvos, 18 dos 29 checks considerados potencialmente aplicáveis ao perfil observado foram executados. Os 17 restantes foram classificados como não aplicáveis e 23 como dependentes de contexto, artefatos declarativos ou condições não presentes no clone analisado."* — em substituição a qualquer uso absoluto de "62% de cobertura". Complemento obrigatório: *"Essa métrica mede aplicabilidade do catálogo no recorte estático adotado; ela não mede cobertura universal de privacidade, segurança, ética, código ou requisitos legais."*

## 11. Comparação metodológica com a rodada API PGD

Relatório 05: a rodada A (API PGD) foi **recuperada por re-execução local sob a mesma instrumentação congelada** — mesmo clone da suite (v0.20.0), mesmo `catalog_hash`, mesmo modo, mesmo Python, mesmo SO, mesmos critérios de classificação humana e regras de sanitização; emenda de protocolo declarada para o quarto clone (`gestaogovbr/api-pgd` @ `9d4b774c`, tag `3.3.10`). A comparação foi **executada** com paridade total nos dez fatores de proveniência exigidos pelo parecer: exit 11 em ambos os alvos; partição do catálogo idêntica e mutuamente exclusiva (18 executados + 17 não aplicáveis + 23 dependentes de contexto = 58 nos dois); findings 4 (4 ALTO) × 8 (6 ALTO, 2 MÉDIO); falsos positivos preliminares 2/4 × 3/8; o par P-04/P-07 reproduziu-se nos dois alvos, P-06 só no alvo B, e as superfícies S-04 de documentação/exemplo (alvo A) contrastam com as integrações operacionais e fixture (alvo B). Ameaças à comparabilidade declaradas no relatório 05 (§5) — em especial: a rodada A é execução de recuperação sobre o estado atual do alvo, não o laudo histórico da rodada 1, e a igualdade das partições é observação desta comparação controlada, não lei geral. Critério pré-registrado para um terceiro alvo permanece: somente um repositório com uso explícito de IA, para cobrir a lacuna conceitual do pilar de ética — nunca motivado por "precisar dar findings".

**Formulação defensável registrada a partir do parecer da v3 (não altera resultados):** a igualdade da partição nos dois alvos **não prova equivalência de maturidade de segurança, privacidade ou conformidade** entre os projetos — mostra que, sob o modo estático e o perfil atual da suite, os dois repositórios apresentam estruturas de aplicabilidade semelhantes (predominantemente Python, sem sistema de IA exposto no clone, sem os artefatos declarativos que vários checks exigem), e que essa paridade decorre, em parte, do perfil dos alvos e da configuração da suite. A conclusão defensável integral consta do relatório 05 (§2.1, nota de interpretação).

**Rodada C (alvo de IA) executada após este relatório:** conforme o critério pré-registrado, a terceira rodada foi realizada sobre `hiyouga/LlamaFactory` @ `d6bb97d` (framework de fine-tuning de LLMs, Apache-2.0) — emenda de protocolo nº 2, pré-triagem pré-registrada em `matrices/pre-triagem-alvo-c.md`. Resultado sintético: guarda E-00 em escopo por fato computado (pack de ética sem nenhum check fora de escopo pela guarda); partição deslocada para **25 executados + 2 não aplicáveis + 29 dependentes de contexto + 2 indeterminados = 58** — primeiro veredito `indeterminado` do corpus (exit 20), com E-06 e P-15 recusando decisão por falta de substrato; 21 findings com 12 possíveis falsos positivos preliminares de alta especificidade de perfil (parsing de dataset, contexto de decisão em rotinas de treino, superfícies de CI × UI). Detalhes nos relatórios 02/03-alvo-c e síntese A × B × C no relatório 08.

## 12. Recomendações de evolução da PSE Suite

1. **S-04:** distinguir URL de autopresentação (User-Agent, referência ao próprio projeto) de egresso de terceiro — elimina o único falso positivo sistêmico desta rodada sem suprimir achados reais.
2. **Estado "biblioteca redistribuível":** checks declarativos (P-04/P-07 e dependentes) poderiam reconhecer o perfil de plugin/library e derivar a responsabilidade do artefato para o operador, evitando ALTO sistemático em repositórios de biblioteca.
3. **Herdar a guarda E-00** para S-10/S-11/S-13 (domínio `ai`/`api` sem IA no corpus executaram limpos sem utilidade informativa).
4. **Sinal de subdeclaração de catálogo:** catálogo existente com nenhum campo `sensitive` merecer nota no laudo (o caso M4 mostrou que o vetor depende da classe declarada).
5. **E-08 para Airflow:** candidatos padrão de lineage para pipelines Airflow (ex.: metadados de DAG/XCom/datasets) aumentariam muito o valor da suite no perfil engenharia de dados.
6. **Leitura declarativa de Dockerfile/workflows:** hoje fora do bloco `lidos`; um check de superfície de configuração (sem parser pesado) fecharia o vão visível nesta rodada.

## 13. Plano de adoção/piloto futuro

Relatório 06 (hipótese, nada executado): repositório voluntário autorizado; estático sem rede como etapa inicial; baseline de alertas com política "alertar antes de bloquear"; revisor técnico + DPO para interpretar controles; sanitização e retenção protegidas; triagem humana com as categorias desta rodada; métricas de adoção (cobertura, tempo, confirmação humana, ruído, indeterminados, esforço); calibração com regressão; expansão para passiva/dinâmica/ativa apenas em homologação isolada com autorização e identidades sintéticas. Todos os números são hipóteses a calibrar.

## 14. Conclusão

No escopo observado, a PSE Suite comportou-se sobre um repositório público de engenharia de dados em Python/Airflow com **exatamente a honestidade que declara**: decidiu onde pôde (18 checks), explicou cada não-decisão (25 pulos com motivo computado), recusou-se a fingir leitura (bloco `alcance`), registrou ausências declarativas como achado (P-04/P-07) em vez de calar, mordeu vetores plantados (7 de 8 mutações) e manteve a dúvida visível onde o contexto impedia conclusão (ratificação 11). O esforço de adoção concentra-se na **preparação** (estudo de contratos, venv, artefatos declarativos), não na execução (segundos por rodada) — assimetria favorável ao CI. O limite estrutural desta rodada é o mesmo do alvo: a biblioteca distribui a capacidade; os artefatos de governança pertencem ao operador. É essa fronteira — e não qualquer veredito sobre o FastETL — que define a agenda do piloto futuro e da evolução da suite.

## 15. Anexos

| Anexo | Caminho | sha256 (preenchido em `00-provenance.md` final) |
|---|---|---|
| Proveniência JSON | `evidence/provenance/00-provenance.json` | ver tabela final |
| Proveniência narrada | `reports/00-provenance.md` | — |
| Caracterização PSE | `reports/01-caracterizacao-pse-suite.md` | — |
| Caracterização do alvo | `reports/02-caracterizacao-alvo-b.md` | — |
| Execução e resultados | `reports/03-execucao-alvo-b.md` | — |
| Validação manual | `reports/04-validacao-manual-e-limitacoes.md` | — |
| Comparação rodada A × B | `reports/05-comparacao-api-pgd-alvo-b.md` | — |
| Pré-triagem do alvo C | `matrices/pre-triagem-alvo-c.md` | — |
| Caracterização do alvo C (IA) | `reports/02-caracterizacao-alvo-c.md` | — |
| Execução do alvo C (IA) | `reports/03-execucao-alvo-c.md` | — |
| Matriz de estados do alvo C | `matrices/estados-por-check-alvo-c.md` | — |
| Laudo bruto do alvo C (não divulgar) | `evidence/raw/laudo-alvo-c-bruto.json` | — |
| Laudo sanitizado do alvo C | `evidence/sanitized/laudo-alvo-c-sanitizado.json` | — |
| Resumo executivo sanitizado do alvo C | `evidence/sanitized/resumo-executivo-laudo-alvo-c.md` | — |
| Síntese do corpus A × B × C | `reports/08-sintese-corpus.md` | — |
| Caracterização do alvo A | `reports/02-caracterizacao-alvo-a.md` | — |
| Execução do alvo A (recuperação) | `reports/03-execucao-alvo-a.md` | — |
| Matriz de estados do alvo A | `matrices/estados-por-check-alvo-a.md` | — |
| Laudo bruto do alvo A (não divulgar) | `evidence/raw/laudo-alvo-a-bruto.json` | — |
| Laudo sanitizado do alvo A | `evidence/sanitized/laudo-alvo-a-sanitizado.json` | — |
| Resumo executivo sanitizado do alvo A | `evidence/sanitized/resumo-executivo-laudo-alvo-a.md` | — |
| Piloto futuro | `reports/06-plano-piloto-adocao.md` | — |
| Pré-triagem | `matrices/cobertura-por-artefato.md` | — |
| Mutações | `matrices/mutacoes-e-resultados.md` | — |
| Matriz central | `matrices/requisito-check-evidencia-limite.md` | — |
| Laudo bruto (não divulgar) | `evidence/raw/laudo-alvo-b-bruto.json` | — |
| Laudo sanitizado | `evidence/sanitized/laudo-alvo-b-sanitizado.json` | — |
| Resumo executivo sanitizado | `evidence/sanitized/resumo-executivo-laudo.md` | — |
| Resultados das mutações | `evidence/raw/mutacoes-resultados.json` | — |
| Logs de execução | `evidence/raw/manifesto-pse.txt`, `self-test.txt`, `pytest-pse-suite.txt`, `comando-inventory.txt` | — |

---

**Declaração final obrigatória:** Esta avaliação foi realizada sobre clones locais de código público, em modo estático e somente leitura, limitada aos commits e artefatos observados. Seus resultados não constituem auditoria institucional, certificação de segurança, parecer jurídico de conformidade, teste em produção ou comprovação de ausência de riscos.
