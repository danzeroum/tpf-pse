# MANIFEST-FINAL — Pacote final do corpus TPF PSE Suite (revisão v3.1)

**Estudo:** TPF — Avaliação exploratória da PSE Suite sobre corpus externo (FastETL, API PGD e alvo de IA) — Rodada 2 do Trabalho Prático Final (Projeto Técnico), Pós-Graduação em Arquitetura e Engenharia de Software, FIA Online.
**Natureza:** avaliação exploratória, estática e somente leitura, sobre clones públicos congelados, sem execução de DAGs/treinos, sem acesso a bancos, sem chamadas a fontes externas e sem credenciais.
**Estado do corpus:** revisão v3.1 concluída — corpus metodologicamente consistente e utilizável no TPF (fechamento da orientação). Este pacote não modifica nenhum resultado congelado.
**Geração do pacote:** 2026-08-31 23:01 UTC

> **Delimitação de leitura:** nenhuma afirmação deste pacote caracteriza vulnerabilidade, violação legal ou desconformidade do FastETL, da API PGD, do LlamaFactory, de seus mantenedores ou de qualquer organização. Os laudos sanitizados são evidência de execução da suíte no modo estático, sujeita às limitações declaradas nos relatórios 04, 05 e 08.

---

## 1. Âncoras de congelamento

### 1.1 Instrumento — PSE Suite

| Campo | Valor |
|---|---|
| Suite version | **0.20.0** |
| Schema do laudo | `laudo-pse-1.0` |
| catalog_hash | `4682a4ae1115e577e95e2ddbd666bfd041efb2fca4b3d77e7683e2055571a0ac` |
| Commit da suite (`danzeroum/pse-suite`) | `443da92dbdb22a9af18aa6eebb51aac2da901458` (tag descritiva `v0.3.0-53-g443da92`) |
| Commit do consumidor de referência (`danzeroum/project`) | `991e2d0f28d746e40a80c89280bdd9060f5a0311` |
| Autoprova da suite | OK — 58 mutações canônicas, 0 falhas; E-06 indeterminado na fixture (esperado) |
| Testes oficiais da suite | 809 aprovados, 10 pulados (8 Playwright ausente; 2 aceite btv ausente) — **contagem vinculada à configuração local registrada na proveniência, não propriedade permanente do produto** |

### 1.2 Alvos avaliados — commits congelados das três rodadas

| Rodada | Alvo (nomenclatura neutra) | Repositório público | Commit congelado | Observações |
|---|---|---|---|---|
| A | `alvo-a` | `gestaogovbr/api-pgd` | `9d4b774cc6763b234372999a1d1c4baf248e3080` | tag `3.3.10`; rodada recuperada por **re-execução local** com a mesma instrumentação da rodada B (emenda de protocolo — relatório 05, §1) |
| B | `alvo-b` | `gestaogovbr/FastETL` | `9fb5d596cd8c3d4d0efcf6cdd1ca0c7b5e24afc1` | tag descritiva `0.2.14-3-g9fb5d59` |
| C | `alvo-c` | `hiyouga/LlamaFactory` | `d6bb97ddff5d752d8b05aa099a168127c7253562` | `main`; selecionado por **pré-triagem pré-registrada** antes da execução (emenda de protocolo nº 2 — `matrices/pre-triagem-alvo-c.md`) |

### 1.3 Ambiente de execução

Debian GNU/Linux 13 (trixie), x86_64 · Python 3.12.14 · pip 25.0.1 · git 2.47.3 · venv isolado `.venv-pse` (`pip install -e repos/pse-suite[dev]`). Detalhes completos em `evidence/provenance/00-provenance.json` (`ambiente`, `comandos` com exit codes e durações).

---

## 2. Conteúdo do pacote — 37 arquivos + este manifesto

| Categoria | Diretório no pacote | Nº de arquivos |
|---|---|---:|
| Relatório Markdown | `reports/` | 13 |
| Matriz | `matrices/` | 6 |
| Script | `scripts/` | 9 |
| README | `raiz do pacote` | 1 |
| Worklog | `raiz do pacote` | 1 |
| Proveniência | `evidence/provenance/` | 1 |
| Laudo sanitizado | `evidence/sanitized/` | 6 |
| (este manifesto) | `MANIFEST-FINAL.md` | 1 |

**Ordem de leitura recomendada:** ver `README.md` (seção "Ordem de leitura", itens 1–15).

---

## 3. Integridade — SHA-256 por categoria

### Relatório Markdown (13 arquivos)

| Arquivo (caminho no pacote) | Tamanho (bytes) | SHA-256 |
|---|---:|---|
| `reports/00-provenance.md` | 11349 | `60a1a9d900116dd9293504e97d1f08ccb61cd621c9ba1a370f46be88062bde26` |
| `reports/01-caracterizacao-pse-suite.md` | 17151 | `5fdc8dd14add81d26b775cc44ef2b15727788098ce218eb47eb1ec5882a771f1` |
| `reports/02-caracterizacao-alvo-a.md` | 4833 | `f5b4471f002fa5bb03bf88214ea5d2af2c4205e94492b9e50c8757fd280e93bc` |
| `reports/02-caracterizacao-alvo-b.md` | 8643 | `ddd087c9ce2eca6730a529424a074fccd923d07271c67a74d65e3bfa79a36af8` |
| `reports/02-caracterizacao-alvo-c.md` | 4599 | `2acdcc0960bc0267bed27708c42c9ac3ceb9efc8012996f0023cc8ec91652d96` |
| `reports/03-execucao-alvo-a.md` | 13525 | `336b6f7689933fa2351156652d7b1118a1744b6747984236697f175291164ec1` |
| `reports/03-execucao-alvo-b.md` | 11805 | `6d06bf1bec193a1e116fd4d33eacfaee6d4b227126079eb014b691101cb8962a` |
| `reports/03-execucao-alvo-c.md` | 14981 | `b4885af2bc93b6ae3a33f5fd5b35611c17b4aba6f9993d0c3fb7c9be331384e8` |
| `reports/04-validacao-manual-e-limitacoes.md` | 7880 | `11faf435c80407c5caeb787dd356ca70b76ee81bfb77711f1ff7a52c28c06b1d` |
| `reports/05-comparacao-api-pgd-alvo-b.md` | 16027 | `008b4237f1bde43a1e03ea61cfd40695d71fba3a0b7ddadbdc614ff9e56d3396` |
| `reports/06-plano-piloto-adocao.md` | 5293 | `d51a858233be2ee3198e394b94197af46fe33804fcdcb3fa9855ca2b5874ef54` |
| `reports/07-relatorio-final-alvo-b.md` | 23236 | `6f607ba5406e90ebc16866067372a81cdbe921ed5fe4e60383f138192ed538d7` |
| `reports/08-sintese-corpus.md` | 11986 | `e09c94aa119ce119bd9733e6281af154ee05fa29cef14baf5400eb86ae975d5c` |

### Matriz (6 arquivos)

| Arquivo (caminho no pacote) | Tamanho (bytes) | SHA-256 |
|---|---:|---|
| `matrices/cobertura-por-artefato.md` | 7043 | `fb230bf51b81648527c163e170a9e7845fbc10e35ce115116afb136dea1c9ef3` |
| `matrices/estados-por-check-alvo-a.md` | 6745 | `90523ede76b6a4b03805936aff5dd8d1fd6f1d04638ded2242840365d06fc47b` |
| `matrices/estados-por-check-alvo-c.md` | 6762 | `ae9e11215302ed91953fcd0f51456163aa39597a58616fc3300f03791397ea7f` |
| `matrices/mutacoes-e-resultados.md` | 6425 | `728d208d48dfa6b7f9aca4a7776144f6b0cae34c458c7187b5c23925a74034c0` |
| `matrices/pre-triagem-alvo-c.md` | 10112 | `c35b4d8d1b9f86a7b04d827877b02c58fe873630b8f3a502ac34d3bf18759850` |
| `matrices/requisito-check-evidencia-limite.md` | 11124 | `021dcd1fe35acc77c52fb43d3ec075fbd25a04c909e648e413c8d440e918a018` |

### Script (9 arquivos)

| Arquivo (caminho no pacote) | Tamanho (bytes) | SHA-256 |
|---|---:|---|
| `scripts/00_provenance.py` | 3984 | `3dfe746b58d7ef5bc7db60c8047bdd748b73afc71d53d82418f2948a58035061` |
| `scripts/06_sanitizar.py` | 5043 | `22cb565962324ff7d4ccd6e3bbb83c3c106b0f066c98586f9a15e7b4ce0dc304` |
| `scripts/08_mutacoes.py` | 11592 | `cc0161ab42d76fa7fb07dcc1d300c9c6bffcbe9bfa7309ea8ef115574cb95ed8` |
| `scripts/10_analise_revisao.py` | 3404 | `d3909f0f5cf63bb98677da34f02ceb21b05b5addbf63913ae0f8f9cc3b69dfff` |
| `scripts/11_analise_alvo_a.py` | 6218 | `cfa4535db3dee388d07d54ed36ec50defd066236f8e2d84fe544ce01c87ab1af` |
| `scripts/12_sanitizar_alvo_a.py` | 4720 | `8cec0f045e3470e0e89aa07a444aaebfd5f29a8b14bca94d2494092bf7ecb952` |
| `scripts/13_sanitizar_alvo_c.py` | 5109 | `1260ba82d95a877985caeb52cdc20006e83b106f687b8a70fbf4b4d5377539c7` |
| `scripts/14_analise_alvo_c.py` | 7848 | `22d268b1630656d7fbdaf015fdaaecba01d865fb0d19c7531a2e1ace8f4696b6` |
| `scripts/99_fechamento.py` | 13201 | `7cf5a63c8e63714d98858d59e66dfe3887ecf4a3fa7366bb985375cc90b2aaff` |

### README (1 arquivo)

| Arquivo (caminho no pacote) | Tamanho (bytes) | SHA-256 |
|---|---:|---|
| `README.md` | 7135 | `1cd14674615dc99eb5068aba7b32c84b9144c5ded0e467a4e316df594ec9a663` |

### Worklog (1 arquivo)

| Arquivo (caminho no pacote) | Tamanho (bytes) | SHA-256 |
|---|---:|---|
| `worklog.md` | 20099 | `ed3395bc05e1a5cd2d0be6a5afee0aa81d3c387c96633e5034206a5ed7e64f90` |

### Proveniência (1 arquivo)

| Arquivo (caminho no pacote) | Tamanho (bytes) | SHA-256 |
|---|---:|---|
| `evidence/provenance/00-provenance.json` | 11509 | `4d98de149e55a1692135433c286eea17edd527f6fdf2339b869010783f2b0c4d` |

### Laudo sanitizado (6 arquivos)

| Arquivo (caminho no pacote) | Tamanho (bytes) | SHA-256 |
|---|---:|---|
| `evidence/sanitized/laudo-alvo-a-sanitizado.json` | 14087 | `dc7850c70fd918e18447602bbb04894dc88ee00437801b3819459acc8e71532d` |
| `evidence/sanitized/laudo-alvo-b-sanitizado.json` | 18332 | `4942afe81f3aa31b4892d4ed4c456ed1aa4025753cef528913b70197a0df3b0f` |
| `evidence/sanitized/laudo-alvo-c-sanitizado.json` | 24766 | `cf7eb33db4d3dee37d695e850544e37fbed39b6d263ee67433d57a063fd69a6c` |
| `evidence/sanitized/resumo-executivo-laudo.md` | 5533 | `d173ccd399813e7fe266955871f2cadb9f63f481766cd6efda51ea95a768c1b0` |
| `evidence/sanitized/resumo-executivo-laudo-alvo-a.md` | 4903 | `c7cd2bb14b41761086842396194097a9279466437606025fc871f3142cbd398c` |
| `evidence/sanitized/resumo-executivo-laudo-alvo-c.md` | 6855 | `d93b23cb4417236dfa03bc51489a390788519c633811a4f5b3116b6f9eb309b9` |

---

## 4. Verificação cruzada com a proveniência congelada

O arquivo `evidence/provenance/00-provenance.json` (fechado em 2026-08-31T22:43:59Z) registra 32 hashes SHA-256 dos artefatos finais. No empacotamento: (i) 25 hashes foram recalculados e **conferiram exatamente** com os arquivos incluídos neste pacote; (ii) 1 divergência registrada — `reports/00-provenance.md`, **esperada e documentada na própria proveniência** (hash autoreferente, calculado antes do fechamento do próprio arquivo); (iii) 6 hashes restantes correspondem a artefatos brutos de `evidence/raw/` deliberadamente excluídos deste pacote (laudos brutos, logs de comando e resultados de mutações), cuja rastreabilidade permanece garantida pelo próprio arquivo de proveniência (comandos, exit codes e durações). Nenhum artefato foi modificado para acomodar o pacote.

---

## 5. O que NÃO está neste pacote (exclusões de segurança)

Conforme instrução de exportação, o pacote **exclui**:

- **Laudos brutos e logs de execução** (`evidence/raw/` — laudos-alvo-\*-bruto.json, comandos, self-test, pytest, resultados de mutações): material não divulgável, permanece apenas no ambiente de origem;
- **Clones dos cinco repositórios** (`repos/` — pse-suite, project, FastETL, api-pgd, llamafactory): reproduzíveis a partir dos commits congelados da §1;
- **Ambiente virtual** (`.venv-pse/`);
- **Credenciais e arquivos de ambiente** (`.env` e similares) — nenhum segredo real foi incluído; a única string de credencial presente é a **credencial sintética plantada** pela mutação M2 (`sk-live-plantada-…`, `scripts/08_mutacoes.py`), insumo metodológico documentado, sem valor real;
- **Artefatos temporários do workspace** (`tool-results/`, caches, estágios intermediários).

---

## 6. Nota sobre os laudos sanitizados

Os três laudos sanitizados e os três resumos executivos (`evidence/sanitized/`) foram produzidos com **regras idênticas nas três rodadas** (scripts `06`, `12`, `13`): credenciais substituídas por `[REDACTED]`; hosts e URLs apontados pelos achados S-04 mascarados como `[REDACTED-HOST]`; varredura global por literais proibidos antes do fechamento de cada rodada. Os hosts reais correspondentes constam apenas dos laudos brutos, que não integram este pacote. A proveniência dos brutos (hashes, comandos, exit codes) permanece registrada em `evidence/provenance/00-provenance.json` para fins de rastreabilidade.

---

## 7. Resultados canônicos por rodada (referência de citação — números congelados)

| Rodada | Exit | Executados/total | Aplicáveis executados | Pulados | Não habilitados | Indeterminados | Findings | Duração | Partição do catálogo |
|---|---|---|---|---|---|---|---|---|---|
| A (api-pgd) | 11 | 18/58 | 18/29 | 25 | 15 | 0 | 4 (4 ALTO) | 2,44 s | 18+17+23 = 58 |
| B (FastETL) | 11 | 18/58 | 18/29 | 25 | 15 | 0 | 8 (6 ALTO, 2 MÉDIO) | 2,0 s | 18+17+23 = 58 |
| C (LlamaFactory) | 20 | 25/58 | 25/39¹ | 12 | 19 | 2 (E-06, P-15) | 21 (18 ALTO, 3 MÉDIO) | 31,62 s | 25+2+29+2 = 58 |

¹ Denominador inclui os 2 checks indeterminados (extensão declarada *a priori* na análise da rodada C).

**Formulação defensável para citação (conforme parecer):** a igualdade das partições das rodadas A e B (18 executados, 17 não aplicáveis, 23 dependentes de contexto) demonstra **aplicabilidade estrutural semelhante no modo estático**, e não equivalência de maturidade de segurança, privacidade ou governança; o deslocamento da partição na rodada C (25+2+29+2) confirma a interação catálogo×perfil. A métrica mede aplicabilidade do catálogo no recorte estático adotado — não cobertura universal de privacidade, segurança, ética, código ou requisitos legais.

---

## 8. Instruções de reprodução

> Requisitos: Linux x86_64; git; Python 3.12.x. Todos os comandos a partir da raiz do workspace reproduzido (mesma topologia `repos/`, `scripts/`, `evidence/`).

```bash
# 1. Clonar e congelar os cinco repositórios (ordem original do estudo)
git clone https://github.com/danzeroum/pse-suite.git repos/pse-suite
git -C repos/pse-suite checkout 443da92dbdb22a9af18aa6eebb51aac2da901458
git clone https://github.com/danzeroum/project.git repos/project
git -C repos/project checkout 991e2d0f28d746e40a80c89280bdd9060f5a0311
git clone https://github.com/gestaogovbr/FastETL.git repos/FastETL
git -C repos/FastETL checkout 9fb5d596cd8c3d4d0efcf6cdd1ca0c7b5e24afc1
git clone https://github.com/gestaogovbr/api-pgd.git repos/api-pgd
git -C repos/api-pgd checkout 9d4b774cc6763b234372999a1d1c4baf248e3080
git clone https://github.com/hiyouga/LlamaFactory.git repos/llamafactory
git -C repos/llamafactory checkout d6bb97ddff5d752d8b05aa099a168127c7253562

# 2. Ambiente isolado e instalação da suite
python3 -m venv .venv-pse
.venv-pse/bin/pip install -e 'repos/pse-suite[dev]'

# 3. Validação do instrumento — as âncoras devem bater com a §1.1
./.venv-pse/bin/pse --manifesto    # conferir catalog_hash 4682a4ae…a0ac
./.venv-pse/bin/pse --self-test    # 58 mutações canônicas, 0 falhas
cd repos/pse-suite && ../../.venv-pse/bin/python -m pytest -q   # 809 aprovados, 10 pulados
cd ../..

# 4. Rodada B (alvo-b / FastETL)
./.venv-pse/bin/pse --path repos/FastETL --modo pse_inventory \
  --output evidence/raw/laudo-alvo-b-bruto.json
# esperado: exit 11 · ~2,0 s · estados 18/25/15/0 · 8 findings (6 ALTO, 2 MÉDIO)

# 5. Rodada A (alvo-a / API PGD) — re-execução de recuperação
./.venv-pse/bin/pse --path repos/api-pgd --modo pse_inventory \
  --output evidence/raw/laudo-alvo-a-bruto.json
# esperado: exit 11 · ~2,4 s · estados 18/25/15/0 · 4 findings (4 ALTO)

# 6. Rodada C (alvo-c / LlamaFactory)
./.venv-pse/bin/pse --path repos/llamafactory --modo pse_inventory \
  --output evidence/raw/laudo-alvo-c-bruto.json
# esperado: exit 20 · ~31 s · estados 25/12/19/2 · 21 findings (18 ALTO, 3 MÉDIO)

# 7. Sanitização, análise e fechamento (mesma ordem do estudo)
python3 scripts/06_sanitizar.py
python3 scripts/12_sanitizar_alvo_a.py
python3 scripts/13_sanitizar_alvo_c.py
python3 scripts/10_analise_revisao.py
python3 scripts/11_analise_alvo_a.py
python3 scripts/14_analise_alvo_c.py
python3 scripts/99_fechamento.py
```

**Advertências de reprodução:**

1. Durações e timestamps variam entre execuções; findings, estados e cobertura devem reproduzir. Re-execuções determinísticas já foram verificadas nas três rodadas, com divergências apenas de duração/timestamp.
2. As contagens (809/10 testes; 58 mutações canônicas) estão vinculadas ao commit, ao catálogo congelado e ao ambiente registrados na proveniência — não são propriedades permanentes do produto.
3. Se o `catalog_hash` da sua instalação divergir de `4682a4ae…a0ac`, os resultados NÃO são comparáveis aos deste corpus (ameaça à comparabilidade — relatório 05, §5).
4. A rodada A é **reexecução de recuperação** (emenda de protocolo declarada) e deve ser citada como tal; a rodada C depende da pré-triagem pré-registrada (`matrices/pre-triagem-alvo-c.md`) para justificar a seleção do alvo.
5. Os scripts de sanitização (06/12/13) exigem os laudos brutos correspondentes em `evidence/raw/` — que não integram este pacote por serem não divulgáveis; em ambiente de reprodução, os brutos são gerados pelos comandos das etapas 4–6.

---

## 9. Notas finais

- Este manifesto não inclui o hash de si mesmo (autoreferência); todos os demais arquivos do pacote estão tabelados na §3.
- O worklog incluído (`worklog.md`) registra o histórico completo de execução e revisões (v1 → v2 → v3 → v3.1) do corpus.
- Regra de congelamento preservada: nenhum artefato listado aqui foi alterado durante o empacotamento (cópia binária com `copy2`; cross-check da §4 executado somente para leitura).
- Pacote gerado pelo script `empacotar_final.py` (whitelist explícita + verificação de arquivos extras + cross-check de proveniência), mantido fora do pacote por ser instrumental ao export, não ao corpus.
