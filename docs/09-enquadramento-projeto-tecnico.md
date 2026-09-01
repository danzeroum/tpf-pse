# 09 — Enquadramento do TPF como Projeto Técnico

## Apresentação da proposta

Em um projeto de software, decisões e controles relevantes para privacidade, segurança e ética por design deixam rastros em muitos lugares: código-fonte, configurações, dependências, pipelines de integração e entrega contínuas, manifestos e documentação. Esses artefatos são parte do trabalho cotidiano de engenharia, mas nem sempre são fáceis de localizar, relacionar e revisar de forma consistente à medida que o repositório evolui.

Essa dispersão cria um problema prático. Quando uma equipe precisa compreender o que já está documentado, quais controles possuem evidência técnica e quais pontos ainda dependem de investigação, a resposta pode ficar distribuída entre pessoas, diretórios, ferramentas e versões diferentes do projeto. O resultado não é necessariamente a ausência de controles; frequentemente é a ausência de um processo reproduzível para encontrar, registrar e discutir as evidências disponíveis.

A PSE Suite é proposta neste TPF como uma ferramenta de apoio a esse processo. Por meio de checks versionados e de laudos rastreáveis, ela busca tornar mais sistemática a observação de artefatos selecionados de privacidade, segurança e ética por design. A ferramenta não substitui auditorias, avaliações jurídicas, testes dinâmicos, análise de arquitetura ou decisões humanas de governança. Seu papel é oferecer uma primeira camada técnica de observação e organizar insumos para revisão humana.

O corpus já registrado neste repositório — relatórios, matrizes, evidências, scripts e manifesto de proveniência — preserva uma avaliação exploratória, estática e somente leitura. No contexto deste TPF, ele é utilizado como evidência de viabilidade e de limites para a implantação de um piloto controlado de governança como código.

## Problema

Em equipes de desenvolvimento de software, evidências relacionadas a controles selecionados de privacidade, segurança e ética por design podem estar distribuídas entre código-fonte, arquivos de configuração, pipelines de CI/CD, manifestos, documentação e artefatos de modelos de IA. A identificação e a revisão dessas evidências tendem a depender de atividades manuais, pouco padronizadas e difíceis de reproduzir entre versões de um repositório.

Por exemplo, um repositório pode conter variáveis de ambiente, dependências, configurações de acesso a dados, documentação de pipeline ou artefatos de IA em diretórios e formatos distintos. Sem uma prática estruturada de observação, cada revisão pode exigir uma nova busca, novas interpretações e trocas de contexto entre profissionais.

A ausência de um artefato esperado em uma análise estática pode ter interpretações distintas: pode indicar uma lacuna de evidência no repositório, refletir uma característica arquitetural do componente ou significar que o controle está documentado e operado fora do escopo analisado.

Por isso, a ausência de evidência, isoladamente, não permite concluir que exista falha técnica, violação legal ou desconformidade organizacional. Uma prática de governança como código precisa explicitar tanto as evidências encontradas quanto os limites do que conseguiu observar.

Diante desse contexto, o problema a ser estudado é:

> **Como estruturar e implantar, em um projeto-piloto de desenvolvimento de software, uma prática de governança como código capaz de gerar evidências técnicas rastreáveis sobre controles selecionados de privacidade, segurança e ética por design, respeitando os limites da análise estática de repositórios?**

## Objetivo

### Objetivo geral

Propor um projeto técnico de implantação piloto da PSE Suite como mecanismo de governança como código em repositórios de software, definindo arquitetura de adoção, critérios de priorização, evidências técnicas, limites de uso, indicadores e roadmap de evolução.

Para alcançar esse objetivo, o trabalho se desdobra em sete etapas: da caracterização da ferramenta e do estudo de sua viabilidade técnica à elaboração de um plano-piloto operacionalizável.

### Objetivos específicos

1. Caracterizar a PSE Suite, seus modos de execução, mecanismos de proveniência e tipos de evidência produzidos.
2. Sistematizar as evidências de viabilidade e os limites identificados em avaliações exploratórias sobre repositórios públicos com perfis arquiteturais distintos.
3. Mapear controles selecionados aos respectivos checks, evidências, limites de interpretação e recomendações de tratamento.
4. Definir um processo de integração da PSE Suite ao ciclo de desenvolvimento e à integração contínua.
5. Estabelecer critérios de triagem humana, priorização e tratamento dos achados.
6. Elaborar um plano-piloto com escopo, recursos, cronograma, riscos, indicadores e critérios de sucesso.
7. Propor um roadmap de evolução para cobertura técnica, integrações e governança operacional.

## Justificativa

### Relevância profissional

Equipes de engenharia precisam revisar continuamente artefatos que influenciam privacidade, segurança e governança de sistemas. Quando as evidências técnicas estão dispersas, parte desse trabalho depende de buscas manuais, conhecimento tácito e verificações que podem variar entre pessoas e versões do software. A governança como código é proposta como uma forma de apoiar a identificação estruturada dessas evidências e de tornar a discussão técnica mais rastreável e repetível.

### Viabilidade técnica

A proposta não parte apenas de uma hipótese conceitual. Este repositório reúne um corpus técnico público com relatórios, matrizes de rastreabilidade, scripts de reprodução, evidências de execução e manifesto de integridade. As avaliações exploratórias realizadas em clones locais de repositórios públicos e commits congelados permitem identificar aspectos de aplicabilidade, limites de cobertura, ruído, possíveis falsos positivos, ausência de evidência e dependência de contexto. Esses elementos reduzem incertezas para o planejamento de um piloto controlado.

### Aderência ao Projeto Técnico

A proposta é adequada à modalidade Projeto Técnico porque detalha uma intervenção aplicável: seleção de escopo, arquitetura operacional, integração ao ciclo de desenvolvimento, responsabilidades, critérios de triagem, indicadores, monitoramento, riscos e roadmap. O foco do trabalho não é afirmar que a PSE Suite resolve integralmente problemas de privacidade, segurança ou ética. O foco é propor uma forma realista, mensurável e progressiva de utilizá-la como apoio à governança técnica em um projeto-piloto.

## Delimitação

O Projeto Técnico limita-se ao planejamento de um piloto controlado em repositório de software. A proposta não contempla execução em produção, acesso a sistemas externos, bancos de dados, credenciais reais ou dados pessoais reais. Também não representa garantia de conformidade regulatória, certificação de controles ou substituição de processos especializados de segurança, privacidade, jurídico e gestão de riscos.

A análise estática pode localizar indícios e evidências presentes nos artefatos versionados, mas não observa, por si só, comportamento em tempo de execução, configuração de infraestrutura externa, práticas operacionais não registradas no repositório, efetividade organizacional de controles ou contexto de uso pelo consumidor de uma biblioteca.

## Uso do corpus técnico

Os documentos existentes devem ser lidos como **diagnóstico de viabilidade**, e não como a entrega final do Projeto Técnico. Eles subsidiam a proposta nos seguintes aspectos:

| Evidência do corpus | Uso no Projeto Técnico |
|---|---|
| Proveniência por SHA, versão e `catalog_hash` | Requisito de rastreabilidade do piloto |
| Execuções em perfis arquiteturais distintos | Evidência de aplicabilidade condicionada ao tipo de repositório |
| Achados validados, ausências de evidência e falsos positivos | Base para fluxo de triagem e revisão humana |
| Checks não aplicáveis ou fora de alcance | Delimitação de cobertura e gestão de expectativas |
| Mutações controladas | Evidência de que regras selecionadas detectam vetores plantados |
| Matrizes requisito → check → evidência → limite | Instrumento de governança e monitoramento do piloto |

## Estrutura recomendada para o TPF

1. Introdução: contexto, problema, objetivo, justificativa e delimitação.
2. Referencial teórico: governança como código, DevSecOps, privacidade, segurança e governança de IA.
3. Diagnóstico e evidências de viabilidade: síntese do corpus técnico existente.
4. Proposta de solução: arquitetura, processo operacional, papéis, critérios de priorização e integração ao CI/CD.
5. Plano piloto: cronograma, recursos, riscos, indicadores, monitoramento, avaliação e sustentabilidade.
6. Conclusão e limitações.

## Declaração de interpretação

Achados e ausências de evidência identificados pela PSE Suite devem ser tratados como insumos técnicos para investigação e priorização. Eles não constituem, isoladamente, afirmação de vulnerabilidade, falha, violação legal, desconformidade ou inadequação de qualquer repositório, organização, mantenedor ou produto analisado.
