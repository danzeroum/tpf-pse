#!/usr/bin/env python3
"""Fase 8 - Mutacoes controladas (maximo 8) sobre copias descartaveis.

Nao altera o clone original do FastETL nem o clone da PSE Suite:
cada mutacao usa copia fresca descartavel criada aqui.
Apenas mutacoes dentro do escopo declarado do check mutado.
"""
import json
import os
import shutil
import subprocess
import time
import datetime

BASE = "/home/z/my-project/tpf-pse-fastetl"
SRC_FETL = f"{BASE}/repos/FastETL"
SRC_PSE = f"{BASE}/repos/pse-suite"
VENV_PSE = f"{BASE}/.venv-pse/bin/pse"
WORK = f"{BASE}/evidence/raw/mutacoes"
OUT = f"{BASE}/evidence/raw/mutacoes-resultados.json"

# CPF sintetico OBVIAMENTE invalido (sequencia de digitos repetidos) - nenhum titular real
CPF_SINTETICO = "111.222.333-44"


def copia_fresca(nome):
    dst = os.path.join(WORK, nome)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(SRC_FETL, dst,
                    ignore=shutil.ignore_patterns(".git", "__pycache__"))
    return dst


def rodar_pse(alvo, config=None):
    out = os.path.join(WORK, "laudo-mutacao.json")
    cmd = [VENV_PSE, "--path", alvo, "--modo", "pse_inventory", "--output", out]
    if config:
        cmd += ["--config", config]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    dur = round(time.time() - t0, 2)
    dados = None
    if os.path.exists(out):
        with open(out) as f:
            dados = json.load(f)
        os.remove(out)
    return {"exit": r.returncode, "dur_s": dur, "cmd": " ".join(cmd),
            "stderr_tail": r.stderr.strip()[-200:], "laudo": dados}


def resumo(laudo):
    if not laudo:
        return {}
    return {
        "exit_code": laudo.get("exit_code"),
        "findings": [{"check": f["check_id"], "sev": f["severidade"],
                      "arq": f["arquivo"], "linha": f["linha"]} for f in laudo.get("findings", [])],
        "executados": sorted(laudo.get("checks_executados", [])),
        "pulados": sorted([p["id"] for p in laudo.get("checks_pulados", [])]),
        "indeterminados": len(laudo.get("checks_indeterminados", [])),
        "fora_de_alcance": laudo.get("alcance", {}).get("arquivos_fora_de_alcance"),
        "fora_escopo_packs": [p.get("pack") for p in laudo.get("packs_fora_de_escopo", [])],
    }


def main():
    os.makedirs(WORK, exist_ok=True)
    resultados = []

    # ---------- M1: PII sintetica em log (P-01) ----------
    d = copia_fresca("m01")
    p = os.path.join(d, "fastetl", "mut_m01_log.py")
    with open(p, "w") as f:
        f.write("import logging\nlogger = logging.getLogger(__name__)\n\n"
                "def mutacao(cpf):\n"
                f"    logger.info(\"cadastro cpf=%s\", \"{CPF_SINTETICO}\")\n")
    r = rodar_pse(d)
    resultados.append({"id": "M1", "mutacao": "CPF sintetico em chamada de log "
                       "(fastetl/mut_m01_log.py)", "check_esperado": "P-01 (CRITICO/ALTO)",
                       "resultado": {"exit_processo": r["exit"], **resumo(r["laudo"])},
                       "comando": r["cmd"], "dur_s": r["dur_s"]})

    # ---------- M2: credencial sintetica formato conhecido, fora de tests/ (S-06) ----------
    d = copia_fresca("m02")
    p = os.path.join(d, "fastetl", "mut_m02_cred.py")
    with open(p, "w") as f:
        f.write("api_key = \"sk-live-plantada-0123456789\"\n")
    r = rodar_pse(d)
    resultados.append({"id": "M2", "mutacao": "Credencial sintetica com formato "
                       "conhecido (sk-) em codigo nao-teste", "check_esperado": "S-06/P-06 (CRITICO)",
                       "resultado": {"exit_processo": r["exit"], **resumo(r["laudo"])},
                       "comando": r["cmd"], "dur_s": r["dur_s"]})

    # ---------- M3: host de terceiro sintetico em URL (S-04) ----------
    d = copia_fresca("m03")
    p = os.path.join(d, "fastetl", "mut_m03_terceiro.py")
    with open(p, "w") as f:
        f.write("import requests\n\n\ndef enviar():\n"
                "    requests.post(\"https://api.x.example.net/collect\", json={})\n")
    r = rodar_pse(d)
    resultados.append({"id": "M3", "mutacao": "Host de terceiro sintetico "
                       "(api.x.example.net) em integracao de fixture",
                       "check_esperado": "S-04 (ALTO - dominio reservado em URL NAO suprime)",
                       "resultado": {"exit_processo": r["exit"], **resumo(r["laudo"])},
                       "comando": r["cmd"], "dur_s": r["dur_s"]})

    # ---------- M4: catalogo declarativo criado com campo sensivel sem cifra (P-04 cessa; P-18 morde) ----------
    d = copia_fresca("m04")
    os.makedirs(os.path.join(d, "tests", "qa"), exist_ok=True)
    with open(os.path.join(d, "tests", "qa", "catalog.yaml"), "w") as f:
        f.write("tables:\n  clientes:\n    fields:\n      cpf:\n"
                "        class: personal\n        owner: cadastro\n"
                "        purpose: identificacao\n        legal_basis: contrato\n"
                "        retention_years: 5\n")
    r = rodar_pse(d)
    resultados.append({"id": "M4", "mutacao": "Criacao de tests/qa/catalog.yaml "
                       "com campo pessoal sem cifra", "check_esperado": "P-04 deixa de acusar; "
                       "P-18 emite ALTO (campo sensivel sem cifra)",
                       "resultado": {"exit_processo": r["exit"], **resumo(r["laudo"])},
                       "comando": r["cmd"], "dur_s": r["dur_s"]})

    # ---------- M5: sha256 nu de campo pessoal com escrita (P-20) ----------
    d = copia_fresca("m05")
    os.makedirs(os.path.join(d, "tests", "qa"), exist_ok=True)
    with open(os.path.join(d, "tests", "qa", "catalog.yaml"), "w") as f:
        f.write("tables:\n  clientes:\n    fields:\n      cpf:\n"
                "        class: personal\n        owner: cadastro\n"
                "        purpose: identificacao\n        legal_basis: contrato\n"
                "        retention_years: 5\n")
    p = os.path.join(d, "fastetl", "mut_m05_hash.py")
    with open(p, "w") as f:
        f.write("import hashlib\n\n\ndef exportar(cliente, warehouse):\n"
                "    h = hashlib.sha256(cliente.cpf.encode()).hexdigest()\n"
                "    warehouse.insert(\"dim_cliente\", {\"id_anonimo\": h})\n")
    r = rodar_pse(d)
    resultados.append({"id": "M5", "mutacao": "sha256 nu de campo pessoal gravado "
                       "como id_anonimo (com catalogo)", "check_esperado": "P-20 (ALTO)",
                       "resultado": {"exit_processo": r["exit"], **resumo(r["laudo"])},
                       "comando": r["cmd"], "dur_s": r["dur_s"]})

    # ---------- M6: decision_making declarado (E-00 muda o escopo do pack) ----------
    d = copia_fresca("m06")
    cfg = os.path.join(d, "mut-config.yaml")
    with open(cfg, "w") as f:
        f.write("decision_making: automated\n")
    r = rodar_pse(d, config=cfg)
    resultados.append({"id": "M6", "mutacao": "pse-config.yaml declarando "
                       "decision_making: automated em corpus SEM IA",
                       "check_esperado": "pack ethics entra em escopo (E-00 respeita declaracao)",
                       "resultado": {"exit_processo": r["exit"], **resumo(r["laudo"])},
                       "comando": r["cmd"], "dur_s": r["dur_s"]})

    # ---------- M7: doc gerada da PSE alterada -> trava de CI deve reprovar ----------
    d = os.path.join(WORK, "m07-pse-copy")
    if os.path.exists(d):
        shutil.rmtree(d)
    shutil.copytree(SRC_PSE, d, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"))
    doc = os.path.join(d, "docs", "TESTES.md")

    # M7a (tentativa 1): acrescentar linha APOS o rodape volatil -> trava NAO morde
    # (corpo_comparado corta na marca; comportamento documentado na propria suite)
    with open(doc, "a") as f:
        f.write("\n<!-- mutacao M7a: linha manual apos o rodape -->\n")
    t0 = time.time()
    rr = subprocess.run(["/home/z/my-project/tpf-pse-fastetl/.venv-pse/bin/python",
                         "-m", "pytest", "tests/test_indice.py::test_docs_testes_esta_atualizado", "-q"],
                        capture_output=True, text=True, cwd=d, timeout=240)
    dur_a = round(time.time() - t0, 2)
    m7a_exit = rr.returncode

    # M7b (tentativa 2): adulterar o CORPO da doc -> trava deve morder
    with open(doc) as f:
        conteudo = f.read()
    conteudo_mut = conteudo.replace("Camada A", "Camada Z", 1)
    assert conteudo_mut != conteudo, "mutacao do corpo falhou"
    with open(doc, "w") as f:
        f.write(conteudo_mut)
    t0 = time.time()
    rr2 = subprocess.run(["/home/z/my-project/tpf-pse-fastetl/.venv-pse/bin/python",
                          "-m", "pytest", "tests/test_indice.py::test_docs_testes_esta_atualizado", "-q"],
                         capture_output=True, text=True, cwd=d, timeout=240)
    dur_b = round(time.time() - t0, 2)
    tail_b = [l for l in rr2.stdout.strip().splitlines() if l.strip()][-1:] if rr2.stdout else []
    resultados.append({"id": "M7a", "mutacao": "Linha manual APOS o rodape volatil "
                       "de docs/TESTES.md (copia descartavel da PSE)",
                       "check_esperado": "trava NAO morde (comparacao corta na marca de rodape)",
                       "resultado": {"exit": m7a_exit,
                                     "leitura": "comportamento coerente com test_o_que_vem_depois_da_marca_nao_entra_na_comparacao"},
                       "comando": "pytest tests/test_indice.py::test_docs_testes_esta_atualizado -q",
                       "dur_s": dur_a})
    resultados.append({"id": "M7b", "mutacao": "Adulteracao do CORPO de docs/TESTES.md "
                       "(Camada A -> Camada Z), como no proprio teste de tamper da suite",
                       "check_esperado": "trava REPROVA (doc desatualizada)",
                       "resultado": {"exit": rr2.returncode, "pytest_tail": tail_b},
                       "comando": "pytest tests/test_indice.py::test_docs_testes_esta_atualizado -q",
                       "dur_s": dur_b})

    # ---------- M8: arquivo fora de alcance (declaracao de limite) ----------
    d = copia_fresca("m08")
    with open(os.path.join(d, "notas.zip"), "wb") as f:
        f.write(b"PK\x05\x06" + b"\x00" * 18)  # zip vazio sintetico
    r = rodar_pse(d)
    resultados.append({"id": "M8", "mutacao": "Arquivo notas.zip (extensao fora de alcance)",
                       "check_esperado": "alcance.fora_de_alcance cresce de 2 para 3; "
                       "nenhum estado falso positivo",
                       "resultado": {"exit_processo": r["exit"], **resumo(r["laudo"])},
                       "comando": r["cmd"], "dur_s": r["dur_s"]})

    with open(OUT, "w") as f:
        json.dump({"gerado_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "nota": "copias descartaveis; clones originais intactos", "mutacoes": resultados},
                  f, ensure_ascii=False, indent=1)

    # sintese curta
    for m in resultados:
        res = m["resultado"]
        if m["id"].startswith("M7"):
            print(f"{m['id']}: pytest exit={res['exit']} (esperado 1/reprova)")
            continue
        fs = res.get("findings", [])
        novos = [f"{f['check']}/{f['sev']}" for f in fs if "mut_m" in str(f["arq"]) or True]
        print(f"{m['id']}: exit={res.get('exit_code')} findings={len(fs)} "
              f"primeiros={[f['check'] for f in fs][:8]} fora_alcance={res.get('fora_de_alcance')} "
              f"packs_fora={res.get('fora_escopo_packs')}")
    print("OK ->", OUT)


if __name__ == "__main__":
    main()
