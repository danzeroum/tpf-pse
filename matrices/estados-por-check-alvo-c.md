# Matriz de estados por check — Alvo C (LlamaFactory, perfil IA/treinamento)

Laudo: `evidence/raw/laudo-alvo-c-bruto.json` · commit `d6bb97ddff5d752d8b05aa099a168127c7253562` · suite 0.20.0 · `catalog_hash 4682a4ae…a0ac` · modo `pse_inventory`

Classificação com precedência declarada (relatório 07, §10.1), com duas extensões declaradas a priori para este perfil (scripts/14_analise_alvo_c.py): partição quadriforme com estado indeterminado próprio; motivo do E-12 classificado como vetor estrutural ausente pela forma ("nenhuma exportação de embedding/hash derivado no código"), análogo ao P-19.

| Check | Pilar | Estado | Detalhe / motivo (resumido) |
|---|---|---|---|
| E-00 | ethics | executado | sem achado (substrato lido) |
| E-01 | ethics | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| E-02 | ethics | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| E-03 | ethics | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| E-04 | ethics | executado | sem achado (substrato lido) |
| E-05 | ethics | executado | sem achado (substrato lido) |
| E-06 | ethics | indeterminado — estado proprio | dataset de avaliacao ausente: nenhum `fairness_dataset` declarado em pse-config.yaml. Fairness  |
| E-07 | ethics | executado | 1 finding(s): ALTO |
| E-08 | ethics | pulado — dependente de contexto | nenhum tratamento de dado pessoal a rastrear: o catalogo nao declara campo personal/sensitive ( |
| E-09 | ethics | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| E-10 | ethics | executado | 3 finding(s): MEDIO |
| E-11 | ethics | executado | sem achado (substrato lido) |
| E-12 | ethics | pulado — nao aplicavel (vetor estrutural ausente) | nenhuma exportacao de embedding/hash derivado no codigo |
| E-13 | ethics | pulado — dependente de contexto | manifesto de terceiros ausente — sem ele todo host de dependencia seria achado, e ruido nao e e |
| P-01 | privacy | executado | sem achado (substrato lido) |
| P-02 | privacy | pulado — dependente de contexto | catalogo de dados ausente — cobrado por P-04 |
| P-03 | privacy | executado | sem achado (substrato lido) |
| P-04 | privacy | executado | 1 finding(s): ALTO |
| P-05 | privacy | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| P-06 | privacy | executado | sem achado (substrato lido) |
| P-07 | privacy | executado | 1 finding(s): ALTO |
| P-08 | privacy | pulado — dependente de contexto | catalogo de dados ausente — cobrado por P-04 |
| P-09 | privacy | executado | sem achado (substrato lido) |
| P-10 | privacy | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| P-11 | privacy | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| P-13 | privacy | executado | sem achado (substrato lido) |
| P-14 | privacy | executado | sem achado (substrato lido) |
| P-15 | privacy | indeterminado — estado proprio | ha treino de modelo, mas nao existe catalogo de dados para dizer se os campos usados como featu |
| P-16 | privacy | executado | 3 finding(s): ALTO |
| P-17 | privacy | executado | sem achado (substrato lido) |
| P-18 | privacy | pulado — dependente de contexto | catalogo de dados ausente — cobrado por P-04; sem inventario nao ha campo sensivel a confrontar |
| P-19 | privacy | pulado — nao aplicavel (vetor estrutural ausente) | nenhuma producao de evento em barramento append-only no codigo — nao ha registro imutavel a con |
| P-20 | privacy | executado | sem achado (substrato lido) |
| P-22 | privacy | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| P-23 | privacy | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| P-24 | privacy | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-01 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-02 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-03 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-04 | security | executado | 12 finding(s): ALTO |
| S-05 | security | pulado — dependente de contexto | manifesto de terceiros ausente — cobrado por S-04 |
| S-06 | security | executado | sem achado (substrato lido) |
| S-07 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-08 | security | pulado — dependente de contexto | manifesto de terceiros ausente — cobrado por S-04 |
| S-09 | security | executado | sem achado (substrato lido) |
| S-10 | security | executado | sem achado (substrato lido) |
| S-11 | security | executado | sem achado (substrato lido) |
| S-12 | security | pulado — dependente de contexto | nenhum arquivo se declara contrato de API (sem chave `openapi` nem `swagger` de topo) — nao ha  |
| S-13 | security | executado | sem achado (substrato lido) |
| S-14 | security | executado | sem achado (substrato lido) |
| S-15 | security | executado | sem achado (substrato lido) |
| S-16 | security | pulado — dependente de contexto | nenhuma politica de residencia de dados declarada (`data_residency` na config ou no manifesto)  |
| S-17 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-18 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-19 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-20 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-21 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-22 | security | pulado — dependente de contexto | nenhuma finalidade entra no servidor: nenhum ponto do codigo le `X-Purpose` nem chave equivalen |

**Partição:** executados 25 + não aplicáveis 2 + dependentes de contexto 29 + indeterminados 2 = 58 de 58 — partição mutuamente exclusiva do catálogo (estado indeterminado preservado, nunca colapsado).

Nota: motivos abreviados para leitura; os motivos íntegros constam do laudo. Nenhum motivo de pulo é silencioso.
