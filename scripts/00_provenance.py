#!/usr/bin/env python3
"""Fase 1 - Congelamento e proveniencia do estudo TPF PSE Suite x FastETL.

Gera:
  evidence/provenance/00-provenance.json
  reports/00-provenance.md

Somente leitura local. Nenhuma rede. Nenhum servico.
"""
import json
import hashlib
import subprocess
import datetime
import os
import sys

BASE = "/home/z/my-project/tpf-pse-fastetl"
REPOS = ["pse-suite", "project", "FastETL"]


def sh(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return r.stdout.strip(), r.returncode


def repo_info(name):
    p = os.path.join(BASE, "repos", name)
    url, _ = sh(f"git remote get-url origin", cwd=p)
    branch, _ = sh(f"git rev-parse --abbrev-ref HEAD", cwd=p)
    sha, _ = sh(f"git rev-parse HEAD", cwd=p)
    date, _ = sh(f"git log -1 --format=%cI", cwd=p)
    tag, _ = sh(f"git describe --tags 2>/dev/null || echo null", cwd=p)
    ncommits, _ = sh(f"git rev-list --count HEAD", cwd=p)
    return {
        "repositorio": name,
        "url": url,
        "branch": branch,
        "sha_completo": sha,
        "data_hora_utc_commit": date,
        "tag_descritiva": None if tag == "null" else tag,
        "commits_no_clone": int(ncommits),
    }


def main():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    prov = {
        "estudo": "TPF PSE Suite x FastETL - rodada 2 (perfil engenharia de dados/Airflow)",
        "modo": "avaliacao exploratoria, estatica e somente leitura",
        "gerado_em_utc": now,
        "repositorios": [repo_info(r) for r in REPOS],
        "ambiente": {
            "so": "Debian GNU/Linux 13 (trixie)",
            "arquitetura": "x86_64",
            "kernel": "5.10.134-013.8.3.kangaroo.al8.x86_64",
            "git": subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip(),
            "python": sys.version.split()[0],
            "pip": "25.0.1",
            "venv": os.path.join(BASE, ".venv-pse"),
        },
        "pse_suite": {
            "suite_version": None,
            "schema_version": None,
            "catalog_hash": None,
            "nota": "preenchido apos instalacao em venv isolado (ver 01-execucao)",
        },
        "comandos": [],
        "hashes_sha256_relatorios_finais": {},
    }
    os.makedirs(os.path.join(BASE, "evidence", "provenance"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "reports"), exist_ok=True)
    with open(os.path.join(BASE, "evidence", "provenance", "00-provenance.json"), "w") as f:
        json.dump(prov, f, indent=2, ensure_ascii=False)

    md = ["# Proveniência do estudo — TPF PSE Suite × FastETL", "",
          "Avaliação exploratória, estática e somente leitura. Clones locais congelados por SHA.",
          "", f"Registro gerado em: **{now}**", "",
          "## Repositórios", "",
          "| Repositório | URL | Branch | SHA completo | Data/hora UTC (commit) | Tag |",
          "|---|---|---|---|---|---|"]
    for r in prov["repositorios"]:
        md.append(f"| {r['repositorio']} | {r['url']} | {r['branch']} | `{r['sha_completo']}` | {r['data_hora_utc_commit']} | {r['tag_descritiva'] or '—'} |")
    a = prov["ambiente"]
    md += ["", "## Ambiente", "",
           f"- SO: {a['so']} | Arquitetura: {a['arquitetura']}",
           f"- Kernel: {a['kernel']}",
           f"- Git: {a['git']}",
           f"- Python: {a['python']} | pip: {a['pip']}",
           f"- venv isolado: {a['venv']}",
           "", "## Regras de congelamento", "",
           "- Nenhum commit será trocado/atualizado após o início do estudo.",
           "- Toda execução de ferramenta registra comando exato, código de saída e duração.",
           "- Relatórios finais recebem hash SHA-256 registrado nesta proveniência.",
           ""]
    with open(os.path.join(BASE, "reports", "00-provenance.md"), "w") as f:
        f.write("\n".join(md))
    print("OK provenance written")


if __name__ == "__main__":
    main()
