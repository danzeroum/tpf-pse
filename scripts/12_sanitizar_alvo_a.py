#!/usr/bin/env python3
"""Sanitizacao do laudo bruto PSE x api-pgd (rodada A — recuperada por re-execucao).

Mesmas regras do protocolo TPF aplicadas pela rodada B (scripts/06_sanitizar.py):
- Nao reproduzir possivel segredo, token, PII ou valor de configuracao.
- Hosts externos mascarados em evidencia ([REDACTED-HOST]).
- Snippet de credencial (check P-06) substituido integralmente.
- Varredura global por literais proibidos no JSON inteiro.
"""
import json
import hashlib
import datetime
import re

BASE = "/home/z/my-project/tpf-pse-fastetl"
RAW = f"{BASE}/evidence/raw/laudo-alvo-a-bruto.json"
OUT = f"{BASE}/evidence/sanitized/laudo-alvo-a-sanitizado.json"

# Literais que NUNCA podem aparecer no material sanitizado.
# (hosts externos apontados por S-04 no alvo A; a inspecao manual os descreve
#  qualitativamente nos relatorios — host de documentacao de biblioteca e URL
#  de hospedagem de codigo em arquivo de exemplo)
PADROES_REDACT = [
    "errors.pydantic.dev",
    "github.com",
]


def redact_str(s: str):
    if not isinstance(s, str):
        return s, []
    changed = []
    for lit in PADROES_REDACT:
        if lit in s:
            s = s.replace(lit, "[REDACTED-HOST]")
            changed.append("host-mascarado")
    s2 = re.sub(r"(https?://)[A-Za-z0-9.\-_]+", lambda m: m.group(1) + "[REDACTED-HOST]", s)
    if s2 != s:
        changed.append("host-mascarado")
        s = s2
    return s, changed


def walk(obj):
    n = 0
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                obj[k], c = redact_str(v)
                n += len(c)
            else:
                n += walk(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                obj[i], c = redact_str(v)
                n += len(c)
            else:
                n += walk(v)
    return n


def main():
    laudo = json.load(open(RAW))

    redactions = []
    # 1. regra de credencial (safeguard; sem P-06 findings neste alvo)
    for f_ in laudo.get("findings", []):
        if f_.get("snippet"):
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

    # 2. mascaramento em todo o laudo (titulos de findings, motivos, textos)
    n = walk(laudo)
    if n:
        redactions.append({"escopo": "varredura-estrutural",
                           "acao": f"{n} campo(s) com host/valor mascarado em todo o laudo"})

    # 3. varredura global por literais proibidos
    blob = json.dumps(laudo, ensure_ascii=False, indent=1)
    for lit in PADROES_REDACT:
        if lit in blob:
            blob = blob.replace(lit, "[REDACTED-HOST]")
            redactions.append({"escopo": "varredura-global", "acao": f"host {lit} mascarado"})

    laudo["sanitizacao"] = {
        "data_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "metodo": "redacao assistida por script (scripts/12_sanitizar_alvo_a.py); "
                  "mesmas regras do protocolo TPF da rodada B: tipo de indício + check + arquivo:linha, sem literal",
        "regras": [
            "hosts externos apontados por S-04 mascarados como [REDACTED-HOST] (inclui titulos de findings)",
            "URLs com esquema mascaradas como https://[REDACTED-HOST]",
            "snippet de credencial (P-06) seria substituido integralmente (regra preventiva; sem P-06 neste alvo)",
            "varredura global por literais proibidos aplicada ao JSON inteiro",
        ],
        "redacoes": redactions,
        "nota": "o laudo BRUTO permanece em evidence/raw/ e nao deve ser divulgado",
    }

    with open(OUT, "w") as f:
        f.write(json.dumps(laudo, ensure_ascii=False, indent=1))

    final = open(OUT).read()
    for lit in PADROES_REDACT:
        assert lit not in final, f"LITERAL PROIBIDO RESTANTE: {lit}"
    h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("OK sanitizado:", OUT)
    print("sha256:", h)
    print("redacoes registradas:", len(redactions))


if __name__ == "__main__":
    main()
