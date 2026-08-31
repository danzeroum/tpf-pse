#!/usr/bin/env python3
"""Rodada A (recuperada por re-execucao local): analise do laudo 'alvo-a'.

Replica a metodologia do script 10_analise_revisao.py (indicadores do parecer),
com a mesma regra de classificação e precedência declarada (07, §10.1):
  1. guarda E-00 (ética/IA fora de escopo)            -> não aplicável
  2. vetor estrutural ausente no perfil sem IA        -> não aplicável
  3. demais pulos = artefato declarativo/convensão    -> dependente de contexto
  4. não habilitados (Trabalho A sem alvo autorizado) -> dependente de contexto
Verifica a partição: executados + não aplicáveis + dependentes = 58.
Gera matrices/estados-por-check-alvo-a.md (matriz compacta de estados).
"""
import json
from collections import Counter

BASE = "/home/z/my-project/tpf-pse-fastetl"
n = json.load(open(f"{BASE}/evidence/raw/laudo-alvo-a-bruto.json"))

art = n["artifact"]
print("=== proveniencia do laudo ===")
for k in ("suite", "suite_version", "schema_version", "catalog_hash", "repo_commit",
          "config_fingerprint", "timestamp_utc", "duracao_s", "modo", "autorizacao"):
    print(f"  {k}: {art.get(k)}")
print("  exit_code:", n.get("exit_code"), "| veredito:", n.get("veredito"))

ex = n["checks_executados"]
pl = n["checks_pulados"]
nh = n["checks_nao_habilitados"]
finds = n["findings"]
cob = n["cobertura"]

def classificar(m):
    if "fora de escopo" in m and "etica" in m:
        return "nao_aplicavel"
    if m.startswith("nenhuma chamada de treino") or m.startswith("nenhuma producao de evento em barramento"):
        return "nao_aplicavel"
    return "dependente_contexto"

achado_checks = sorted({f["check_id"] for f in finds})
sem_achado = sorted(set(ex) - set(achado_checks))

etica = [p for p in pl if classificar(p["motivo"]) == "nao_aplicavel" and "etica" in p["motivo"]]
estrut = [p for p in pl if classificar(p["motivo"]) == "nao_aplicavel" and "etica" not in p["motivo"]]
declar = [p for p in pl if classificar(p["motivo"]) == "dependente_contexto"]

print("\n=== estados ===")
print("executados:", len(ex), "| pulados:", len(pl), "| nao habilitados:", len(nh),
      "| indeterminados:", len(n.get("checks_indeterminados", [])))
print("IDs com achado (distintos):", achado_checks, "| achados por check:", Counter(f["check_id"] for f in finds))
print("sem achado IDs:", sem_achado)
print("severidades:", Counter(f["severidade"] for f in finds))
print("achados por pilar:", Counter(f["check_id"][0] for f in finds))
print("cobertura_parcial:", json.dumps(n.get("relatorios", {}).get("cobertura_parcial", []), ensure_ascii=False)[:300])
print("correlacoes:", json.dumps(n.get("correlacoes", []), ensure_ascii=False)[:300])

print("\n=== indicadores (metodologia do parecer) ===")
total = cob["catalogo_total"]
nao_hab_n = len(nh)
aplicaveis = total - len(etica) - nao_hab_n
print("etica (guarda E-00):", len(etica), "| vetor estrutural:", [p["id"] for p in estrut],
      "| declarativo ausente:", [p["id"] for p in declar])
print(f"(1) cobertura bruta = {len(ex)}/{total} = {len(ex)/total:.1%}")
print(f"(2) potencialmente aplicaveis = {total} - {len(etica)} - {nao_hab_n} = {aplicaveis}"
      f" ; cobertura sobre aplicaveis = {len(ex)}/{aplicaveis} = {len(ex)/aplicaveis:.1%}")
nao_aplic = len(etica) + len(estrut)
dep_contexto = len(declar) + nao_hab_n
print(f"(3) nao aplicaveis = {len(etica)} + {len(estrut)} = {nao_aplic}")
print(f"(4) dependentes de contexto = {len(declar)} + {nao_hab_n} = {dep_contexto}")
soma = len(ex) + nao_aplic + dep_contexto
print(f"PARTICAO: {len(ex)} + {nao_aplic} + {dep_contexto} = {soma} (catalogo = {total}) "
      f"{'OK - particao mutuamente exclusiva' if soma == total else 'ERRO - NAO E PARTICAO'}")

print("\n=== alcance ===")
print(json.dumps(n.get("alcance", {}), ensure_ascii=False)[:600])

# ---- matriz compacta de estados (alvo A) ----
find_by_check = {}
for f in finds:
    find_by_check.setdefault(f["check_id"], []).append(f)
skip_by_id = {p["id"]: p for p in pl}
nh_by_id = {p["id"]: p for p in nh}

def pilar(cid):
    return {"P": "privacy", "S": "security", "E": "ethics"}[cid[0]]

rows = []
for cid in sorted(set(ex) | set(skip_by_id) | set(nh_by_id)):
    if cid in ex:
        fnd = find_by_check.get(cid, [])
        det = f"{len(fnd)} finding(s): " + ", ".join(sorted({f['severidade'] for f in fnd})) if fnd else "sem achado (substrato lido)"
        rows.append((cid, pilar(cid), "executado", det))
    elif cid in skip_by_id:
        cat = classificar(skip_by_id[cid]["motivo"])
        cat_label = "nao aplicavel" if cat == "nao_aplicavel" else "dependente de contexto"
        motivo = skip_by_id[cid]["motivo"]
        motivo = motivo if "etica" not in motivo else "guarda E-00: pack ethics fora de escopo (motivo herdado E-01..E-13)"
        rows.append((cid, pilar(cid), f"pulado — {cat_label}", motivo[:95]))
    else:
        rows.append((cid, pilar(cid), "nao habilitado — dependente de contexto", "Trabalho A sem target declarado (previsto e nao pedido)"))

md = ["# Matriz de estados por check — Alvo A (api-pgd, recuperação por re-execução local)", "",
      f"Laudo: `evidence/raw/laudo-alvo-a-bruto.json` · commit `9d4b774c` · suite 0.20.0 · `catalog_hash 4682a4ae…a0ac` · modo `pse_inventory`",
      "", "Classificação com precedência declarada (relatório 07, §10.1): executado / não aplicável (guarda E-00 ou vetor estrutural ausente) / dependente de contexto (artefato declarativo do operador ou Trabalho A).",
      "", "| Check | Pilar | Estado | Detalhe / motivo (resumido) |", "|---|---|---|---|"]
for cid, pil, est, det in rows:
    md.append(f"| {cid} | {pil} | {est} | {det} |")
tot = cob["catalogo_total"]
md += ["", f"**Partição:** executados {len(ex)} + não aplicáveis {nao_aplic} + dependentes de contexto {dep_contexto} = {soma} de {total} — "
       f"{'partição mutuamente exclusiva do catálogo.' if soma == tot else 'ERRO: não é partição.'}",
       "", "Nota: motivos abreviados para leitura; os motivos íntegros constam do laudo. Nenhum motivo de pulo é silencioso.", ""]
open(f"{BASE}/matrices/estados-por-check-alvo-a.md", "w").write("\n".join(md))
print(f"\nOK matriz: matrices/estados-por-check-alvo-a.md ({len(rows)} checks)")
