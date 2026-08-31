# Matriz de estados por check — Alvo A (api-pgd, recuperação por re-execução local)

Laudo: `evidence/raw/laudo-alvo-a-bruto.json` · commit `9d4b774c` · suite 0.20.0 · `catalog_hash 4682a4ae…a0ac` · modo `pse_inventory`

Classificação com precedência declarada (relatório 07, §10.1): executado / não aplicável (guarda E-00 ou vetor estrutural ausente) / dependente de contexto (artefato declarativo do operador ou Trabalho A).

| Check | Pilar | Estado | Detalhe / motivo (resumido) |
|---|---|---|---|
| E-00 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-01 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-02 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-03 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-04 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-05 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-06 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-07 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-08 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-09 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-10 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-11 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-12 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
| E-13 | ethics | pulado — nao aplicavel | guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13) |
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
| P-15 | privacy | pulado — nao aplicavel | nenhuma chamada de treino no codigo — nao ha feature a confrontar com o catalogo |
| P-16 | privacy | pulado — nao aplicavel | nenhuma chamada de treino no codigo — nao ha dataset de treino a inventariar |
| P-17 | privacy | executado | sem achado (substrato lido) |
| P-18 | privacy | pulado — dependente de contexto | catalogo de dados ausente — cobrado por P-04; sem inventario nao ha campo sensivel a confrontar |
| P-19 | privacy | pulado — nao aplicavel | nenhuma producao de evento em barramento append-only no codigo — nao ha registro imutavel a con |
| P-20 | privacy | executado | sem achado (substrato lido) |
| P-22 | privacy | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| P-23 | privacy | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| P-24 | privacy | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-01 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-02 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-03 | security | nao habilitado — dependente de contexto | Trabalho A sem target declarado (previsto e nao pedido) |
| S-04 | security | executado | 2 finding(s): ALTO |
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

**Partição:** executados 18 + não aplicáveis 17 + dependentes de contexto 23 = 58 de 58 — partição mutuamente exclusiva do catálogo.

Nota: motivos abreviados para leitura; os motivos íntegros constam do laudo. Nenhum motivo de pulo é silencioso.
