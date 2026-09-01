# Proposta Inicial do TPF — PSE Suite

## Modalidade

**Projeto Técnico** — Pós-Graduação em Arquitetura e Engenharia de Software, FIA Online.

Este arquivo contém o texto acadêmico da entrega inicial. Dados cadastrais e o arquivo DOCX de submissão permanecem fora do repositório público.

## Problema a ser estudado

Em projetos de software, decisões e controles relacionados à privacidade, à segurança e à ética por design deixam rastros distribuídos pelo ciclo de desenvolvimento: no código-fonte, em arquivos de configuração, dependências, pipelines de integração e entrega contínuas, manifestos de infraestrutura, documentação técnica e registros de execução.

À medida que o repositório evolui, localizar, relacionar e revisar essas evidências de forma consistente se torna uma tarefa complexa. Informações importantes podem estar fragmentadas entre diretórios, ferramentas, pessoas responsáveis e versões distintas do software. O problema não é necessariamente a inexistência de controles, mas a dificuldade de encontrar, registrar, conectar e discutir as evidências disponíveis de maneira reproduzível.

Por exemplo, um repositório pode utilizar variáveis de ambiente, bibliotecas externas, permissões de acesso a dados, documentação de pipelines e artefatos de infraestrutura como código. Esses elementos podem conter sinais relevantes para a análise de privacidade, segurança ou ética por design, mas estar organizados em formatos e diretórios diferentes ou ser operados fora do recorte analisado.

A ausência de um artefato esperado em uma análise estática pode indicar uma lacuna de evidência no repositório, uma característica arquitetural do componente analisado ou a existência de controles documentados e operados em outro contexto. Por essa razão, não deve ser interpretada isoladamente como falha técnica, violação legal ou desconformidade organizacional.

Diante desse cenário, o problema deste Projeto Técnico é: **como estruturar e implantar, em um projeto-piloto de desenvolvimento de software, uma prática de governança como código capaz de gerar evidências técnicas rastreáveis sobre controles selecionados de privacidade, segurança e ética por design, respeitando os limites inerentes à análise estática de repositórios?**

## Objetivo a ser alcançado

### Objetivo geral

Propor um projeto técnico para a implantação piloto da PSE Suite como mecanismo de governança como código em repositórios de software, definindo sua arquitetura de adoção, critérios de priorização, evidências técnicas, limites de uso, indicadores de acompanhamento e roadmap de evolução.

A adoção de governança como código não se resume à execução de uma ferramenta. Ela exige definir quais repositórios serão analisados, quais controles serão priorizados, quais evidências serão aceitas, como os resultados serão interpretados, quem responderá pela triagem dos achados e como a prática poderá evoluir após o piloto.

### Objetivos específicos

1. Caracterizar a PSE Suite, seus modos de execução, mecanismos de proveniência e tipos de evidência técnica produzidos.
2. Sistematizar evidências de viabilidade, limites de cobertura e pontos de atenção identificados em avaliações exploratórias sobre repositórios públicos com perfis arquiteturais distintos.
3. Mapear controles selecionados de privacidade, segurança e ética por design aos respectivos checks, evidências, limites de interpretação e recomendações de tratamento.
4. Definir um processo de integração da PSE Suite ao ciclo de desenvolvimento e às práticas de integração contínua.
5. Estabelecer critérios para triagem humana, priorização e tratamento dos achados.
6. Elaborar um plano-piloto com escopo, recursos, cronograma, responsabilidades, riscos, indicadores e critérios de sucesso.
7. Propor um roadmap de evolução para ampliar gradualmente a cobertura técnica, fortalecer integrações e consolidar uma prática de governança operacional baseada em evidências.

## Justificativa

### Relevância profissional

No cotidiano das equipes de engenharia, configurações, dependências, regras de pipeline, documentos, manifestos e código-fonte registram escolhas que afetam privacidade, segurança e governança. Quando essas evidências permanecem dispersas, a equipe depende de buscas manuais, memória institucional e interpretações que variam entre pessoas e versões. A governança como código busca apoiar uma identificação estruturada de evidências e tornar a discussão técnica mais rastreável, repetível e verificável.

### Viabilidade técnica

A proposta é sustentada por corpus técnico público já produzido, composto por relatórios, matrizes de rastreabilidade, scripts de reprodução, evidências de execução e manifestos de integridade. Avaliações exploratórias em clones locais de repositórios públicos e commits congelados permitem observar aplicabilidade, cobertura, limites de interpretação, dependência de contexto e possíveis falsos positivos. Esses insumos permitem delimitar o escopo, mapear riscos e elaborar um piloto controlado com critérios claros de execução e avaliação.

### Aderência ao Projeto Técnico

A proposta se enquadra como Projeto Técnico porque propõe desenhar e estruturar uma intervenção aplicável: a implantação piloto da PSE Suite como mecanismo de governança como código. A intervenção envolve escopo, arquitetura operacional, integração ao ciclo de desenvolvimento, responsabilidades, triagem humana, indicadores, monitoramento, riscos e roadmap. O resultado esperado é um plano realista, mensurável e progressivo para produzir, interpretar, registrar e tratar evidências técnicas, preservando a análise humana e os limites da automação.

## Delimitação

O trabalho não é auditoria, certificação, parecer jurídico, teste de produção ou garantia de conformidade. A análise estática pode localizar evidências e indícios em artefatos versionados, mas não avalia isoladamente comportamento em execução, infraestrutura externa, práticas operacionais não registradas ou efetividade organizacional de controles.

## Relação com o corpus

Os relatórios, matrizes, evidências e scripts deste repositório são utilizados como diagnóstico de viabilidade para a proposta de implantação piloto. Eles não constituem, isoladamente, afirmação de vulnerabilidade, falha, violação legal ou desconformidade de qualquer repositório ou organização analisada.
