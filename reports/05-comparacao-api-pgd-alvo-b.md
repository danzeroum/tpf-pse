# 05 — Comparação metodológica entre as rodadas A (API PGD) e B (FastETL)

## 1. Recuperação da rodada A por re-execução local

Os insumos originais da rodada 1 (API PGD) não estavam disponíveis neste ambiente — nenhuma pasta, laudo ou matriz da rodada anterior foi encontrado no sistema de arquivos local (registro formal na v2 deste documento). Conforme a sequência recomendada pelo parecer da orientação, a rodada A foi então **recuperada por re-execução local** com a instrumentação congelada desta rodada B, e o protocolo recebeu uma **emenda declarada**: um quarto clone público (`gestaogovbr/api-pgd`, congelado em `9d4b774c`, tag `3.3.10`) foi acrescentado aos três originais, sob as mesmas restrições — modo estático `pse_inventory`, somente leitura, sem execução da aplicação, sem banco, sem rede além dos clones, sanitização integral e verificação de clone intacto.

Parâmetros da recuperação, todos idênticos aos da rodada B por construção (mesmo clone da suite, mesmo venv, mesma máquina): suite `pse-suite` @ `443da92` (v0.20.0), `catalog_hash 4682a4ae…a0ac`, schema `laudo-pse-1.0`, modo `pse_inventory`, Python 3.12.14, Debian GNU/Linux 13, mesmas categorias de classificação humana, mesmas regras de sanitização. Execução registrada em `reports/03-execucao-alvo-a.md` (exit 11, 2,4 s, laudo bruto `evidence/raw/laudo-alvo-a-bruto.json`, sanitizado `evidence/sanitized/laudo-alvo-a-sanitizado.json`).

Consequência metodológica: a comparação abaixo é **executada** — não sobre os laudos históricos da rodada 1, cujos insumos permanecem indisponíveis, mas sobre uma execução nova e congelada do mesmo instrumento sobre o mesmo tipo de alvo (API Python do Programa de Gestão). Quando os insumos originais forem localizados, esta execução deverá ser reconciliada com eles (ameaça declarada no §5).

## 2. Quadro de comparação (colunas preenchidas a partir dos laudos congelados)

| Métrica | API PGD — rodada A (recuperada) | FastETL — rodada B (laudo congelado) | Interpretação permitida |
|---|---|---|---|
| Linguagem/arquitetura | API Python pública (FastAPI 0.111 + SQLAlchemy 2.0.31 + Pydantic 2.8.2), aplicação completa, AGPLv3, commit/tag `9d4b774c`/`3.3.10` | Plugin/provider Python + Airflow (biblioteca distribuída de operadores/hooks), GPLv3 no LICENSE (divergência com setup.py registrada), commit `9fb5d596` | Perfis arquiteturais distintos exercem subsets diferentes do catálogo |
| Checks executados | 18 de 58 (bruta) · 18/29 (62% sobre potencialmente aplicáveis) | 18 de 58 (bruta) · 18/29 (62% sobre potencialmente aplicáveis) | **Mesma instrumentação → mesma distribuição estrutural de estados** (ver partição no §2.1) |
| Findings por pilar | privacy 2 (P-04, P-07) · security 2 (S-04×2) · ethics 0 | privacy 4 (P-04, P-07, P-06×2) · security 4 (S-04×4) · ethics 0 | Contagem bruta não é ranking de segurança; os pares P-04/P-07 reproduzem-se nos dois alvos |
| Severidades | 4 ALTO · 0 MÉDIO · 0 CRÍTICO | 6 ALTO · 2 MÉDIO · 0 CRÍTICO | Semântica interna da suite, não classificação jurídica |
| Pulados / não habilitados | 25 pulados com motivo · 15 não habilitados | 25 pulados com motivo · 15 não habilitados | Dependência de artefatos declarativos e de escopo do Trabalho A é estrutural, não idiossincrática do alvo |
| Indeterminados / fora de alcance | 0 indeterminados · **0 arquivos fora de alcance** (Python 31, YAML 3, JSON 3, SQL 1) | 0 indeterminados · **2 arquivos fora de alcance** (`.zip`, `.xcf`; Python 43, YAML 5, SQL 5, shell 1) | Limites de observação declarados pelo laudo de cada alvo |
| Falsos positivos conhecidos (triagem humana) | 2 de 4 — os 2 S-04 (`possivel-falso-positivo`: host de documentação de biblioteca em schema de resposta; URL de hospedagem de código em `docs/examples/`) | 3 de 8 — 2×P-06 em fixture de teste e 1×S-04 (URL de autopresentação em User-Agent) | Insumo de calibração da suite, não acusação; em ambos os alvos a leitura preliminar aponta documentação/exemplo, não integração operacional |
| Achados P-06 (credencial) | **nenhum** (check executado limpo) | 2 MÉDIO em fixture de teste (`possivel-falso-positivo`) | O substrato de teste dos alvos difere; a regra não emitiu achado sem vetor |
| Principais lacunas | Ausência de artefatos declarativos (catálogo, consent, manifesto) — padrão dominante | Ausência de artefatos declarativos + responsabilidade distribuída entre biblioteca e operador | Roadmap da PSE (perfis de aplicação/adapters), não veredito sobre os alvos |
| Exit code do laudo | 11 (ALTO sem CRÍTICO) | 11 (ALTO sem CRÍTICO) | Semântica definida pela suite; não é classificação jurídica |

### 2.1 Partição do catálogo nos dois alvos (categorias mutuamente exclusivas)

| Categoria (regra no relatório 07, §10.1) | API PGD (A) | FastETL (B) |
|---|---|---|
| Executados | 18 | 18 |
| Não aplicáveis (guarda E-00: 14 + vetor estrutural ausente: 3) | 17 | 17 |
| Dependentes de contexto (artefato declarativo ausente: 8 + Trabalho A: 15) | 23 | 23 |
| **Partição** | **18 + 17 + 23 = 58** ✔ | **18 + 17 + 23 = 58** ✔ |

A igualdade das partições é um **achado da comparação sob instrumento idêntico**: dois perfis arquiteturais diferentes (aplicação API × biblioteca/pipeline) produziram exatamente a mesma estrutura de estados — o que reforça que a partição é propriedade da interação catálogo×perfil, e não idiossincrasia de um alvo. O que difere é o conteúdo: quais checks emitiram findings (4 × 8) e sobre que tipo de superfície (documentação/exemplo × integrações operacionais + fixture).

**Nota de interpretação registrada a partir do parecer da revisão v3 (não altera resultados):** a igualdade da partição 18 + 17 + 23 = 58 nos dois alvos **não prova que API PGD e FastETL tenham o mesmo nível de governança, segurança ou privacidade**. Ela mostra que, sob o modo estático e o perfil atual da PSE Suite, os dois repositórios apresentam estruturas de aplicabilidade semelhantes: são predominantemente Python, não expõem um sistema de IA no clone analisado e não fornecem os artefatos declarativos que vários checks exigem. A conclusão defensável da comparação é: *"Nos dois repositórios Python avaliados, a PSE Suite apresentou comportamento estrutural semelhante no modo estático: 18 checks executados, 17 não aplicáveis e 23 dependentes de contexto ou artefatos externos. Essa paridade decorre, em parte, do perfil dos alvos e da configuração da suite, e não deve ser interpretada como equivalência de maturidade de segurança, privacidade ou conformidade entre os projetos."* Os checks ausentes ou não aplicáveis podem depender de: catálogo de dados no formato esperado pela PSE; modelo de consentimento; manifesto de integrações de terceiros; informações de residência de dados; especificação OpenAPI estática; artefatos de IA/ML, model card, decisões automatizadas ou dataset de treinamento; e configuração operacional que não existe no clone público — dependências que a própria documentação da suite reconhece ao declarar que itens pulados, indeterminados, não habilitados ou fora de alcance não devem ser interpretados como conformidade.

## 2.5 Paridade de proveniência entre as rodadas (10 fatores do parecer)

| Fator | Rodada A (recuperada) | Rodada B | Paridade |
|---|---|---|---|
| Versão da PSE Suite | 0.20.0 | 0.20.0 | ✔ idêntica |
| Commit da PSE Suite | `443da92dbdb22a9af18aa6eebb51aac2da901458` | `443da92dbdb22a9af18aa6eebb51aac2da901458` | ✔ mesmo clone congelado |
| `catalog_hash` | `4682a4ae1115e577e95e2ddbd666bfd041efb2fca4b3d77e7683e2055571a0ac` | idem | ✔ idêntico |
| `schema_version` | `laudo-pse-1.0` | `laudo-pse-1.0` | ✔ idêntico |
| Modo de execução | `pse_inventory` | `pse_inventory` | ✔ idêntico |
| Versão do Python | 3.12.14 | 3.12.14 | ✔ idêntico |
| Sistema operacional | Debian GNU/Linux 13 (trixie), x86_64 | idem | ✔ idêntico |
| Critérios de classificação humana | `ausencia-de-evidencia-pse`, `confirmado-no-escopo`, `possivel-falso-positivo` (com dúvida preservada) | idem | ✔ mesmas categorias |
| Regras de sanitização | redação de credencial (regra preventiva P-06), mascaramento de hosts como `[REDACTED-HOST]`, varredura global | idem (`scripts/06` / `scripts/12` — mesmas regras) | ✔ equivalentes |
| Formato de laudo | `laudo-pse-1.0` (JSON) + sanitização + resumo executivo | idem | ✔ idêntico |

Nenhum dos dez fatores difere entre as rodadas — a comparação é, portanto, controlada por instrumento. As diferenças restantes entre os alvos (tamanho, domínio, perfil) são atributos dos alvos, não da instrumentação, e devem ser lidas como variáveis explicativas, nunca como ranking (§4).

## 3. Consolidação metodológica das duas rodadas

Com os dois laudos congelados sob a mesma instrumentação, o quadro metodológico abaixo — registrado a partir do parecer da orientação — é sustentado por evidência de ambos os alvos, em nível estritamente metodológico (sem qualquer leitura classificatória dos alvos):

| Questão | API PGD (rodada A) | FastETL (rodada B) | Aprendizado para a PSE |
|---|---|---|---|
| Perfil arquitetural | API Python pública, ligada ao Programa de Gestão (aplicação completa) | Biblioteca/pipeline Apache Airflow (plugin de engenharia de dados) | A suite precisa de perfis de aplicação |
| Artefatos de governança | Ausentes do repositório (P-04/P-07 em ambos; manifesto ausente para os S-04) | Ausentes ou pertencentes ao operador do pipeline | Checks declarativos precisam de contexto |
| Pilar de ética/IA | Guarda E-00: 14 checks fora de escopo | Guarda E-00: 14 checks fora de escopo | É necessário um alvo com IA para avaliar esse pilar |
| Cobertura de código Python | Potencialmente alta — e realizada (31 arquivos por AST, 0 fora de alcance) | Potencialmente alta — e realizada (43 arquivos por AST; 2 fora de alcance) | Python é boa base para o experimento |
| Principais limitações | Artefatos declarativos vivem fora do repositório (organização/ambiente) | Responsabilidade distribuída entre biblioteca e operador | Adapters/perfis de consumidor são prioritários |

**Contribuição central que as duas rodadas sustentam, agora com evidência comparada:** *a governança como código precisa distinguir controles inerentes ao componente de software de controles que dependem do contexto operacional do consumidor.* A comparação controlada mostra o mesmo instrumento, sobre dois perfis diferentes, cobrando artefatos declarativos que em nenhum dos dois repositórios poderiam razoavelmente residir — em uma aplicação API, porque pertencem à organização e ao ambiente que a opera; em uma biblioteca de pipelines, porque pertencem a quem opera cada pipeline com a biblioteca. Em ambos os casos a suite registrou a ausência de forma explícita (achado P-04/P-07 ou pulo com motivo), sem colapso de estados — o comportamento é consistente com a observação registrada no relatório 07, §1.

**Critério pré-registrado para um eventual terceiro alvo (mantido):** só incluir outro repositório se ele responder a uma lacuna de cobertura conceitual não coberta pelas duas rodadas — hoje, os checks do pilar de ética e governança de IA (decisão automatizada, explicabilidade, decision log, supervisão humana, model cards, egresso para modelos). A justificativa formal: as duas rodadas avaliaram aplicabilidade em uma API e em um pipeline, ambas predominantemente Python, e os controles de ética/IA permaneceram não aplicáveis (guarda E-00: 14 checks nos dois alvos). O terceiro alvo seria um repositório público com uso explícito de IA, mediante pré-triagem de linguagem, porte, documentação e licença. A escolha nunca seria motivada por "precisar dar findings".

**Justificativa formal da terceira rodada (formulação registrada a partir do parecer da v3):** *"Os dois primeiros alvos permitiram avaliar privacidade, segurança, configuração e responsabilidade distribuída em código Python. Contudo, não permitiram avaliar adequadamente checks relacionados a IA, decisão automatizada, explicabilidade, trilha decisória, revisão humana, model card e egressos para LLM. Por isso, será realizada uma terceira rodada, previamente delimitada, em um repositório com uso explícito de IA."* O alvo de IA **não deve ser escolhido porque "parece ter mais falhas"**: deve ser escolhido porque permite avaliar o conjunto de controles que os alvos A e B não ativaram. Os oito critérios mínimos estabelecidos pelo parecer (uso explícito de IA; linguagem compatível, preferencialmente Python; escopo administrável; código e documentação suficientes; licença pública adequada; análise estática sem execução de API/modelo/serviço; pelo menos um fluxo observável de decisão, prompt, resposta, modelo, classificação, review ou audit log; commit ou tag congelável) foram **pré-registrados na matriz de pré-triagem** (`matrices/pre-triagem-alvo-c.md`) antes da enumeração de candidatos.

## 4. Regras de leitura (pré-registradas e aplicadas nesta comparação)

1. **Nunca concluir** que um repositório é "mais seguro" ou "mais conforme" que o outro — os laudos medem **aplicabilidade e comportamento da suite**, não conformidade dos alvos.
2. Comparar apenas: execução relativa por perfil, distribuição de estados (executado/pulado/não habilitado/indeterminado), taxa de achado por vetor, taxa de falso positivo após triagem humana, e esforço de adoção (preparação vs. execução).
3. Diferenças de perfil (API × pipeline) explicam a maior parte da variação de estados; tratá-las como resultado de aplicabilidade do corpus.
4. Qualquer número de severidade citado é do vocabulário interno da suite, sem equivalência legal estabelecida.
5. Ambas as rodadas compartilham a mesma declaração: ausência de achado ≠ ausência de risco; ausência de artefato PSE ≠ ausência de controle organizacional.

## 5. Ameaças à comparabilidade (declaradas)

1. **Rodada A é recuperação por re-execução, não o laudo histórico da rodada 1.** O commit congelado do alvo A (`9d4b774c`, tag `3.3.10`, 2026-07-07) é o estado do repositório na data da recuperação (2026-08-31), não o estado originalmente avaliado na rodada 1 (commit desconhecido neste ambiente). Quando os insumos originais forem localizados, esta execução deve ser reconciliada com eles; divergências são esperadas e devem ser documentadas como evolução do alvo, não como inconsistência do método.
2. **Alvos de porte e domínio diferentes.** API de aplicação (52 arquivos rastreados, 31 Python) × plugin de Airflow (43 Python + fixtures, Dockerfile, workflows). A diferença de porte é variável explicativa natural e não controlada — a comparação não isola o efeito de porte.
3. **Superfícies fora de alcance assimétricas.** O alvo B teve 2 arquivos fora de alcance (`.zip`, `.xcf`) e 4 arquivos sem extensão não declarados; o alvo A teve nenhum fora de alcance. A leitura de "cobertura de linguagem" deve considerar essa assimetria como atributo dos alvos.
4. **Um único ambiente.** Ambas as execuções ocorreram na mesma máquina, no mesmo venv e no mesmo dia; a paridade de instrumento é total aqui, mas a generalização para outros ambientes (Python, SO, dependências opcionais como Playwright) não é afirmada — a divergência ambiente×manifesto já documentada na rodada B (809/10 na configuração local descrita na proveniência vs. 798/8 no manifesto v0.20.0) mostra que o ambiente importa.
5. **A igualdade das partições é observação, não lei.** A partição idêntica (18/17/23) nos dois alvos é um resultado empírico desta comparação controlada com este catálogo congelado; não autoriza inferência de que qualquer alvo Python produzirá a mesma partição.
