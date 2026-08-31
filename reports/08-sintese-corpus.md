# 08 — Síntese do corpus: três rodadas externas sob a mesma instrumentação (API × pipeline × IA)

## 1. Escopo desta síntese

Este relatório consolida as **três rodadas externas** do estudo — A (API PGD, `gestaogovbr/api-pgd` @ `9d4b774c`, recuperação por re-execução local), B (FastETL, `gestaogovbr/FastETL` @ `9fb5d596`) e C (LlamaFactory, `hiyouga/LlamaFactory` @ `d6bb97d`, alvo de IA) — executadas com a **mesma instrumentação congelada**: mesmo clone da PSE Suite (v0.20.0 @ `443da92`), mesmo `catalog_hash 4682a4ae…a0ac`, mesmo schema de laudo (`laudo-pse-1.0`), mesmo modo (`pse_inventory`), mesmo venv (Python 3.12.14), mesmo SO, mesmas categorias de classificação humana e mesmas regras de sanitização. A síntese compara **aplicabilidade, comportamento e limites da suite** entre perfis arquiteturais — nunca segurança, privacidade ou conformidade dos alvos (regras de leitura do relatório 05, §4, aplicadas a todo o corpus).

## 2. Paridade de proveniência nas três rodadas

| Fator | Rodada A (recuperada) | Rodada B | Rodada C |
|---|---|---|---|
| Versão / commit da PSE Suite | 0.20.0 / `443da92` | idem | idem |
| `catalog_hash` | `4682a4ae…a0ac` | idem | idem |
| `schema_version` | `laudo-pse-1.0` | idem | idem |
| Modo de execução | `pse_inventory` | idem | idem |
| Python / SO | 3.12.14 / Debian 13 | idem | idem |
| Critérios de classificação humana | 3 categorias + dúvida preservada | idem | idem |
| Regras de sanitização | hosts `[REDACTED-HOST]`, credencial redigida, varredura global | idem | idem |
| Formato de laudo | JSON `laudo-pse-1.0` + sanitizado + resumo | idem | idem |
| Commit do alvo (congelado) | `9d4b774c` (tag `3.3.10`) | `9fb5d596` | `d6bb97d` (`main`, 2026-08-31) |
| Perfil arquitetural | API Python (FastAPI/SQLAlchemy/Pydantic, AGPLv3) | biblioteca/pipeline Airflow (GPLv3, divergência no setup.py) | framework de fine-tuning de LLMs (Apache-2.0) |

Paridade total de instrumento nas três rodadas; as diferenças restantes são atributos dos alvos (perfil, porte, domínio, licença) e funcionam como variáveis explicativas — jamais como ranking.

## 3. Resultado central: a partição do catálogo se move com o perfil

| Categoria (regra 07 §10.1) | A — API | B — pipeline | C — IA/treino |
|---|---|---|---|
| Executados | 18 | 18 | **25** |
| Não aplicáveis (vetor estrutural/guarda) | 17 (14 E-00 + 3 vetor) | 17 (14 E-00 + 3 vetor) | **2** (E-12, P-19) |
| Dependentes de contexto | 23 (8 declarativo + 15 Trabalho A) | 23 (8 declarativo + 15 Trabalho A) | **29** (10 declarativo + 19 Trabalho A) |
| Indeterminados (estado próprio) | 0 | 0 | **2** (E-06, P-15) |
| **Partição** | 18+17+23 = 58 ✔ | 18+17+23 = 58 ✔ | **25+2+29+2 = 58** ✔ |

**Leitura permitida e defensável:**

1. A igualdade das partições em A e B **não prova que API PGD e FastETL tenham o mesmo nível de governança, segurança ou privacidade** — mostra que, sob o modo estático e o perfil atual da suite, os dois repositórios apresentam estruturas de aplicabilidade semelhantes (predominantemente Python, sem IA exposta no clone, sem os artefatos declarativos que vários checks exigem).
2. O deslocamento da partição em C **confirma a hipótese da interação catálogo×perfil** (relatório 05, §2.1): um perfil com IA em código efetivo abre a guarda E-00 e move os 14 checks de ética (e os 2 vetores de treino) de "não aplicável" para execução ou indeterminação — sem que nada na suite tenha sido alterado.
3. As diferenças entre rodadas estão no **conteúdo** (quais checks emitiram findings e sobre que superfícies), não na honestidade dos estados: nas três rodadas nenhum pulo foi silencioso e nenhum estado foi colapsado.

Indicadores por rodada (formulação segura — a fração mede aplicabilidade do catálogo no recorte estático; não mede cobertura universal de privacidade, segurança, ética, código ou requisitos legais):

| Indicador | A | B | C |
|---|---|---|---|
| Cobertura bruta | 18/58 | 18/58 | 25/58 |
| Executados ÷ potencialmente aplicáveis | 18/29 | 18/29 | 25/39 |
| Findings | 4 (4 ALTO) | 8 (6 ALTO, 2 MÉDIO) | 21 (18 ALTO, 3 MÉDIO) |
| Possíveis falsos positivos (triagem) | 2/4 | 3/8 | 12/21 |
| Exit code | 11 | 11 | **20 (indeterminado)** |
| Duração | 2,4 s | 2,0 s | 31,62 s |

## 4. O que as três rodadas demonstram (achados técnicos do corpus)

### 4.1 O modo estático é viável e escala com custo previsível

A PSE Suite executou inventário estático sobre três perfis públicos externos, sem rede, sem credenciais e sem alterar clones, em 2,0–31,62 s (a duração cresce com o porte lido: 38 → 57 → 449 arquivos). A assimetria preparação×execução — identificada na rodada B — mantém-se: o custo está na preparação (clone, venv, estudo de contratos, congelamento), não na execução, o que favorece adoção como etapa de CI.

### 4.2 Governança como código depende de contexto operacional e de artefatos declarativos

Nos três perfis, o padrão dominante foi a cobrança de artefatos declarativos (catálogo, consent, manifesto de terceiros, residência, finalidade, OpenAPI) que não residem no clone: em A pertencem à organização que opera a API; em B, a quem opera cada pipeline com a biblioteca; em C, ao operador do treino e ao publicador do modelo. O par P-04/P-07 reproduziu-se nos três alvos com a mesma semântica de ausência local — e a classificação humana manteve `ausencia-de-evidencia-pse` em todos, sem concluir sobre controles fora do repositório. A tese de distribuição de responsabilidades (componente × operador × organização) é agora sustentada por três perfis arquiteturais distintos.

### 4.3 A PSE revela os próprios limites — inclusive bloqueando

O corpus documenta três formas de "recusa honesta" da suite: (i) pulo com motivo computado (dominante em A/B/C); (ii) não habilitado declarado (Trabalho A sem alvo); e (iii) — inédito do alvo C — **indeterminado com veredito global bloqueante (exit 20)**: E-06 e P-15 tinham metade do indício (treino, fairness) sem a outra metade do substrato (dataset declarado, catálogo), e a suite preferiu não decidir a decidir mal. No escopo e nas versões avaliados, não foi observado colapso de estados em conclusão global de conformidade em nenhuma das rodadas.

### 4.4 O pilar de ética/IA passou de fora de escopo a exercido — com insumos de calibração

Em A e B, a guarda E-00 classificou os 14 checks de ética como fora de escopo (motivo computado, não silencioso). Em C, com IA em código efetivo, o pack entrou em escopo **por fato computado** (sem declaração do alvo, sem adaptação da suite): E-00/E-04/E-05/E-11 executaram limpos; E-07 emitiu ALTO (sem model card versionado no clone — mesma forma declarativa de P-04/P-07); E-10 emitiu 3 MÉDIO (rotinas de treino sem incerteza quantificada — triagem preliminar: possivel-falso-positivo, pois "decisão" em um framework de treino não é decisão sobre pessoas); E-06 ficou indeterminado (fairness sem dataset). Resultado duplo: o corpus agora **exercita** o pilar que antes não avaliava, e a rodada produziu os insumos de calibração mais específicos das três rodadas (qualificação de contexto de decisão, extração de nomes de dataset em P-16, distinção runtime × CI em S-04).

### 4.5 Superfícies de egresso variam por perfil — e a leitura exige contexto

S-04 ilustrou três regimes: integrações operacionais em código (B), superfícies de documentação/exemplo (A) e, em C, um mix de egresso real de **CI** (6 confirmados-no-escopo) e strings de UI/exemplo/metadado (6 possíveis falsos positivos). A mesma regra, sobre perfis diferentes, exige inspeção humana com contexto — reforçando que o valor da suite está no registro rastreável de superfícies, não em veredito automático.

## 5. Interpretação correta do conjunto (para citação no TPF)

A conclusão defensável do corpus é:

> "Nos três repositórios Python avaliados, a PSE Suite apresentou comportamento estrutural coerente com o perfil de cada alvo no modo estático: 18 checks executados nos alvos sem IA (com 17 não aplicáveis e 23 dependentes de contexto em ambos) e 25 checks executados no alvo com IA (com 2 não aplicáveis, 29 dependentes de contexto e 2 indeterminados). Essas distribuições decorrem, em parte, do perfil dos alvos e da configuração da suite, e não devem ser interpretadas como medida de maturidade de segurança, privacidade ou conformidade dos projetos."

Os checks não executados podem depender de: catálogo de dados no formato esperado pela PSE; modelo de consentimento; manifesto de integrações de terceiros; informações de residência de dados; especificação OpenAPI estática; artefatos de IA/ML, model card, decisões automatizadas ou dataset de treinamento; e configuração operacional que não existe no clone público. A própria documentação da suite reconhece que pulado, indeterminado, não habilitado e fora de alcance não devem ser interpretados como conformidade.

## 6. Limitações e ameaças (acumulado do corpus)

1. **Rodada A é recuperação por re-execução** (relatório 05, §5) — não o laudo histórico original.
2. **Portes assimétricos** (31/43/311 arquivos Python; 2,4/2,0/31,62 s) — variável explicativa não isolada.
3. **Um único ambiente** (mesma máquina, venv, dia) — generalização para outros ambientes não é afirmada; a divergência ambiente×manifesto (809/10 local × 798/8 manifesto v0.20.0) permanece registrada.
4. **Uma regra de partição com extensões declaradas** — a partição do alvo C usa a mesma regra de A/B com duas extensões codificadas a priori (estado indeterminado próprio; forma de motivo do E-12). As extensões estão documentadas em `scripts/14_analise_alvo_c.py` e não alteram os números de A/B.
5. **Triagem humana é preliminar e de um único avaliador** — as classificações (12 possíveis falsos positivos em C, por exemplo) são insumo de calibração, não veredito; a dúvida permanece visível em todos os casos.
6. **Seletividade do corpus** — três perfis Python escolhidos por lacuna conceitual e viabilidade estática; nenhum alvo com IA **aplicada a decisões sobre pessoas** (crédito, saúde, recursos humanos) integrou o corpus: os checks de ética exercidos em C operaram sobre substrato de framework de treino, e a leitura sobre "decisão sobre pessoas" permanece como limite declarado.
7. **Sem adaptação do alvo** — nenhum `pse-config.yaml` foi criado; os indicadores medem a suite **sem** configuração, que é o cenário de primeira adoção, não o de maturidade.

## 7. Contribuição para a tese (TPF)

O corpus sustenta, com evidência rastreável em três perfis arquiteturais:

> **A governança como código pode produzir evidência técnica rastreável em diferentes tipos de repositórios, mas sua aplicabilidade depende da arquitetura, do suporte de linguagem, da disponibilidade de artefatos declarativos e da divisão de responsabilidades entre componente, operador e organização.**

Contribuições específicas das rodadas para a tese: a partição do catálogo como assinatura da interação catálogo×perfil (§3); a taxonomia completa de estados não-colapsados, incluindo o bloqueio por indeterminação (§4.3); a abertura de guarda de escopo por fato computado como mecanismo de honestidade declarativa (§4.4); e a fronteira componente×operador×organização observada de forma independente nos três perfis (§4.2).

---

**Declaração final obrigatória:** Esta síntese cobre avaliações estáticas, somente leitura, sobre clones locais de código público, limitadas aos commits e artefatos observados. Seus resultados não constituem auditoria institucional, certificação de segurança, parecer jurídico de conformidade, teste em produção ou comprovação de ausência de riscos — de nenhum dos três alvos.
