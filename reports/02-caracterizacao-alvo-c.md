# 02 — Caracterização factual do alvo C — LlamaFactory (perfil IA/treinamento)

> Caracterização **factual e neutra** do clone analisado, para contextualizar a leitura do laudo. Nada nesta seção constitui avaliação de qualidade, segurança ou conformidade do projeto; as observações registram superfícies relevantes para a aplicabilidade dos checks, na forma do relatório 02 do alvo B.

## 1. Identificação e congelamento

| Atributo | Valor |
|---|---|
| Repositório | `hiyouga/LlamaFactory` (público, não-fork, não-arquivado) |
| Commit congelado | `d6bb97ddff5d752d8b05aa099a168127c7253562` (branch `main`, 2026-08-31) |
| Histórico | clone integral com histórico completo — 3.097 commits |
| Licença | Apache-2.0 (`LICENSE` e campo `license` do `pyproject.toml` — **consistentes entre si**, sem divergência documental) |
| Empacotamento | `pyproject.toml` (hatchling); `requires-python >= 3.11`; dependência núcleo `torch>=2.4.0` |
| Atividade | pushed em 2026-08-31; ~74 mil estrelas; artigo ACL 2024; adotado na indústria (badges "used by" no README) |
| Seleção | pré-triagem pré-registrada em `matrices/pre-triagem-alvo-c.md` (8 critérios do parecer + critério técnico de abertura da guarda E-00), antes da execução |

## 2. Inventário factual do clone

| Grandeza | Valor |
|---|---|
| Arquivos Python | 311 (~62,9 mil linhas) |
| YAML | 113 (inclui workflows de CI, templates de issue e configuração) |
| JSON | 20 + 5 `.jsonl` (registros e datasets demonstrativos) |
| Markdown | 75 (README bilíngue ~1.000 linhas, docs) |
| Outros | mídia (`mp4/mp3/wav/flac/jpg/svg`), `.cff`, TOML, shell ×4 |
| Pastas principais | `src/llamafactory/{api, chat, data, eval, extras, hparams, model, third_party, train, v1, webui}`, `examples/` (108 arquivos), `data/` (35), `docs/` (66), `docker/` (13), `tests/` (38) + `tests_v1/` (20), `scripts/` (21), `requirements/` (25) |
| CI | `.github/workflows/`: `tests.yml`, `tests_npu.yml`, `docker.yml`, `publish.yml` |

## 3. Perfil arquitetural (para leitura do laudo)

1. **Framework de treinamento/afinamento de LLMs** — o substrato central são pipelines de treino (`train/`: sft, rm, dpo, kto, mca, megatron_bridge, hyper_parallel), com chamadas reais de treino/avaliação (`trainer.train()`, `trainer.fit()`, `trainer.predict(...)`) sobre `torch`/`transformers`. É o terceiro perfil arquitetural do corpus, distinto da API (alvo A) e da biblioteca de pipelines (alvo B).
2. **Registry declarativo de datasets** — `data/dataset_info.json` cataloga os datasets demonstrativos (alpaca, dpo, kto, identity, glaive, c4) com referências a fontes externas; é a superfície mais próxima de um "inventário" no repositório (não é um catálogo PSE e não declara classes `personal`/`sensitive`).
3. **Superfícies de egresso variadas** — integrações de runtime (download de modelos hospedados externamente), integrações opcionais de experiment tracking (nomeadas em strings de UI), egresso de CI (índices de pacotes, registry, mirror) e URLs de documentação/autopresentação em strings de UI.
4. **WebUI** — módulo `webui/` com strings localizadas extensas (`locales.py`, >2 mil linhas) e `api/` para serving; `examples/` inclui scripts de exemplo que referenciam assets externos.
5. **Sem artefatos do padrão PSE** — nenhum `pse-config.yaml`, catálogo de dados, modelo de consentimento, manifesto de terceiros, declaração de residência ou model card versionado no repositório (fato factual, sem conotação de falta — ver relatório 03, §3).
6. **Divergência de licença inexistente** — ao contrário do alvo B (GPLv3 no LICENSE × Apache no setup.py), o alvo C declara Apache-2.0 de forma consistente nos dois pontos (observação factual registrada para comparação de perfis).

## 4. Motivação da seleção (síntese)

O alvo foi selecionado por responder à lacuna conceitual pré-registrada do corpus: os alvos A e B deixaram todo o pilar de ética/IA fora de escopo (guarda E-00: 14 checks em ambos) e os vetores de treino não aplicáveis (P-15/P-16). O LlamaFactory contém, em código efetivo Python, os três tipos de indício que a guarda E-00 é definida para reconhecer (dependência de ML, rotinas com nomes de decisão/avaliação, chamadas de inferência/treino) — o que torna o pack de ética **em escopo por fato computado**, sem qualquer declaração ou adaptação do alvo. A escolha não considerou findings, severidades ou histórico de incidentes: apenas a superfície de controles observável estaticamente, conforme a matriz de pré-triagem.
