# TPF — Avaliação exploratória da PSE Suite sobre corpus externo (FastETL, API PGD e alvo de IA)

**Rodada 2** do Trabalho Prático Final (Projeto Técnico) — Pós-Graduação em Arquitetura e Engenharia de Software, FIA Online.

> **Natureza do estudo:** avaliação exploratória, estática e somente leitura.
> **Delimitação:** clones locais de código público (cinco após as emendas de protocolo — nº 1: recuperação da rodada A, relatório 05, §1; nº 2: rodada C com alvo de IA, relatório 03-execucao-alvo-c), commits congelados, sem execução de DAGs/treinos, sem subir Airflow, sem acesso a bancos, sem chamadas a fontes externas, sem credenciais e sem interação com ambiente de produção.
> **Nada aqui constitui** auditoria, certificação, parecer jurídico, teste em produção ou comprovação de ausência de riscos. Nenhuma afirmação caracteriza vulnerabilidade, violação legal ou desconformidade do FastETL, da API PGD, do LlamaFactory, de seus mantenedores ou de qualquer organização.

## Estrutura

```
tpf-pse-fastetl/
├── repos/                  clones congelados por SHA (pse-suite, project, FastETL, api-pgd, llamafactory)
├── evidence/
│   ├── raw/                material bruto local — NÃO divulgar
│   ├── sanitized/          anexos seguros (laudos sanitizados + resumos, alvos A, B e C)
│   └── provenance/         00-provenance.json
├── reports/                00 a 08 (rodadas A/B/C + comparações + síntese do corpus)
├── matrices/               pré-triagens (B e C), mutações, matriz central, estados dos alvos A e C
└── scripts/                scripts de proveniência, análise, sanitização e mutações
```

## Ordem de leitura

1. `reports/00-provenance.md` — proveniência, comandos, hashes.
2. `reports/01-caracterizacao-pse-suite.md` — a régua (e princípios do consumidor de referência).
3. `reports/02-caracterizacao-alvo-b.md` — o alvo (FastETL; nomenclatura neutra "alvo-b" por decisão do parecer).
4. `matrices/cobertura-por-artefato.md` — pré-triagem de aplicabilidade (Fase 5).
5. `reports/03-execucao-alvo-b.md` + `evidence/sanitized/resumo-executivo-laudo.md` — a execução.
6. `reports/04-validacao-manual-e-limitacoes.md` — classificação humana dos achados.
7. `matrices/mutacoes-e-resultados.md` — mutações controladas M1–M8.
8. `matrices/requisito-check-evidencia-limite.md` — matriz central (58 checks).
9. `reports/02-caracterizacao-alvo-a.md` + `reports/03-execucao-alvo-a.md` + `evidence/sanitized/resumo-executivo-laudo-alvo-a.md` — rodada A (API PGD) recuperada por re-execução local.
10. `matrices/estados-por-check-alvo-a.md` — matriz de estados do alvo A (58 checks).
11. `reports/05` (comparação A × B), `reports/06` (piloto), `reports/07-relatorio-final-alvo-b.md` — síntese final.
12. `matrices/pre-triagem-alvo-c.md` — pré-triagem pré-registrada do alvo de IA (8 critérios do parecer + critério técnico da guarda E-00).
13. `reports/02-caracterizacao-alvo-c.md` + `reports/03-execucao-alvo-c.md` + `evidence/sanitized/resumo-executivo-laudo-alvo-c.md` — rodada C (LlamaFactory).
14. `matrices/estados-por-check-alvo-c.md` — matriz de estados do alvo C (partição quadriforme).
15. `reports/08-sintese-corpus.md` — síntese do corpus A × B × C (documento de fechamento para o TPF).

## Reprodução segura do experimento

Pré-requisitos: Python ≥ 3.10, Git, `pip`. Sem Docker; sem Airflow; sem rede além dos clones e do `pip install` (os hosts dos clones estão nas URLs abaixo).

```bash
# 1. Diretório de trabalho e clones (commits congelados: ver 00-provenance.md)
mkdir tpf-pse-fastetl && cd tpf-pse-fastetl && mkdir -p repos evidence/{raw,sanitized,provenance} reports matrices scripts
git clone https://github.com/danzeroum/pse-suite.git repos/pse-suite
git clone https://github.com/danzeroum/project.git repos/project
git clone https://github.com/gestaogovbr/FastETL.git repos/FastETL
git clone https://github.com/gestaogovbr/api-pgd.git repos/api-pgd   # emenda de protocolo (relatório 05, §1)
git clone https://github.com/hiyouga/LlamaFactory.git repos/llamafactory  # emenda de protocolo nº 2 (rodada C)

# 2. Congelamento (registre SHA/branch/data de cada clone)
for r in pse-suite project FastETL api-pgd llamafactory; do git -C repos/$r rev-parse HEAD; done

# 3. Ambiente isolado e instalação da suite
python3 -m venv .venv-pse
./.venv-pse/bin/pip install -e "repos/pse-suite[dev]"

# 4. Autoprova e testes oficiais da suite (registre falhas e pulados)
./.venv-pse/bin/pse --manifesto
./.venv-pse/bin/pse --self-test
(cd repos/pse-suite && /caminho/para/tpf-pse-fastetl/.venv-pse/bin/python -m pytest -q)

# 5. Execução estática contra os clones locais (única execução sobre cada alvo)
./.venv-pse/bin/pse --path repos/FastETL --modo pse_inventory \
    --output evidence/raw/laudo-alvo-b-bruto.json
./.venv-pse/bin/pse --path repos/api-pgd --modo pse_inventory \
    --output evidence/raw/laudo-alvo-a-bruto.json
./.venv-pse/bin/pse --path repos/llamafactory --modo pse_inventory \
    --output evidence/raw/laudo-alvo-c-bruto.json

# 6. Sanitização antes de divulgar qualquer coisa
python3 scripts/06_sanitizar.py
python3 scripts/12_sanitizar_alvo_a.py
python3 scripts/13_sanitizar_alvo_c.py
```

### Regras mandatórias de reprodução

- **Nunca altere** os clones (`git status --porcelain` deve ficar vazio); mutações só em cópias descartáveis (ver `scripts/08_mutacoes.py`).
- **Nunca execute** `pse_passive`/`pse_active`, DAGs, Docker, Airflow, banco ou qualquer serviço; nunca acesse credenciais.
- **Nunca publique** `evidence/raw/` nem literais apontados por achados — use `[REDACTED]` + check + `arquivo:linha` (ver `scripts/06_sanitizar.py`).
- **Não trate** achados como vulnerabilidade, desconformidade ou falha: são indícios técnicos que requerem validação humana.

## Resultado em uma linha

Rodada B (FastETL congelado `9fb5d596`): **exit 11 · 18/58 executados · 25 pulados com motivo · 15 não habilitados · 0 indeterminados · 8 achados (6 ALTO, 2 MÉDIO) · 2,0 s** — todos os achados sanitizados e classificados; 8 mutações controladas documentam que a régua morde e declara seus limites.

Rodada A (API PGD congelado `9d4b774c`, recuperação por re-execução local — relatório 05, §1): **exit 11 · 18/58 · 18/29 aplicáveis · 25 pulados · 15 não habilitados · 0 indeterminados · 4 achados (4 ALTO) · 2,4 s** — mesma partição do catálogo (18 + 17 + 23 = 58) sob a mesma instrumentação; comparação A × B com paridade de proveniência nos dez fatores do parecer (relatório 05, §2.5).

Rodada C (LlamaFactory congelado `d6bb97d`, alvo de IA — emenda de protocolo nº 2): **exit 20 (indeterminado) · 25/58 executados · 12 pulados · 19 não habilitados · 2 indeterminados (E-06, P-15) · 21 achados (18 ALTO, 3 MÉDIO) · 31,6 s** — guarda E-00 em escopo por fato computado; partição deslocada para 25 + 2 + 29 + 2 = 58, confirmando a interação catálogo×perfil; síntese do corpus em `reports/08-sintese-corpus.md`.
