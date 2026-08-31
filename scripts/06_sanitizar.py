#!/usr/bin/env python3
"""Fase 6 - Sanitizacao do laudo bruto PSE x FastETL.

Regras do protocolo TPF:
- Nao reproduzir possivel segredo, token, PII ou valor de configuracao.
- Substituir literais por [REDACTED], preservando tipo de indicio,
  check, arquivo relativo e linha.
- Registrar bloco de sanitizacao no proprio laudo sanitizado.
"""
import json
import hashlib
import datetime

BASE = "/home/z/my-project/tpf-pse-fastetl"
RAW = f"{BASE}/evidence/raw/laudo-alvo-b-bruto.json"
OUT = f"{BASE}/evidence/sanitized/laudo-alvo-b-sanitizado.json"

# Substrings que NUNCA podem aparecer no material sanitizado.
PADROES_REDACT = [
    "ozoBaroF2021",          # literal de credencial apontado por P-06 (fixture de teste)
    "gestaogovbr/FastETL",   # mantido apenas mascarado em evidencia de host? (URL publica, mas e valor de config -> mascarar em snippet)
]

def redact_str(s: str):
    if not isinstance(s, str):
        return s, []
    changed = []
    for lit in PADROES_REDACT:
        if lit in s:
            s = s.replace(lit, "[REDACTED]")
            changed.append(lit[:4] + "***")
    # host de terceiro: manter so o prefixo como o proprio laudo faz (git..., gra..., log..., www...)
    import re
    def mask_url(m):
        prefix = m.group(1)
        return f"{prefix}[REDACTED]"
    s2 = re.sub(r"(https?://)[A-Za-z0-9.\-_]+", lambda m: m.group(1) + "[REDACTED-HOST]", s)
    if s2 != s:
        changed.append("host-mascarado")
        s = s2
    return s, changed


def walk(obj, path=""):
    n = 0
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k], c = redact_str(v) if isinstance(v, str) else (walk(v, f"{path}.{k}"), []) if not isinstance(v, (dict, list)) else (walk(v, f"{path}.{k}"), [])
            n += len(c) + (len(obj[k][1]) if False else 0)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                obj[i], c = redact_str(v)
                n += len(c)
            else:
                n += walk(v, f"{path}[{i}]")
    return n


def main():
    with open(RAW) as f:
        laudo = json.load(f)

    # 1. snippets de credencial: redacao total (nao manter nem prefixo parcial)
    redactions = []
    for f_ in laudo.get("findings", []):
        if f_.get("check_id") == "P-06" and f_.get("snippet"):
            redactions.append({"check": "P-06", "campo": "snippet",
                               "arquivo": f_.get("arquivo"), "linha": f_.get("linha"),
                               "acao": "literal substituido por [REDACTED-SNIPPET-CREDENCIAL]"})
            f_["snippet"] = "[REDACTED-SNIPPET-CREDENCIAL]"
        elif f_.get("snippet"):
            s, c = redact_str(f_["snippet"])
            if c:
                redactions.append({"check": f_.get("check_id"), "campo": "snippet",
                                   "arquivo": f_.get("arquivo"), "linha": f_.get("linha"),
                                   "acao": "host/valor mascarado"})
            f_["snippet"] = s
        if f_.get("trace"):
            s, c = redact_str(json.dumps(f_["trace"], ensure_ascii=False))
            if c:
                redactions.append({"check": f_.get("check_id"), "campo": "trace",
                                   "acao": "host/valor mascarado"})
            try:
                f_["trace"] = json.loads(s)
            except Exception:
                f_["trace"] = s

    # 2. varredura geral por literais proibidos em todo o laudo
    blob = json.dumps(laudo, ensure_ascii=False, indent=1)
    for lit in PADROES_REDACT:
        if lit in blob:
            blob = blob.replace(lit, "[REDACTED]")
            redactions.append({"escopo": "varredura-global", "acao": f"literal {lit[:4]}*** substituido"})

    laudo["sanitizacao"] = {
        "data_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "metodo": "redacao manual assistida por script (scripts/06_sanitizar.py); "
                  "conforme protocolo TPF: tipo de indício + check + arquivo:linha, sem literal",
        "regras": [
            "snippet de P-06 (credencial) substituido integralmente por [REDACTED-SNIPPET-CREDENCIAL]",
            "URLs de host em campos de evidencia mascaradas como https://[REDACTED-HOST]",
            "varredura global por literais proibidos aplicada ao JSON inteiro",
        ],
        "redacoes": redactions,
        "nota": "o laudo BRUTO permanece em evidence/raw/ e nao deve ser divulgado; "
                "a propria PSE ja mascarava o valor parcialmente na origem",
    }

    with open(OUT, "w") as f:
        f.write(blob if not laudo.get("sanitizacao") else json.dumps(laudo, ensure_ascii=False, indent=1))

    # verificacao final
    final = open(OUT).read()
    for lit in PADROES_REDACT:
        assert lit not in final, f"LITERAL PROIBIDO RESTANTE: {lit}"
    h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("OK sanitizado:", OUT)
    print("sha256:", h)
    print("redacoes:", len(redactions))


if __name__ == "__main__":
    main()
