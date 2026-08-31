# Proveniência do estudo — TPF PSE Suite × FastETL

Avaliação exploratória, estática e somente leitura. Clones locais congelados por SHA.
**Revisão v2:** nomenclatura dos anexos padronizada para nomes neutros (`alvo-b`), conforme parecer da orientação; o laudo do inventário foi re-executado de forma determinística (mesmo comando, commit, suite e `catalog_hash`) e a sanitização refeita; grafia do nome do projeto corrigida em toda a documentação (FastETL).
**Revisão v3:** atenções finais do parecer aplicadas — nota metodológica formal dos quatro indicadores de cobertura com regra de classificação de precedência declarada e verificação de partição (relatório 07, §10.1); precisão das contagens de testes e mutações (associadas ao commit, catálogo e ambiente congelados); rodada A (API PGD) recuperada por re-execução local com a mesma instrumentação congelada (emenda de protocolo declarada — quarto clone), habilitando a comparação A × B executada com paridade de proveniência (relatório 05).
**Revisão v3.1 (pós-parecer + rodada C):** notas de interpretação do parecer da v3 incorporadas ao corpus (formulação defensável da partição e complemento da métrica — relatórios 05 §2.1 e 07 §10.1/§11); rodada C executada sobre alvo de IA (LlamaFactory @ d6bb97d, emenda de protocolo n.2 — quinto clone) com pré-triagem pré-registrada; síntese do corpus A × B × C no relatório 08.

**Fechamento:** 2026-08-31T22:43:59Z

## Repositórios

| Repositório | URL | Branch | SHA completo | Data/hora UTC (commit) | Tag descritiva |
|---|---|---|---|---|---|
| pse-suite | https://github.com/danzeroum/pse-suite.git | main | `443da92dbdb22a9af18aa6eebb51aac2da901458` | 2026-08-17T17:23:21-03:00 | v0.3.0-53-g443da92 |
| project | https://github.com/danzeroum/project.git | main | `991e2d0f28d746e40a80c89280bdd9060f5a0311` | 2026-08-31T14:06:17Z | — |
| FastETL | https://github.com/gestaogovbr/FastETL.git | main | `9fb5d596cd8c3d4d0efcf6cdd1ca0c7b5e24afc1` | 2026-04-29T16:19:31-03:00 | 0.2.14-3-g9fb5d59 |
| api-pgd | https://github.com/gestaogovbr/api-pgd.git | main | `9d4b774cc6763b234372999a1d1c4baf248e3080` | 2026-07-07T17:12:42-03:00 | 3.3.10 |
| llamafactory | https://github.com/hiyouga/LlamaFactory.git | main | `d6bb97ddff5d752d8b05aa099a168127c7253562` | 2026-08-31T16:13:06+08:00 | — |

## Ambiente

- SO: Debian GNU/Linux 13 (trixie) · Arquitetura: x86_64 · Kernel: 5.10.134-013.8.3.kangaroo.al8.x86_64
- Git: git version 2.47.3 · Python: 3.12.14 · pip: 25.0.1 · venv: `.venv-pse`

## PSE Suite instalada

- suite_version: **0.20.0** · schema: `laudo-pse-1.0`
- catalog_hash: `4682a4ae1115e577e95e2ddbd666bfd041efb2fca4b3d77e7683e2055571a0ac`
- Autoprova: OK - 58 mutacoes canonicas, 0 falhas; E-06 indeterminado na fixture (esperado)
- Testes oficiais: 809 passaram, 10 puladas (8 Playwright ausente; 2 aceite btv ausente) - Python 3.12.14

## Comandos executados

| Fase | Comando | Exit | Duração | Artefato | Nota |
|---|---|---|---|---|---|
| 0 | `git clone --depth 50 https://github.com/danzeroum/pse-suite.git` | 0 | — | — |  |
| 0 | `git clone --depth 50 https://github.com/danzeroum/project.git` | 0 | — | — |  |
| 0 | `git clone --depth 50 https://github.com/gestaogovbr/FastETL.git` | 0 | — | — |  |
| 0 | `git fetch --unshallow --tags (conversao para historico completo)` | 0 | — | — |  |
| 2 | `python3 -m venv .venv-pse && pip install -e 'repos/pse-suite[dev]'` | 0 | — | — |  |
| 2 | `./.venv-pse/bin/pse --manifesto` | 0 | — | evidence/raw/manifesto-pse.txt |  |
| 2 | `./.venv-pse/bin/pse --self-test` | 0 | — | evidence/raw/self-test.txt |  |
| 2 | `.venv-pse/bin/python -m pytest -q (em repos/pse-suite)` | 0 | 157.78 | evidence/raw/pytest-pse-suite.txt | 809 passaram, 10 puladas |
| 6 | `./.venv-pse/bin/pse --path repos/FastETL --modo pse_inventory --output evidence/raw/laudo-alvo-b-bruto.json` | 11 | 2.0 | evidence/raw/laudo-alvo-b-bruto.json | exit 11 = violacao com ALTO sem CRITICO (semantica da suite, nao juridica); re-execucao deterministica (v2) apos padronizacao de nomenclatura — findings/estados/cobertura identicos; exec original: dur 2.07s |
| 6 | `python3 scripts/06_sanitizar.py` | 0 | — | evidence/sanitized/laudo-alvo-b-sanitizado.json |  |
| 8 | `python3 scripts/08_mutacoes.py (8 mutacoes, copias descartaveis)` | 0 | — | evidence/raw/mutacoes-resultados.json | M1 exit 10; M2 exit 10; M3/M4/M5/M8 exit 11; M6 exit 20; M7a exit 0; M7b exit 1 |
| 10-a | `git clone https://github.com/gestaogovbr/api-pgd.git repos/api-pgd (recuperacao da rodada A — emenda de protocolo declarada no relatorio 05)` | 0 | — | — | alvo congelado imediatamente apos o clone: 9d4b774cc6763b234372999a1d1c4baf248e3080 (tag 3.3.10, 1396 commits) |
| 10-a | `./.venv-pse/bin/pse --path repos/api-pgd --modo pse_inventory --output evidence/raw/laudo-alvo-a-bruto.json` | 11 | 2.44 | evidence/raw/laudo-alvo-a-bruto.json | rodada A recuperada por re-execucao local com a mesma instrumentacao da rodada B (suite 0.20.0, mesmo catalog_hash, mesmo venv); estados 18/25/15/0; 4 findings (4 ALTO); particao 18+17+23=58 |
| 10-a | `python3 scripts/12_sanitizar_alvo_a.py` | 0 | — | evidence/sanitized/laudo-alvo-a-sanitizado.json | mesmas regras de sanitizacao da rodada B; hosts apontados por S-04 mascarados como [REDACTED-HOST] |
| 10-b | `git clone https://github.com/hiyouga/LlamaFactory.git repos/llamafactory (rodada C — emenda de protocolo n.2 declarada no relatorio 03-execucao-alvo-c)` | 0 | — | — | quinto clone publico; alvo de IA selecionado por pre-triagem pre-registrada (matrices/pre-triagem-alvo-c.md); congelado imediatamente apos o clone: d6bb97ddff5d752d8b05aa099a168127c7253562 (main, 3097 commits) |
| 10-b | `./.venv-pse/bin/pse --path repos/llamafactory --modo pse_inventory --output evidence/raw/laudo-alvo-c-bruto.json` | 20 | 31.62 | evidence/raw/laudo-alvo-c-bruto.json | rodada C (alvo de IA): veredito indeterminado — 2 checks (E-06, P-15) sem substrato para decidir; pack de etica EM ESCOPO por fato computado; estados 25/12/19/2; 21 findings (18 ALTO, 3 MEDIO); particao 25+2+29+2=58; re-execucao deterministica verificada (~30,8s, divergencias apenas duracao/timestamp) |
| 10-b | `python3 scripts/13_sanitizar_alvo_c.py` | 0 | — | evidence/sanitized/laudo-alvo-c-sanitizado.json | mesmas regras de sanitizacao das rodadas A/B; 12 hosts apontados por S-04 mascarados como [REDACTED-HOST] |
| 10-b | `python3 scripts/14_analise_alvo_c.py` | 0 | — | matrices/estados-por-check-alvo-c.md | indicadores do parecer com duas extensoes declaradas a priori (particao quadripartida com estado indeterminado proprio; forma de motivo do E-12 como vetor estrutural); assercao de particao OK |

## Hashes SHA-256 dos anexos finais

| Artefato | SHA-256 |
|---|---|
| `reports/00-provenance.md` | `a533596471e71f64bab64fbd7b95d4dd62b129d87f099dd5328d5bfeaeb75bfc` |
| `reports/01-caracterizacao-pse-suite.md` | `5fdc8dd14add81d26b775cc44ef2b15727788098ce218eb47eb1ec5882a771f1` |
| `reports/02-caracterizacao-alvo-b.md` | `ddd087c9ce2eca6730a529424a074fccd923d07271c67a74d65e3bfa79a36af8` |
| `reports/03-execucao-alvo-b.md` | `6d06bf1bec193a1e116fd4d33eacfaee6d4b227126079eb014b691101cb8962a` |
| `reports/04-validacao-manual-e-limitacoes.md` | `11faf435c80407c5caeb787dd356ca70b76ee81bfb77711f1ff7a52c28c06b1d` |
| `reports/02-caracterizacao-alvo-a.md` | `f5b4471f002fa5bb03bf88214ea5d2af2c4205e94492b9e50c8757fd280e93bc` |
| `reports/03-execucao-alvo-a.md` | `336b6f7689933fa2351156652d7b1118a1744b6747984236697f175291164ec1` |
| `matrices/estados-por-check-alvo-a.md` | `90523ede76b6a4b03805936aff5dd8d1fd6f1d04638ded2242840365d06fc47b` |
| `reports/05-comparacao-api-pgd-alvo-b.md` | `008b4237f1bde43a1e03ea61cfd40695d71fba3a0b7ddadbdc614ff9e56d3396` |
| `reports/06-plano-piloto-adocao.md` | `d51a858233be2ee3198e394b94197af46fe33804fcdcb3fa9855ca2b5874ef54` |
| `reports/07-relatorio-final-alvo-b.md` | `6f607ba5406e90ebc16866067372a81cdbe921ed5fe4e60383f138192ed538d7` |
| `matrices/cobertura-por-artefato.md` | `fb230bf51b81648527c163e170a9e7845fbc10e35ce115116afb136dea1c9ef3` |
| `matrices/mutacoes-e-resultados.md` | `728d208d48dfa6b7f9aca4a7776144f6b0cae34c458c7187b5c23925a74034c0` |
| `matrices/requisito-check-evidencia-limite.md` | `021dcd1fe35acc77c52fb43d3ec075fbd25a04c909e648e413c8d440e918a018` |
| `evidence/sanitized/laudo-alvo-b-sanitizado.json` | `4942afe81f3aa31b4892d4ed4c456ed1aa4025753cef528913b70197a0df3b0f` |
| `evidence/sanitized/resumo-executivo-laudo.md` | `d173ccd399813e7fe266955871f2cadb9f63f481766cd6efda51ea95a768c1b0` |
| `evidence/sanitized/laudo-alvo-a-sanitizado.json` | `dc7850c70fd918e18447602bbb04894dc88ee00437801b3819459acc8e71532d` |
| `evidence/sanitized/resumo-executivo-laudo-alvo-a.md` | `c7cd2bb14b41761086842396194097a9279466437606025fc871f3142cbd398c` |
| `evidence/raw/laudo-alvo-b-bruto.json` | `7201c25c0bfd8afa6555cd5a983413d36806afad12ae336d4c541a0517f1a61d` |
| `evidence/raw/laudo-alvo-a-bruto.json` | `9242263a6cf7bf1759edd0e5e1adf535c9cab9fed028646fb8dc47a9f64d1c3e` |
| `evidence/raw/comando-inventory-alvo-a.txt` | `ede1f4bfed6bad9ee449dcabc81ee05c8438af4b8009ab7bf206c845f1975e2b` |
| `evidence/raw/mutacoes-resultados.json` | `5b4983c580959313b5d9530f62226dfd6487b74ba99229649657ea9ea670783b` |
| `matrices/pre-triagem-alvo-c.md` | `c35b4d8d1b9f86a7b04d827877b02c58fe873630b8f3a502ac34d3bf18759850` |
| `reports/02-caracterizacao-alvo-c.md` | `2acdcc0960bc0267bed27708c42c9ac3ceb9efc8012996f0023cc8ec91652d96` |
| `reports/03-execucao-alvo-c.md` | `b4885af2bc93b6ae3a33f5fd5b35611c17b4aba6f9993d0c3fb7c9be331384e8` |
| `matrices/estados-por-check-alvo-c.md` | `ae9e11215302ed91953fcd0f51456163aa39597a58616fc3300f03791397ea7f` |
| `evidence/raw/laudo-alvo-c-bruto.json` | `81999d73fc0c5c4dc78c971215e82b4da4754cddbd0760084b8c5987045d6259` |
| `evidence/raw/comando-inventory-alvo-c.txt` | `ea0bb90ec2a7ba2c6d90db82fade6b162589a50566657ea818e927b11ebf3c55` |
| `evidence/sanitized/laudo-alvo-c-sanitizado.json` | `cf7eb33db4d3dee37d695e850544e37fbed39b6d263ee67433d57a063fd69a6c` |
| `evidence/sanitized/resumo-executivo-laudo-alvo-c.md` | `d93b23cb4417236dfa03bc51489a390788519c633811a4f5b3116b6f9eb309b9` |
| `reports/08-sintese-corpus.md` | `e09c94aa119ce119bd9733e6281af154ee05fa29cef14baf5400eb86ae975d5c` |
| `README.md` | `1cd14674615dc99eb5068aba7b32c84b9144c5ded0e467a4e316df594ec9a663` |

Nota: o hash de `reports/00-provenance.md` é autoreferente (calculado antes do fechamento do próprio arquivo) e refere-se à versão anterior deste documento; os demais hashes são definitivos.


## Regras de congelamento

- Nenhum commit foi trocado/atualizado após o início (`git status --porcelain` vazio nos clones ao final).
- O clone do alvo A (`api-pgd`) foi acrescentado por emenda de protocolo declarada (relatório 05, §1) e congelado imediatamente após o clone.
- O clone do alvo C (`llamafactory`) foi acrescentado por emenda de protocolo nº 2 (relatório 03-execucao-alvo-c), com pré-triagem pré-registrada antes da enumeração final de candidatos, e congelado imediatamente após o clone.
- Toda execução registrou comando, código de saída e duração.
- Laudo bruto permanece em `evidence/raw/` (não divulgar); material divulgável apenas em `evidence/sanitized/` e `reports/`.
