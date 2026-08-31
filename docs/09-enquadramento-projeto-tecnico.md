# 09 — Enquadramento do TPF como Projeto Técnico

## Finalidade deste documento

Este documento organiza o enquadramento acadêmico e profissional do Trabalho Prático Final (TPF) na modalidade **Projeto Técnico**, para a Pós-Graduação em Arquitetura e Engenharia de Software da FIA Online.

O corpus técnico já registrado neste repositório — relatórios, matrizes, evidências, scripts e manifesto de proveniência — permanece como evidência histórica de uma avaliação exploratória, estática e somente leitura. Ele não é apresentado como auditoria, certificação, parecer jurídico, comprovação de conformidade ou teste de produção.

No TPF, esse corpus passa a exercer uma função específica: **demonstrar a viabilidade, os limites e os requisitos de implantação de um piloto da PSE Suite como prática de governança como código**.

## Problema

Em equipes de desenvolvimento de software, evidências relacionadas a controles selecionados de privacidade, segurança e ética por design podem estar distribuídas entre código-fonte, arquivos de configuração, pipelines de integração e entrega contínuas, manifestos, documentação e artefatos de modelos de IA. A obtenção e a revisão dessas evidências dependem frequentemente de atividades manuais, pouco padronizadas e difíceis de reproduzir entre versões do repositório.

Como exemplo, um repositório pode conter configuração de acesso a dados, dependências, variáveis de ambiente, documentação de pipeline ou artefatos de IA em locais distintos. A ausência de um artefato esperado pela ferramenta pode significar uma lacuna de evidência no repositório, uma característica arquitetural do componente ou um controle existente em outro ambiente. Logo, ela não permite concluir, isoladamente, que há falha técnica, violação legal ou desconformidade organizacional.

A questão que orienta este Projeto Técnico é:

> **Como estruturar e implantar, em um projeto-piloto de desenvolvimento de software, uma prática de governança como código capaz de gerar evidências técnicas rastreáveis sobre controles selecionados de privacidade, segurança e ética por design, respeitando os limites da análise estática de repositórios?**

## Objetivo

### Objetivo geral

Propor um projeto técnico de implantação piloto da PSE Suite como mecanismo de governança como código em repositórios de software, definindo a arquitetura de adoção, critérios de priorização, evidências técnicas, limites de uso, indicadores e roadmap de evolução.

### Objetivos específicos

1. Caracterizar a PSE Suite, seus modos de execução, mecanismos de proveniência e tipos de evidência produzidos.
2. Sistematizar as evidências de viabilidade e os limites identificados nas rodadas exploratórias sobre repositórios públicos com perfis arquiteturais distintos.
3. Mapear controles selecionados aos respectivos checks, evidências, limites de interpretação e recomendações de tratamento.
4. Definir um processo de integração da PSE Suite ao ciclo de desenvolvimento e à integração contínua.
5. Estabelecer critérios de triagem humana, priorização e tratamento dos achados.
6. Elaborar um plano-piloto com escopo, recursos, cronograma, riscos, indicadores e critérios de sucesso.
7. Propor um roadmap de evolução para cobertura técnica, integrações e governança operacional.

## Justificativa

A proposta é relevante para a prática profissional porque equipes de engenharia precisam tornar controles técnicos mais observáveis, repetíveis e rastreáveis no ciclo de desenvolvimento. Uma abordagem de governança como código pode apoiar a identificação de evidências em repositórios e a priorização de revisões humanas, desde que seus resultados sejam interpretados de acordo com o escopo, a versão da ferramenta e o contexto operacional.

A originalidade da proposta está em combinar checks versionados, proveniência de execução, laudos reproduzíveis, classificação explícita de estados e limites de interpretação. O objetivo não é substituir auditorias, avaliações jurídicas, testes dinâmicos, análises de arquitetura ou decisões de governança. A PSE Suite é proposta como mecanismo complementar para tornar a coleta e a discussão de evidências mais sistemáticas.

A viabilidade é sustentada pelo corpus técnico público deste repositório. Ele registra execuções estáticas em clones locais de repositórios públicos, commits congelados, matrizes de rastreabilidade, relatórios de validação e scripts de reprodução. Os resultados existentes oferecem subsídios para dimensionar aplicabilidade, ruído, falsos positivos, ausência de evidência, itens fora de alcance e necessidades de revisão humana antes de uma adoção em CI/CD.

## Delimitação

O Projeto Técnico limita-se ao planejamento de um piloto controlado em repositório de software. A proposta não contempla execução em produção, acesso a sistemas externos, acesso a bancos de dados, uso de credenciais reais, análise de dados pessoais reais, garantia de conformidade regulatória ou certificação de controles.

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
