# Worklog — TPF PSE Suite × FastETL

---
Task ID: 1-15 (run completa)
Agent: Super Z (agente principal)
Task: Avaliação exploratória, estática e somente leitura da PSE Suite sobre o FastETL (rodada 2 do TPF FIA Online), conforme runbook de 12 fases do usuário.

Work Log:
- Fase 1: clonados os 3 repositórios públicos (danzeroum/pse-suite @ 443da92dbdb22a9af18aa6eebb51aac2da901458, danzeroum/project @ 991e2d0f28d746e40a80c89280bdd9060f5a0311, gestaogovbr/FastETL @ 9fb5d596cd8c3d4d0efcf6cdd1ca0c7b5e24afc1), histórico completo + proveniência congelada (scripts/00_provenance.py → evidence/provenance/00-provenance.json + reports/00-provenance.md).
- Fase 2: lidos README, pyproject, MANIFESTO-v0.20.0, COMO-ADOTAR, TESTES, INDICE-DE-TESTES, matriz-dominio, BURACOS-ASSUMIDOS, RATIFICACOES, cobertura-btv, ci.yml, checks-catalog.yaml, limites.py, cli.py, E-00; suite instalada em venv isolado (.venv-pse); pse --manifesto (exit 0, catalog_hash 4682a4ae…a0ac), pse --self-test (exit 0, 58 mutações), pytest (809 pass / 10 skip / 157,78 s; pulos: 8 Playwright ausente, 2 aceite btv pendente).
- Fase 3: lidos README, CLAUDE, project.yaml, ripd.md, assurance-evidence.md, evidence-bundle README, ADR-032, data-inventory/ledger schemas, test_assurance_evidence_contract.py; princípios registrados como subseção do relatório 01.
- Fase 4: caracterização factual do FastETL (43 .py, ~8.007 linhas; GPLv3 vs license Apache no setup.py registrada de forma neutra; inventário por extensão/diretório; mapa de compatibilidade) → reports/02-caracterizacao-fastenl.md (nome obrigatório "fastenl" respeitado).
- Fase 5: pré-triagem hipotética por pilar/check/artefato → matrices/cobertura-por-artefato.md.
- Fase 6: pse --path repos/FastETL --modo pse_inventory → exit 11, 2,07 s, 18 executados/25 pulados/15 não habilitados/0 indeterminados/8 findings (6 ALTO, 2 MÉDIO); laudo bruto em evidence/raw (sha256 09eea0fd…); sanitização via scripts/06_sanitizar.py (credencial → [REDACTED], hosts mascarados em evidência, varredura global) → evidence/sanitized (sha256 00caaa08…); relatório 03.
- Fase 7: validação manual dos 8 achados (3 confirmado-no-escopo, 2 ausencia-de-evidencia-pse, 3 possivel-falso-positivo) → reports/04.
- Fase 8: 8 mutações em cópias descartáveis (scripts/08_mutacoes.py; clones intactos verificados): M1 P-01 CRÍTICO detectado; M2 S-06 CRÍTICO; M3 S-04 sobre host sintético; M4 P-04 cessou + P-02 mordeu, P-18 não disparou (mutação plantou personal, vetor é sensitive — erro de experimento documentado); M5 P-20 ALTO; M6 declaração automated reabre ethics e E-06 vira indeterminado → exit 20; M7a trava não morde após rodapé volátil (comportamento documentado); M7b trava morde no corpo (exit 1); M8 fora_de_alcance 2→3 → matrices/mutacoes-e-resultados.md.
- Fase 9: matriz central com 58 checks e separação exigida (verificado/encontrado/não-verificável/não-aplicável/contexto organizacional/evolução) → matrices/requisito-check-evidencia-limite.md.
- Fase 10: insumos da rodada API PGD indisponíveis localmente → relatório 05 registra a indisponibilidade, pré-preenche o lado FastETL e pré-registra regras de leitura não acusatórias.
- Fase 11: plano de piloto hipotético → reports/06.
- Fase 12: relatório final → reports/07-relatorio-final-rodada-fastenl.md (15 seções + declaração final obrigatória).
- Fechamento: README.md de reprodução segura; scripts/99_fechamento.py completou proveniência (suite, comandos com exit/duração, 16 hashes SHA-256); verificação final: git status vazio nos 3 clones, [REDACTED] presente no sanitizado, nenhum literal proibido.

Stage Summary:
- 16 artefatos entregues sob /home/z/my-project/tpf-pse-fastetl/ (8 relatórios, 3 matrizes, proveniência JSON+MD, laudo sanitizado, resumo executivo, README).
- Execução-alvo: exit 11; estados 18/25/15/0/0; findings 8 (privacy 4, security 4, ethics 0 fora de escopo computado); 2,07 s.
- Mutações: 7 detecções exatas, 1 parcial analisada, 2 descobertas de comportamento (superfície declarativa ativa família de checks; declaração sem insumo → exit 20 fail-closed).
- Restrições éticas cumpridas: só clones + pip autorizado; sem rede/serviços/credenciais; sanitização integral; nenhum veredito sobre o alvo; linguagem controlada nos 8 relatórios.

---
Task ID: 16 (revisão v2 pós-parecer)
Agent: Super Z (agente principal)
Task: Aplicar as correções do parecer da orientação sobre a rodada FastETL (nomenclatura, formulações de achados, métricas de cobertura, frase de escopo, consolidação metodológica).

Work Log:
- Nomenclatura: anexos renomeados para nomes neutros estáveis (alvo-b): 02-caracterizacao-alvo-b.md, 03-execucao-alvo-b.md, 05-comparacao-api-pgd-alvo-b.md, 07-relatorio-final-alvo-b.md, laudo-alvo-b-bruto.json, laudo-alvo-b-sanitizado.json; grafia in-text já correta (FastETL) verificada — zero ocorrências de "fastenl" no corpus.
- Re-execução determinística do pse_inventory com o nome corrigido (mesmo commit 9fb5d596, suite 0.20.0, catalog_hash 4682a4ae): exit 11, 2,0 s, findings/estados/cobertura idênticos (diff confirma só timestamp/duração); sanitização refeita (sha256 bruto 7201c25c…, sanitizado 4942afe8…); comando-inventory.txt atualizado; arquivos antigos removidos.
- Métricas: "31%" isolado substituído por 4 indicadores calculados do laudo (scripts/10_analise_revisao.py): bruta 18/58; aplicáveis 18/29 (62%); não aplicáveis 17; dependentes de contexto 23. Correções aritméticas expostas pelo refinamento: com achado 6→4 checks distintos (sem achado 12→14, incl. P-09); ética fora de escopo 11→14 checks (E-00 a E-13) no relatório 03, resumo e matriz central.
- Formulações: P-04/P-07/S-04/P-06 reescritos com as formulações recomendadas (não localizado no clone; inspeção manual deve classificar; valor não divulgado) em 03 (§3 + parágrafo de formulação responsável), resumo sanitizado, 04 e 07; "nunca emite verde silencioso" substituída pela frase com escopo no 07 (§1).
- Consolidação: relatório 05 ganhou §3 (tabela metodológica API PGD × FastETL do parecer, contribuição central e critério pré-registrado para terceiro alvo com IA); 07 adotou o título rigoroso recomendado e passou a referenciar a consolidação; 06 atualizado (18/58 e 18/29; 2,0 s).
- Proveniência v2: scripts 06/99/10 atualizados; 99_fechamento.py re-registrado (nota de revisão, duração 2,0 s, novos nomes) e re-executado (16 hashes); nota sobre hash autoreferente do 00-provenance.md.
- Verificação final: zero "fastenl"/paths antigos; "31%" só como menção-meta explicando o que não fazer; clones intactos (git status vazio nos 3).

Stage Summary:
- Corpus integralmente aderente ao parecer; evidência congelada v2 com re-execução determinística documentada.
- Números canônicos da rodada: exit 11 · 18/58 bruta · 18/29 aplicáveis · 25 pulados · 15 não habilitados · 0 indeterminados · 8 findings (6 ALTO, 2 MÉDIO) · 2,0 s · 7/8 mutações com detecção.

---
Task ID: 17 (revisão v3 — atenções finais do parecer + recuperação da rodada A)
Agent: Super Z (agente principal)
Task: Aplicar os três cuidados finais do parecer (definição formal dos 4 indicadores com declaração de exclusividade mútua; precisão das contagens de testes/mutações; recuperação da rodada API PGD) e preencher a comparação A × B.

Work Log:
- Atenção 1: nota metodológica formal criada no relatório 07 (§10.1) — fórmulas dos 4 indicadores, regra de classificação com precedência declarada 1→4 e declaração explícita de exclusividade mútua; regra codificada em scripts/10 (alvo B) e scripts/11 (alvo A) e verificada por asserção de partição: 18+17+23=58 nos DOIS alvos. Auditoria da v2: o filtro de tokens do script 10 duplicava os pulos de ética no conjunto "declarativo" (motivo E-00 contém "decision_making"; motivo P-15 contém "catalogo"), mas os números publicados (17/23) eram a partição correta e permanecem inalterados; script corrigido para reproduzir os números publicados.
- Atenção 2: contagens qualificadas em todo o corpus — frase exata do parecer no 07 §1 ("Na configuração local descrita na proveniência, a execução da suíte retornou 809 testes aprovados e 10 pulados, sem falhas."); 58 mutações vinculadas ao catálogo congelado (07 §1, 01); nota de que contagens estão associadas ao commit/catálogo/ambiente congelados, não propriedade permanente do produto (07 §6, 01). Registros de proveniência (00-provenance.json/md) e logs brutos mantidos intactos — são evidência observada, não narrativa.
- Atenção 3: rodada A recuperada por re-execução local — insumos originais inexistem neste ambiente (varredura exaustiva de /home/z confirmou); repo identificado via API de busca (gestaogovbr/api-pgd, mesmo org do FastETL), clonado e congelado (9d4b774cc6763b234372999a1d1c4baf248e3080, tag 3.3.10, 1.396 commits, FastAPI 0.111/SQLAlchemy 2.0.31/Pydantic 2.8.2, AGPLv3, 31 .py); emenda de protocolo declarada (quarto clone) no 03-execucao-alvo-a, 05 §1, README e proveniência. Execução pse_inventory com a MESMA instrumentação congelada da rodada B: exit 11, 2,4 s, estados 18/25/15/0, 4 findings (P-04, P-07, S-04×2 — todos ALTO; P-06 limpo; S-04 sobre superfícies de documentação/exemplo), partição 18+17+23=58 idêntica à rodada B.
- Artefatos novos da rodada A: reports/02-caracterizacao-alvo-a.md; reports/03-execucao-alvo-a.md (triagem humana: 2 ausencia-de-evidencia-pse, 2 possivel-falso-positivo, dúvida preservada); matrices/estados-por-check-alvo-a.md (58 checks gerada por script); evidence/raw/laudo-alvo-a-bruto.json (sha256 9242263a…) + comando-inventory-alvo-a.txt; evidence/sanitized/laudo-alvo-a-sanitizado.json (sha256 dc7850c7…, hosts mascarados [REDACTED-HOST], regras idênticas à rodada B via scripts/12) + resumo-executivo-laudo-alvo-a.md.
- Comparação A × B executada no relatório 05 (reescrito integralmente): quadro de métricas preenchido com dados dos dois laudos; partição lado a lado (§2.1); tabela de paridade de proveniência com os 10 fatores exigidos pelo parecer (§2.5 — todos idênticos, paridade total); consolidação metodológica agora sustentada por evidência comparada (§3); regras de leitura mantidas (§4); 5 ameaças à comparabilidade declaradas (§5, em especial: rodada A é recuperação sobre o estado atual do alvo, não o laudo histórico da rodada 1).
- Relatório 07 atualizado: nota de revisão v3 no cabeçalho; §1 (frase do parecer + referência à rodada A recuperada); §2 (rodada A); §6 (contagens vinculadas ao congelamento); §10.1 nova; §11 reescrito (comparação executada); §15 (6 anexos do alvo A). Relatório 01 atualizado (mutações e testes vinculados ao catálogo/ambiente congelados). README atualizado (4 clones, reprodução dos dois alvos, resultado em uma linha para A e B, delimitação com emenda de protocolo).
- Proveniência v3 fechada: scripts/99_fechamento.py estendido (3 comandos fase 10-a, 7 artefatos novos, repositório api-pgd com campo "origem" da emenda, nota v3 no MD, regra de congelamento da emenda); 23 hashes registrados.

Stage Summary:
- Corpus v3 fechado: rodada B congelada (resultados originais intocados), rodada A recuperada por re-execução e congelada (9d4b774c), comparação A × B executada sob paridade total de instrumento (10/10 fatores idênticos).
- Números canônicos da rodada A: exit 11 · 18/58 bruta · 18/29 aplicáveis · 25 pulados · 15 não habilitados · 0 indeterminados · 4 findings (4 ALTO) · 2,4 s · partição 18+17+23=58 idêntica à rodada B.
- Próximo passo, conforme a sequência do parecer: decisão sobre terceiro alvo (IA/ética) apenas depois; critério pré-registrado mantido no relatório 05 (§3).

---
Task ID: 18 (revisão v3.1 — notas de interpretação do parecer + rodada C completa com alvo de IA)
Agent: Super Z (agente principal)
Task: Incorporar as notas de interpretação do parecer da v3 ao corpus (formulação defensável da partição, complemento da métrica, justificativa da terceira rodada) e executar a rodada C completa — pré-triagem pré-registrada, seleção/congelamento do alvo de IA, execução com a instrumentação congelada, sanitização, triagem humana, relatórios e síntese do corpus A × B × C.

Work Log:
- Notas de interpretação (v3.1, sem alterar resultados congelados): relatório 05 §2.1 recebeu a nota do parecer (igualdade 18+17+23=58 NÃO prova equivalência de governança/segurança/privacidade; conclusão defensável integral; lista de dependências dos checks não aplicáveis); relatório 05 §3 recebeu a justificativa formal da terceira rodada (citação do parecer + regra "não escolher por parecer ter mais falhas"); relatório 07 §10.1 recebeu a formulação segura para citação (substitui uso absoluto de "62%") com complemento obrigatório; relatório 07 §11 recebeu a formulação defensável; cabeçalho do 07 anota a v3.1.
- Pré-triagem pré-registrada (matrices/pre-triagem-alvo-c.md): 8 critérios do parecer + critério técnico derivado do instrumento congelado ANTES da execução (leitura de e00_escopo.py: guarda computa indícios só em .py — ML deps, rotinas de decisão por nome, predict/fit/infer, chamadas LLM por hosts da categoria llm da régua); censo de ~19 candidatos (org gestaogovbr incluída — AIE/etica-ia-governanca examinado e rejeitado por não ter .py: a guarda E-00 permaneceria fechada); triagem fina de 3 finalistas com evidência computada (LlamaFactory, private-gpt, gpt-researcher); decisão: hiyouga/LlamaFactory — único finalista que ativa ethics pack (E-00) E vetores de treino (P-15/P-16); escolha por superfície de controles, não por falhas.
- Alvo C congelado: repos/llamafactory @ d6bb97ddff5d752d8b05aa099a168127c7253562 (main, 3097 commits, clone integral, Apache-2.0 consistente, 311 .py/~63k LOC); emenda de protocolo nº 2 declarada (quinto clone) no 03-execucao-alvo-c, README e proveniência.
- Execução: pse_inventory exit 20 (veredito indeterminado — PRIMEIRO do corpus), 31,62 s; guarda E-00 EM ESCOPO por fato computado (packs_fora_de_escopo vazio); estados 25 executados/12 pulados/19 não habilitados/2 indeterminados (E-06, P-15); 21 findings (18 ALTO, 3 MÉDIO); re-execução determinística verificada (~30,8 s; divergências só duracao/timestamp); laudo bruto sha256 81999d73….
- Análise (scripts/14, extensões declaradas a priori): partição QUADRIpartida 25+2+29+2=58 verificada por asserção (estado indeterminado nunca colapsado; E-12 classificado vetor estrutural pela forma do motivo, análogo ao P-19); indicadores 25/58 bruta, 25/39 aplicáveis (com indeterminados no denominador); matriz de estados matrices/estados-por-check-alvo-c.md.
- Sanitização (scripts/13, mesmas regras A/B): 12 hosts de S-04 mascarados [REDACTED-HOST], varredura global, zero literais proibidos; sha256 sanitizado cf7eb33d…; resumo executivo sanitizado alvo-c.
- Triagem humana (21 findings): 3 ausencia-de-evidencia-pse (P-04, P-07, E-07 — model card mesma forma declarativa); 6 confirmado-no-escopo (S-04 de egresso real de CI: pypi/docker/pytorch/nodesource/hf-mirror/cache interno); 12 possivel-falso-positivo (6 S-04 de UI/docs/exemplo; 3 P-16 com artefatos de parsing — 'w'=modo open(), 'utf-8'=encoding, mca_config=config de checkpoint; 3 E-10 sobre rotinas de treino, não decisão sobre pessoas); dúvida preservada em todos.
- Relatórios novos: 02-caracterizacao-alvo-c.md; 03-execucao-alvo-c.md (emenda nº 2, execução, indicadores, motivos, achados+triagem, alcance — incl. pyproject.toml fora de alcance por TOML, 6 observações de comportamento inéditas); 08-sintese-corpus.md (paridade de proveniência nas 3 rodadas, partição A/B idêntica × C deslocada confirmando interação catálogo×perfil, 4 achados técnicos do corpus + pilar ética/IA exercido, interpretação correta para citação, 7 limitações, contribuição para a tese).
- Atualizações: 07 (cabeçalho v3.1, §11 rodada C, 8 anexos novos); README (título do corpus, 5 clones, ordem de leitura 12–15, reprodução com llamafactory, resultado em uma linha da rodada C); 99_fechamento.py estendido (5 comandos fase 10-b, 10 artefatos novos, repo llamafactory com origem da emenda, nota v3.1) e re-executado (32 hashes).
- Verificação final: git status vazio nos 5 clones; sanitizado C sem literais proibidos (14 máscaras [REDACTED-HOST]).

Stage Summary:
- Corpus v3.1 fechado: 3 rodadas externas (A API/B pipeline/C IA) sob paridade total de instrumento, pré-triagem pré-registrada, partição quadripartida do alvo C e síntese A × B × C entregue (relatório 08).
- Números canônicos da rodada C: exit 20 · 25/58 bruta · 25/39 aplicáveis · 12 pulados · 19 não habilitados · 2 indeterminados (E-06, P-15) · 21 findings (18 ALTO, 3 MÉDIO) · 31,62 s · partição 25+2+29+2=58.
- Resultado central do corpus: a partição do catálogo se move com o perfil (18+17+23 em A/B sem IA → 25+2+29+2 em C com IA), confirmando a tese catálogo×perfil; pilar de ética/IA deixou de ser fora de escopo e agora produz evidência + insumos de calibração.

---
Task ID: 19 (empacotamento final — exportação do corpus v3.1)
Agent: Super Z (agente principal)
Task: Exportar pacote final contendo somente relatórios Markdown, matrizes, scripts, README, worklog, proveniência e laudos sanitizados, com MANIFEST-FINAL.md (lista de arquivos, SHA-256, versão da PSE Suite, catalog_hash, commits dos três alvos e instruções de reprodução); sem novas análises e sem modificar resultados.

Work Log:
- Gate de segurança do empacotamento: varredura dos candidatos — credencial sintética da mutação M2 (sk-live-plantada-…) em scripts/08_mutacoes.py confirmada como insumo metodológico documentado, sem valor real; hosts mascarados [REDACTED-HOST] nos 3 laudos sanitizados; nenhum padrão de credencial real.
- scripts/empacotar_final.py criado (mantido FORA do pacote, instrumental ao export): whitelist explícita de 37 arquivos (13 relatórios, 6 matrizes, 9 scripts, README, worklog, proveniência JSON, 6 laudos/resumos sanitizados), guardas de padrões proibidos (evidence/raw, repos/, .venv, .env, tool-results, laudos brutos), staging limpo com copy2, SHA-256 de todos os arquivos, cross-check vs 00-provenance.json, verificação de arquivos extras e geração do zip.
- Cross-check de integridade: 25/32 hashes da proveniência conferiram exatamente; 1 divergência esperada e documentada (reports/00-provenance.md — hash autoreferente); 6 hashes restantes correspondem a artefatos de evidence/raw/ deliberadamente excluídos do pacote.
- MANIFEST-FINAL.md gerado dentro do pacote: âncoras de congelamento (suite 0.20.0; schema laudo-pse-1.0; catalog_hash 4682a4ae…a0ac; commits pse-suite 443da92d, project 991e2d0f, alvo-a api-pgd 9d4b774c, alvo-b FastETL 9fb5d596, alvo-c LlamaFactory d6bb97dd), conteúdo por categoria, integridade SHA-256 por categoria, exclusões de segurança, nota sobre sanitização, resultados canônicos A/B/C com formulação defensável de citação, instruções de reprodução (5 clones congelados, venv, validação do instrumento, 3 execuções com resultados esperados, sanitização/análise/fechamento) e advertências (comparabilidade condicionada ao catalog_hash, contagens vinculadas ao congelamento, rodada A citada como reexecução de recuperação).
- Entregável: download/pacote-final-tpf-pse-v3.1.zip (38 arquivos = 37 do corpus + MANIFEST-FINAL.md; inspeção do zip confirmou zero artefatos proibidos).
- Congelamento preservado: nenhum resultado modificado, nenhuma análise nova; todos os comandos de empacotamento somente leitura sobre o corpus.

Stage Summary:
- Corpus v3.1 exportado, íntegro e reproduzível: pacote final em /home/z/my-project/download/pacote-final-tpf-pse-v3.1.zip com MANIFEST-FINAL.md interno (âncoras, hashes SHA-256, commits dos 3 alvos e reprodução).
