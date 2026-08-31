# 02 — Caracterização factual do alvo A — API PGD (Fase de recuperação)

**Contexto desta caracterização:** os insumos originais da rodada 1 (API PGD) não estavam disponíveis neste ambiente (registro no relatório 05 da v2). Conforme a sequência recomendada pelo parecer da orientação, a rodada A foi **recuperada por re-execução local** com a mesma instrumentação congelada da rodada B. Esta caracterização descreve o alvo congelado nesta recuperação — é um retrato factual, sem qualquer veredito de segurança, conformidade ou qualidade.

## 1. Identificação e congelamento

| Atributo | Valor |
|---|---|
| Repositório público | `gestaogovbr/api-pgd` |
| URL | `https://github.com/gestaogovbr/api-pgd` |
| Commit congelado | `9d4b774cc6763b234372999a1d1c4baf248e3080` |
| Tag descritiva | `3.3.10` (o HEAD congelado coincide com a tag) |
| Data do commit | 2026-07-07 (fuso do repositório) |
| Histórico | completo — 1.396 commits no clone |
| Estado do clone | limpo (`git status --porcelain` vazio; nenhum arquivo criado no alvo) |

Descrição pública do projeto (transcrita do README): *"API integradora de dados de sistemas do Programa de Gestão, usado para o teletrabalho na administração pública federal do Brasil"*. O repositório é a API backend do sistema de Programas de Gestão — mesmo órgão mantenedor do FastETL (org `gestaogovbr`), o que torna os dois alvos comparáveis quanto a contexto institucional, ainda que os perfis arquiteturais sejam distintos.

## 2. Perfil arquitetural e stack

API Python de backend construída sobre **FastAPI 0.111.0** (com `uvicorn`), **SQLAlchemy 2.0.31** (PostgreSQL via `psycopg` 3.2.1) e **Pydantic 2.8.2** — as três dependências nucleares, todas com versão pinada em `requirements.txt` (12 dependências no total, incluindo `python-jose` para JWT, `passlib`/`bcrypt` para senhas, `fastapi-mail` para e-mail e `httpx` para testes). Não há `pyproject.toml` nem `setup.py` na raiz: o manifesto de dependências é exclusivamente o `requirements.txt`, e a aplicação é empacotada/executada via Docker (`Dockerfile` + `docker-compose.yml` + `Makefile`) — nenhum desses artefatos foi executado neste estudo.

A organização do código segue o layout canônico de uma aplicação FastAPI de porte moderado: `src/api.py` (rotas), `src/crud.py` e `src/crud_auth.py` (camada de dados), `src/models.py` e `src/schemas.py` (modelos ORM e contratos de entrada), `src/response_schemas.py` (contratos de saída), `src/db_config.py` e `src/db_audit.py` (configuração e auditoria de banco), `src/email_config.py` e `src/util.py`. Há ainda `migration/` (Alembic) e documentação em `docs/` (guias de autenticação e gestão de usuários) com cinco arquivos de exemplo executável em `docs/examples/`.

## 3. Inventário factual

| Grandeza | Valor |
|---|---|
| Arquivos rastreados pelo Git | 52 |
| Arquivos Python | 31 |
| Distribuição | `tests/` 19 · `src/` 13 · `docs/` 9 · CI 2 · raiz 9 |
| Workflows de CI | 2 (`ci_tests.yml` e build de imagem Docker) |
| Licença | **AGPLv3** (GNU Affero General Public License v3, sem divergência interna observada — não há `setup.py` com metadado de licença) |
| Cobertura de linguagem pelo laudo | Python 31 (AST), YAML 3, JSON 3, SQL 1 — **0 arquivos fora de alcance** |

## 4. Superfícies estáticas relevantes para a suite

Três observações factuais (registradas de forma neutra, sem caracterização de risco) orientam a leitura da execução no relatório 03-alvo-a. Primeira: **não há artefatos declarativos do perfil PSE** no clone — nenhum catálogo de dados, modelo de consentimento, manifesto de terceiros, `pse-config.yaml` ou declaração de residência/finalidade; o laudo aponta `tests/qa/catalog.yaml` e `tests/qa/consent-model.yaml` como os locais convencionados pelo perfil, que não existem no clone. Segunda: o clone é uma **aplicação completa** (não uma biblioteca distribuída): as rotas, modelos e configurações vivem no mesmo repositório que a executaria, o que o distingue do perfil biblioteca/pipeline do FastETL. Terceira: `src/response_schemas.py` e `docs/examples/` contêm referências a hosts externos em contexto de documentação/exemplo (caso apontado por S-04 e classificado no relatório 03-alvo-a), o que representa um tipo de superfície distinto das integrações operacionais observadas na rodada B.

## 5. Nota de delimitação

Esta caracterização é descritiva e reprodutível: cada fato acima pode ser verificado com `git`, `wc` e leitura direta do clone congelado. Nenhuma afirmação aqui — nem em qualquer relatório desta recuperação — constitui avaliação de vulnerabilidade, desconformidade LGPD, qualidade de código ou prática de engenharia do projeto, de seus mantenedores ou de órgãos públicos.
