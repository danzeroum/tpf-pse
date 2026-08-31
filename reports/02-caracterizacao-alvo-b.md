# 02 — Caracterização factual do FastETL

**Estudo:** TPF — PSE Suite × FastETL (rodada 2)
**Alvo:** clone local congelado — `https://github.com/gestaogovbr/FastETL.git` · branch `main` · SHA `9fb5d596cd8c3d4d0efcf6cdd1ca0c7b5e24afc1` · último commit 2026-04-29T16:19:31-03:00 · tag descritiva `0.2.14-3-g9fb5d59`
**Natureza:** descrição factual baseada apenas em README, LEIAME, documentação pública e leitura estática do clone. Nenhuma inferência sobre dados reais, ambientes de produção ou conduta dos mantenedores.

---

## 1. Descrição factual (citando a documentação pública)

Conforme o README/LEIAME, o **FastETL** é "a plugins package for Airflow for building data pipelines for a number of common scenarios" — um pacote de plugins para Apache Airflow para construção de pipelines de dados em cenários comuns. Funcionalidades declaradas na documentação:

- **Replicação** de tabelas *full* ou incremental em bancos SQL Server, Postgres e MySQL;
- Carga de dados de **Google Sheets** e de planilhas em redes **Samba/Windows**;
- Extração de **CSV** a partir de SQL;
- Limpeza de dados via tasks customizadas de *patch* (ex.: coordenadas geográficas, mapeamento de valores canônicos em colunas);
- Consulta a serviço **OSRM** para cálculo de distâncias de rota;
- Uso de **CKAN** ou da API do dados.gov.br para atualização de metadados de datasets;
- Dicionários de dados em OpenDocument via Frictionless Tabular Data Packages;
- (LEIAME) Consulta à API do Diário Oficial da União (**DOU**).

A documentação afirma que o framework "is maintained by a network of developers from many teams at the Ministry of Management and Innovation in Public Services" e que é "widely used for replication of data queried via Quartzo (DaaS) from Serpro" — citação factual da documentação, sem inferência adicional. A instalação é como provider padrão de Airflow: `pip install apache-airflow-providers-fastetl`, com nota de que as bibliotecas `msodbcsql17` e `unixodbc-dev` devem estar presentes nos workers.

## 2. Linguagens, frameworks, dependências, estrutura e licença

| Aspecto | Observação factual |
|---|---|
| Linguagem | Python (43 arquivos `.py`, ~8.007 linhas) |
| Framework central | Apache Airflow ≥ 2.3 (provider/plugin; DAGs, operators, hooks) |
| Drivers/bancos | pyodbc + msodbcsql17 (SQL Server), psycopg2 (Postgres), provider MySQL, alembic |
| Integrações declaradas | ckanapi, pygsheets, google-api-python-client, google-auth, pysmb, frictionless, odfpy, pandas, openmetadata-ingestion, Markdown, beautifulsoup4 |
| Empacotamento | `setup.py` com entry point `apache_airflow_provider` (`fastetl.__init__:get_provider_info`) |
| Versão | derivada de env var `TAG_NAME` (`0.0.0-dev` default); último release documentado no CHANGELOG: 0.2.14 |
| CI próprio | `.github/workflows/ci-tests.yml` (badge no README), `build-and-publish.yml`, `trigger-airflow2-docker.yml` |
| Testes | `tests/` com pytest, `docker-compose.yml` e `wait-for-airflow.sh` — **o Makefile provisiona Airflow via Docker (`make setup/tests`); NADA disso foi executado nesta rodada** |
| Licença | arquivo `LICENSE` contém **GNU General Public License v3**; o `setup.py` declara `license="Apache License 2.0"`. Registrou-se apenas esta divergência documental entre artefatos do próprio repositório, sem qualquer qualificação. |
| Container | `Dockerfile` baseado em `apache/airflow:2.10.5-python3.10`, instala drivers ODBC da Microsoft |

## 3. Estrutura de diretórios

```
FastETL/
├── fastetl/                  pacote do provider (43 .py no total)
│   ├── __init__.py           get_provider_info()
│   ├── data_types.py         tipos (DBSource etc.)
│   ├── operators/            5 operators: db_to_db, db_to_csv, gsheet,
│   │                         osrm_distance, datapackage_to_datadictionary
│   ├── hooks/                5 hooks: db_to_db, ckan, dadosgovbr, gsheet, osrm
│   ├── custom_functions/     núcleo: fast_etl.py (cópia/sync entre bancos),
│   │                         patchwork.py, samba_services.py, sharepoint.py,
│   │                         copy_db_extensions.py, config.py, utils/
│   └── example_dags/         1 DAG de exemplo (db_to_db)
├── tests/                    pytest + docker-compose (não executado)
├── docs/                     apenas imagens (logo etc.) — nenhum texto de processo
├── Dockerfile, Makefile, requirements.txt, setup.py, CHANGELOG.md
└── .github/workflows/        3 workflows
```

## 4. Papel do Airflow e riscos arquiteturais potenciais (em linguagem geral)

O FastETL é um **plugin**: ele estende o Airflow com operators e hooks que o orquestrador executa como tarefas de DAG. Em linguagem geral — sem inferir tratamento de dados pessoais reais —, pipelines de dados com este perfil apresentam superfícies arquiteturais típicas que justificam governança estática: (i) **credenciais transitam por Connections do Airflow** (`BaseHook.get_connection`), e o padrão comum de hooks lê `conn.password` para APIs (ckan, gsheet, dadosgovbr) e strings de conexão ODBC; (ii) **logs são a principal superfície de observabilidade** de operators e funções customizadas (contagens estáticas altas de `logging/logger/self.log` em `patchwork.py`, `fast_etl.py`, `copy_db_extensions.py`); (iii) **replicação entre bancos** copia colunas de origem para destino conforme mapeamento de tipos — a seleção de colunas é configurável por DAG; (iv) **integrações externas** (CKAN, dados.gov.br, OSRM, Google Sheets, Samba/SharePoint) constituem egresso declarado em código; (v) **variáveis de ambiente** são usadas para propagar strings de conexão em alguns pontos (`load_env_var.py`, `gsheet_hook.py`). Essas são categorias de superfície observáveis estaticamente; **nada se afirma** sobre o conteúdo tratado em qualquer instância de uso do plugin.

## 5. Inventário de arquivos por extensão e diretório

**Por extensão (total 64 arquivos):** `.py` 43 (8.007 linhas) · `.sql` 5 (47) · `.md` 3 (409) · `.yml` 2 (408) · `.png` 2 · binários/imagens `.xcf`, `.zip`, `.svg` 3 · `.sh` 1 · `.txt` 1 · sem extensão 4 (867 linhas — p.ex. `Dockerfile`, `LICENSE`).

**Por diretório:** raiz 9 arquivos (1.345 linhas); `fastetl/custom_functions/` 20 arquivos (5.400 linhas — o núcleo); `fastetl/operators/` 6 (885); `fastetl/hooks/` 6 (853); `fastetl/example_dags/` 1 (31); `fastetl/data_types.py` 1 (46); `tests/` 12 arquivos (1.232 linhas); `docs/images/` 5; `.github/` 3 workflows.

## 6. Mapa de compatibilidade FastETL × PSE Suite

| Artefato do FastETL | Exemplo de diretório/extensão | Capacidade potencial da PSE | Limite esperado |
|---|---|---|---|
| Código Python | `fastetl/**/*.py` | checks estáticos de código (P-01, P-06, S-06, E-13, P-19, P-20, E-04, E-05…) | não prova comportamento em runtime de DAG |
| Dependências | `requirements.txt`, `setup.py` | inventário e rastreabilidade; E-13 (host de dependência) | não equivale a análise de vulnerabilidade de dependência |
| Contêiner | `Dockerfile` | superfície de configuração (leitura declarativa) | cobertura depende de cada check; sem parser de Dockerfile declarado |
| Workflows | `.github/workflows/*.yml` | inspeção declarativa | não executa pipeline remoto |
| Testes | `tests/` | identificar fixtures/contexto; rebaixamento de severidade em caminho de teste (ratificação 11) | risco de falso positivo em exemplos |
| DAGs de exemplo | `fastetl/example_dags/`, `tests/dags/` | leitura como código Python | exemplos/fixtures podem gerar achados que exigem classificação humana |
| SQL | `tests/sql/*.sql` | substrato `sql` de checks declarativos (P-03) | cobertura limitada ao que a réga reconhece |
| Documentação | `docs/` (apenas imagens), README | evidência de processo — **ausente/insuficiente aqui** | não comprova operação efetiva; ausência de artefato PSE ≠ ausência de controle organizacional |

## 7. Delimitação obrigatória

> **A análise utiliza clone local de código público, commit congelado e modo estático, sem execução de DAGs, sem subir Airflow, sem acesso a bancos, sem chamadas a fontes externas, sem credenciais e sem interação com ambiente de produção.**

Nenhuma inferência deste relatório caracteriza vulnerabilidade, violação legal, desconformidade LGPD ou falha de produção do FastETL, de seus mantenedores ou de qualquer órgão público. Trata-se de caracterização de superfície técnica para a pré-triagem de aplicabilidade da PSE Suite (Fase 5).
