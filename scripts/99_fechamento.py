#!/usr/bin/env python3
"""Fechamento: completa proveniencia (suite, comandos, hashes) e gera README."""
import json
import hashlib
import datetime
import os

BASE = "/home/z/my-project/tpf-pse-fastetl"
PROV = f"{BASE}/evidence/provenance/00-provenance.json"
PROVMD = f"{BASE}/reports/00-provenance.md"

COMANDOS = [
    {"fase": "0", "comando": "git clone --depth 50 https://github.com/danzeroum/pse-suite.git", "exit": 0},
    {"fase": "0", "comando": "git clone --depth 50 https://github.com/danzeroum/project.git", "exit": 0},
    {"fase": "0", "comando": "git clone --depth 50 https://github.com/gestaogovbr/FastETL.git", "exit": 0},
    {"fase": "0", "comando": "git fetch --unshallow --tags (conversao para historico completo)", "exit": 0},
    {"fase": "2", "comando": "python3 -m venv .venv-pse && pip install -e 'repos/pse-suite[dev]'", "exit": 0},
    {"fase": "2", "comando": "./.venv-pse/bin/pse --manifesto", "exit": 0, "dur_s": None, "artefato": "evidence/raw/manifesto-pse.txt"},
    {"fase": "2", "comando": "./.venv-pse/bin/pse --self-test", "exit": 0, "artefato": "evidence/raw/self-test.txt"},
    {"fase": "2", "comando": ".venv-pse/bin/python -m pytest -q (em repos/pse-suite)", "exit": 0,
     "dur_s": 157.78, "artefato": "evidence/raw/pytest-pse-suite.txt", "nota": "809 passaram, 10 puladas"},
    {"fase": "6", "comando": "./.venv-pse/bin/pse --path repos/FastETL --modo pse_inventory --output evidence/raw/laudo-alvo-b-bruto.json",
     "exit": 11, "dur_s": 2.0, "artefato": "evidence/raw/laudo-alvo-b-bruto.json",
     "nota": "exit 11 = violacao com ALTO sem CRITICO (semantica da suite, nao juridica); re-execucao deterministica (v2) apos padronizacao de nomenclatura — findings/estados/cobertura identicos; exec original: dur 2.07s"},
    {"fase": "6", "comando": "python3 scripts/06_sanitizar.py", "exit": 0, "artefato": "evidence/sanitized/laudo-alvo-b-sanitizado.json"},
    {"fase": "8", "comando": "python3 scripts/08_mutacoes.py (8 mutacoes, copias descartaveis)",
     "exit": 0, "artefato": "evidence/raw/mutacoes-resultados.json",
     "nota": "M1 exit 10; M2 exit 10; M3/M4/M5/M8 exit 11; M6 exit 20; M7a exit 0; M7b exit 1"},
    {"fase": "10-a", "comando": "git clone https://github.com/gestaogovbr/api-pgd.git repos/api-pgd (recuperacao da rodada A — emenda de protocolo declarada no relatorio 05)",
     "exit": 0,
     "nota": "alvo congelado imediatamente apos o clone: 9d4b774cc6763b234372999a1d1c4baf248e3080 (tag 3.3.10, 1396 commits)"},
    {"fase": "10-a", "comando": "./.venv-pse/bin/pse --path repos/api-pgd --modo pse_inventory --output evidence/raw/laudo-alvo-a-bruto.json",
     "exit": 11, "dur_s": 2.44, "artefato": "evidence/raw/laudo-alvo-a-bruto.json",
     "nota": "rodada A recuperada por re-execucao local com a mesma instrumentacao da rodada B (suite 0.20.0, mesmo catalog_hash, mesmo venv); estados 18/25/15/0; 4 findings (4 ALTO); particao 18+17+23=58"},
    {"fase": "10-a", "comando": "python3 scripts/12_sanitizar_alvo_a.py", "exit": 0,
     "artefato": "evidence/sanitized/laudo-alvo-a-sanitizado.json",
     "nota": "mesmas regras de sanitizacao da rodada B; hosts apontados por S-04 mascarados como [REDACTED-HOST]"},
    {"fase": "10-b", "comando": "git clone https://github.com/hiyouga/LlamaFactory.git repos/llamafactory (rodada C — emenda de protocolo n.2 declarada no relatorio 03-execucao-alvo-c)",
     "exit": 0,
     "nota": "quinto clone publico; alvo de IA selecionado por pre-triagem pre-registrada (matrices/pre-triagem-alvo-c.md); congelado imediatamente apos o clone: d6bb97ddff5d752d8b05aa099a168127c7253562 (main, 3097 commits)"},
    {"fase": "10-b", "comando": "./.venv-pse/bin/pse --path repos/llamafactory --modo pse_inventory --output evidence/raw/laudo-alvo-c-bruto.json",
     "exit": 20, "dur_s": 31.62, "artefato": "evidence/raw/laudo-alvo-c-bruto.json",
     "nota": "rodada C (alvo de IA): veredito indeterminado — 2 checks (E-06, P-15) sem substrato para decidir; pack de etica EM ESCOPO por fato computado; estados 25/12/19/2; 21 findings (18 ALTO, 3 MEDIO); particao 25+2+29+2=58; re-execucao deterministica verificada (~30,8s, divergencias apenas duracao/timestamp)"},
    {"fase": "10-b", "comando": "python3 scripts/13_sanitizar_alvo_c.py", "exit": 0,
     "artefato": "evidence/sanitized/laudo-alvo-c-sanitizado.json",
     "nota": "mesmas regras de sanitizacao das rodadas A/B; 12 hosts apontados por S-04 mascarados como [REDACTED-HOST]"},
    {"fase": "10-b", "comando": "python3 scripts/14_analise_alvo_c.py", "exit": 0,
     "artefato": "matrices/estados-por-check-alvo-c.md",
     "nota": "indicadores do parecer com duas extensoes declaradas a priori (particao quadripartida com estado indeterminado proprio; forma de motivo do E-12 como vetor estrutural); assercao de particao OK"},
]

ARTEFATOS = [
    "reports/00-provenance.md",
    "reports/01-caracterizacao-pse-suite.md",
    "reports/02-caracterizacao-alvo-b.md",
    "reports/03-execucao-alvo-b.md",
    "reports/04-validacao-manual-e-limitacoes.md",
    "reports/02-caracterizacao-alvo-a.md",
    "reports/03-execucao-alvo-a.md",
    "matrices/estados-por-check-alvo-a.md",
    "reports/05-comparacao-api-pgd-alvo-b.md",
    "reports/06-plano-piloto-adocao.md",
    "reports/07-relatorio-final-alvo-b.md",
    "matrices/cobertura-por-artefato.md",
    "matrices/mutacoes-e-resultados.md",
    "matrices/requisito-check-evidencia-limite.md",
    "evidence/sanitized/laudo-alvo-b-sanitizado.json",
    "evidence/sanitized/resumo-executivo-laudo.md",
    "evidence/sanitized/laudo-alvo-a-sanitizado.json",
    "evidence/sanitized/resumo-executivo-laudo-alvo-a.md",
    "evidence/raw/laudo-alvo-b-bruto.json",
    "evidence/raw/laudo-alvo-a-bruto.json",
    "evidence/raw/comando-inventory-alvo-a.txt",
    "evidence/raw/mutacoes-resultados.json",
    "matrices/pre-triagem-alvo-c.md",
    "reports/02-caracterizacao-alvo-c.md",
    "reports/03-execucao-alvo-c.md",
    "matrices/estados-por-check-alvo-c.md",
    "evidence/raw/laudo-alvo-c-bruto.json",
    "evidence/raw/comando-inventory-alvo-c.txt",
    "evidence/sanitized/laudo-alvo-c-sanitizado.json",
    "evidence/sanitized/resumo-executivo-laudo-alvo-c.md",
    "reports/08-sintese-corpus.md",
    "README.md",
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    prov = json.load(open(PROV))
    # Rodada A recuperada por re-execucao local (emenda de protocolo — relatorio 05, §1):
    # registro do quarto clone na proveniencia, mantendo os tres originais intactos.
    repos_nomes = {r["repositorio"] for r in prov["repositorios"]}
    if "api-pgd" not in repos_nomes:
        prov["repositorios"].append({
            "repositorio": "api-pgd",
            "url": "https://github.com/gestaogovbr/api-pgd.git",
            "branch": "main",
            "sha_completo": "9d4b774cc6763b234372999a1d1c4baf248e3080",
            "data_hora_utc_commit": "2026-07-07T17:12:42-03:00",
            "tag_descritiva": "3.3.10",
            "commits_no_clone": 1396,
            "origem": "emenda de protocolo: recuperacao da rodada A por re-execucao local (relatorio 05, §1)",
        })
    repos_nomes2 = {r["repositorio"] for r in prov["repositorios"]}
    if "llamafactory" not in repos_nomes2:
        prov["repositorios"].append({
            "repositorio": "llamafactory",
            "url": "https://github.com/hiyouga/LlamaFactory.git",
            "branch": "main",
            "sha_completo": "d6bb97ddff5d752d8b05aa099a168127c7253562",
            "data_hora_utc_commit": "2026-08-31T16:13:06+08:00",
            "tag_descritiva": None,
            "commits_no_clone": 3097,
            "origem": "emenda de protocolo n.2: rodada C (alvo de IA) apos pre-triagem pre-registrada (matrices/pre-triagem-alvo-c.md)",
        })
    prov["pse_suite"] = {
        "suite_version": "0.20.0",
        "schema_version": "laudo-pse-1.0",
        "catalog_hash": "4682a4ae1115e577e95e2ddbd666bfd041efb2fca4b3d77e7683e2055571a0ac",
        "instalacao": "venv isolado .venv-pse (pip install -e repos/pse-suite[dev])",
        "autoprova": "OK - 58 mutacoes canonicas, 0 falhas; E-06 indeterminado na fixture (esperado)",
        "testes_oficiais": "809 passaram, 10 puladas (8 Playwright ausente; 2 aceite btv ausente) - Python 3.12.14",
    }
    prov["comandos"] = COMANDOS
    hashes = {}
    for rel in ARTEFATOS:
        p = os.path.join(BASE, rel)
        if os.path.exists(p):
            hashes[rel] = sha256(p)
    prov["hashes_sha256_relatorios_finais"] = hashes
    prov["fechado_em_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump(prov, open(PROV, "w"), indent=2, ensure_ascii=False)

    md = ["# Proveniência do estudo — TPF PSE Suite × FastETL", "",
          "Avaliação exploratória, estática e somente leitura. Clones locais congelados por SHA.",
          "**Revisão v2:** nomenclatura dos anexos padronizada para nomes neutros (`alvo-b`), conforme parecer da orientação; "
          "o laudo do inventário foi re-executado de forma determinística (mesmo comando, commit, suite e `catalog_hash`) "
          "e a sanitização refeita; grafia do nome do projeto corrigida em toda a documentação (FastETL).",
          "**Revisão v3:** atenções finais do parecer aplicadas — nota metodológica formal dos quatro indicadores de cobertura "
          "com regra de classificação de precedência declarada e verificação de partição (relatório 07, §10.1); precisão das "
          "contagens de testes e mutações (associadas ao commit, catálogo e ambiente congelados); rodada A (API PGD) recuperada "
          "por re-execução local com a mesma instrumentação congelada (emenda de protocolo declarada — quarto clone), habilitando "
          "a comparação A × B executada com paridade de proveniência (relatório 05).",
          "**Revisão v3.1 (pós-parecer + rodada C):** notas de interpretação do parecer da v3 incorporadas ao corpus (formulação "
          "defensável da partição e complemento da métrica — relatórios 05 §2.1 e 07 §10.1/§11); rodada C executada sobre alvo "
          "de IA (LlamaFactory @ d6bb97d, emenda de protocolo n.2 — quinto clone) com pré-triagem pré-registrada; síntese do "
          "corpus A × B × C no relatório 08.",
          "", f"**Fechamento:** {prov['fechado_em_utc']}", "",
          "## Repositórios", "",
          "| Repositório | URL | Branch | SHA completo | Data/hora UTC (commit) | Tag descritiva |",
          "|---|---|---|---|---|---|"]
    for r in prov["repositorios"]:
        md.append(f"| {r['repositorio']} | {r['url']} | {r['branch']} | `{r['sha_completo']}` | {r['data_hora_utc_commit']} | {r['tag_descritiva'] or '—'} |")
    a = prov["ambiente"]
    md += ["", "## Ambiente", "",
           f"- SO: {a['so']} · Arquitetura: {a['arquitetura']} · Kernel: {a['kernel']}",
           f"- Git: {a['git']} · Python: {a['python']} · pip: {a['pip']} · venv: `.venv-pse`",
           "", "## PSE Suite instalada", "",
           f"- suite_version: **{prov['pse_suite']['suite_version']}** · schema: `{prov['pse_suite']['schema_version']}`",
           f"- catalog_hash: `{prov['pse_suite']['catalog_hash']}`",
           f"- Autoprova: {prov['pse_suite']['autoprova']}",
           f"- Testes oficiais: {prov['pse_suite']['testes_oficiais']}",
           "", "## Comandos executados", "",
           "| Fase | Comando | Exit | Duração | Artefato | Nota |",
           "|---|---|---|---|---|---|"]
    for c in COMANDOS:
        md.append(f"| {c['fase']} | `{c['comando']}` | {c['exit']} | {c.get('dur_s') or '—'} | {c.get('artefato') or '—'} | {c.get('nota', '')} |")
    md += ["", "## Hashes SHA-256 dos anexos finais", "",
           "| Artefato | SHA-256 |", "|---|---|"]
    for rel, h in hashes.items():
        md.append(f"| `{rel}` | `{h}` |")
    md += ["", "Nota: o hash de `reports/00-provenance.md` é autoreferente (calculado antes do fechamento do próprio arquivo) e refere-se à versão anterior deste documento; os demais hashes são definitivos.", ""]
    md += ["", "## Regras de congelamento", "",
           "- Nenhum commit foi trocado/atualizado após o início (`git status --porcelain` vazio nos clones ao final).",
           "- O clone do alvo A (`api-pgd`) foi acrescentado por emenda de protocolo declarada (relatório 05, §1) e congelado imediatamente após o clone.",
           "- O clone do alvo C (`llamafactory`) foi acrescentado por emenda de protocolo nº 2 (relatório 03-execucao-alvo-c), com pré-triagem pré-registrada antes da enumeração final de candidatos, e congelado imediatamente após o clone.",
           "- Toda execução registrou comando, código de saída e duração.",
           "- Laudo bruto permanece em `evidence/raw/` (não divulgar); material divulgável apenas em `evidence/sanitized/` e `reports/`.", ""]
    open(PROVMD, "w").write("\n".join(md))
    print("OK proveniencia fechada com", len(hashes), "hashes")


if __name__ == "__main__":
    main()
