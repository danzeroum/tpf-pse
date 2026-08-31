#!/usr/bin/env python3
"""Rodada C (alvo de IA — LlamaFactory): analise do laudo 'alvo-c'.

Replica a metodologia dos scripts 10/11 (indicadores do parecer, regra de
classificacao com precedencia declarada — 07, §10.1), com DUAS extensoes
declaradas ANTES da analise, exigidas pelo novo perfil (IA em escopo):

  (a) o laudo tem 2 checks INDETERMINADOS (E-06, P-15) — a particao do alvo C
      e, portanto, QUADRIpartida: executados + nao aplicaveis + dependentes
      de contexto + indeterminados = 58. Em A/B os indeterminados eram 0 e a
      particao era tripartida; o estado indeterminado NUNCA e colapsado em
      outra categoria (principio anti-colapso de estados da suite).
  (b) o motivo de pulo do E-12 ("nenhuma exportacao de embedding/hash derivado
      no codigo") tem a MESMA FORMA dos vetores estruturais do §10.1 ("nenhuma
      producao de evento em barramento append-only no codigo") — ausencia
      computada de vetor no codigo, nao dependencia de artefato declarativo.
      Classificado como nao aplicavel, por forma de motivo, a priori.
      P-19 mantem a classificação estrutural que ja tinha em A/B.

  Demais pulos (catalogo/manifesto/contrato/residencia/finalidade — artefato
  declarativo ausente) e todos os nao habilitados (Trabalho A) continuam
  dependentes de contexto.
Gera matrices/estados-por-check-alvo-c.md.
"""
import json
from collections import Counter

BASE = "/home/z/my-project/tpf-pse-fastetl"
n = json.load(open(f"{BASE}/evidence/raw/laudo-alvo-c-bruto.json"))

art = n["artifact"]
print("=== proveniencia do laudo ===")
for k in ("suite", "suite_version", "schema_version", "catalog_hash", "repo_commit",
          "config_fingerprint", "timestamp_utc", "duracao_s", "modo", "autorizacao"):
    print(f"  {k}: {art.get(k)}")
print("  exit_code:", n.get("exit_code"), "| veredito:", n.get("veredito"))

ex = n["checks_executados"]
pl = n["checks_pulados"]
nh = n["checks_nao_habilitados"]
ind = n.get("checks_indeterminados", [])
finds = n["findings"]
cob = n["cobertura"]

# motivo de E-12 identificado a priori como vetor estrutural (forma do motivo)
VETORES_ESTRUTURAIS = ("nenhuma producao de evento em barramento",
                       "nenhuma exportacao de embedding/hash derivado")


def classificar(m):
    if m.startswith(VETORES_ESTRUTURAIS):
        return "nao_aplicavel"
    return "dependente_contexto"


achado_checks = sorted({f["check_id"] for f in finds})
sem_achado = sorted(set(ex) - set(achado_checks))

estrut = [p for p in pl if classificar(p["motivo"]) == "nao_aplicavel"]
declar = [p for p in pl if classificar(p["motivo"]) == "dependente_contexto"]

print("\n=== estados ===")
print("executados:", len(ex), "| pulados:", len(pl), "| nao habilitados:", len(nh),
      "| indeterminados:", len(ind), "| IDs indeterminados:", [c["id"] for c in ind])
print("IDs com achado (distintos):", achado_checks, "| achados por check:", Counter(f["check_id"] for f in finds))
print("sem achado IDs:", sem_achado)
print("severidades:", Counter(f["severidade"] for f in finds))
print("achados por pilar:", Counter(f["check_id"][0] for f in finds))
print("cobertura_parcial:", json.dumps(n.get("relatorios", {}).get("cobertura_parcial", []), ensure_ascii=False)[:300])
print("correlacoes:", json.dumps(n.get("correlacoes", []), ensure_ascii=False)[:300])

print("\n=== indicadores (metodologia do parecer, com extensoes declaradas) ===")
total = cob["catalogo_total"]
nao_hab_n = len(nh)
# denominador da cobertura aplicavel: catálogo − guarda E-00 (0 em C: pack em
# escopo) − Trabalho A; os indeterminados PERMANECEM no denominador (tentaram
# executar e não decidiram — colapsá-los fora do denominador inflaria a fração)
guarda_e00 = 0
aplicaveis = total - guarda_e00 - nao_hab_n
print("vetor estrutural (pulos):", [p["id"] for p in estrut])
print("declarativo ausente (pulos):", [p["id"] for p in declar])
print(f"(1) cobertura bruta = {len(ex)}/{total} = {len(ex)/total:.1%}")
print(f"(2) potencialmente aplicaveis = {total} - {guarda_e00} - {nao_hab_n} = {aplicaveis}"
      f" ; cobertura sobre aplicaveis = {len(ex)}/{aplicaveis} = {len(ex)/aplicaveis:.1%}"
      " (inclui 2 indeterminados no denominador)")
nao_aplic = len(estrut)
dep_contexto = len(declar) + nao_hab_n
indet = len(ind)
soma = len(ex) + nao_aplic + dep_contexto + indet
print(f"(3) nao aplicaveis = {nao_aplic}")
print(f"(4) dependentes de contexto = {len(declar)} + {nao_hab_n} = {dep_contexto}")
print(f"(5) indeterminados = {indet} (estado proprio, nunca colapsado)")
print(f"PARTICAO QUADRIpartida: {len(ex)} + {nao_aplic} + {dep_contexto} + {indet} = {soma} "
      f"(catalogo = {total}) "
      f"{'OK - particao mutuamente exclusiva' if soma == total else 'ERRO - NAO E PARTICAO'}")

print("\n=== alcance ===")
lidos = n.get("alcance", {}).get("lidos", [])
fora = n.get("alcance", {}).get("fora_de_alcance", [])
print("lidos:", [(x["linguagem"], x["arquivos"]) for x in lidos])
print("fora de alcance:", sum(x["arquivos"] for x in fora), "arquivos em", len(fora), "tipos")

# ---- matriz compacta de estados (alvo C) ----
find_by_check = {}
for f in finds:
    find_by_check.setdefault(f["check_id"], []).append(f)
skip_by_id = {p["id"]: p for p in pl}
nh_by_id = {p["id"]: p for p in nh}
ind_by_id = {p["id"]: p for p in ind}


def pilar(cid):
    return {"P": "privacy", "S": "security", "E": "ethics"}[cid[0]]


rows = []
for cid in sorted(set(ex) | set(skip_by_id) | set(nh_by_id) | set(ind_by_id)):
    if cid in ex:
        fnd = find_by_check.get(cid, [])
        det = f"{len(fnd)} finding(s): " + ", ".join(sorted({f['severidade'] for f in fnd})) if fnd else "sem achado (substrato lido)"
        rows.append((cid, pilar(cid), "executado", det))
    elif cid in ind_by_id:
        rows.append((cid, pilar(cid), "indeterminado — estado proprio", ind_by_id[cid]["motivo"][:95]))
    elif cid in skip_by_id:
        cat = classificar(skip_by_id[cid]["motivo"])
        cat_label = "nao aplicavel (vetor estrutural ausente)" if cat == "nao_aplicavel" else "dependente de contexto"
        rows.append((cid, pilar(cid), f"pulado — {cat_label}", skip_by_id[cid]["motivo"][:95]))
    else:
        rows.append((cid, pilar(cid), "nao habilitado — dependente de contexto",
                     "Trabalho A sem target declarado (previsto e nao pedido)"))

md = ["# Matriz de estados por check — Alvo C (LlamaFactory, perfil IA/treinamento)", "",
      f"Laudo: `evidence/raw/laudo-alvo-c-bruto.json` · commit `d6bb97ddff5d752d8b05aa099a168127c7253562` · suite 0.20.0 · `catalog_hash 4682a4ae…a0ac` · modo `pse_inventory`",
      "", "Classificação com precedência declarada (relatório 07, §10.1), com duas extensões declaradas a priori para este perfil "
      "(scripts/14_analise_alvo_c.py): partição quadriforme com estado indeterminado próprio; motivo do E-12 classificado como "
      "vetor estrutural ausente pela forma (\"nenhuma exportação de embedding/hash derivado no código\"), análogo ao P-19.",
      "", "| Check | Pilar | Estado | Detalhe / motivo (resumido) |", "|---|---|---|---|"]
for cid, pil, est, det in rows:
    md.append(f"| {cid} | {pil} | {est} | {det} |")
tot = cob["catalogo_total"]
md += ["", f"**Partição:** executados {len(ex)} + não aplicáveis {nao_aplic} + dependentes de contexto {dep_contexto} "
       f"+ indeterminados {indet} = {soma} de {total} — "
       f"{'partição mutuamente exclusiva do catálogo (estado indeterminado preservado, nunca colapsado).' if soma == tot else 'ERRO: não é partição.'}",
       "", "Nota: motivos abreviados para leitura; os motivos íntegros constam do laudo. Nenhum motivo de pulo é silencioso.", ""]
open(f"{BASE}/matrices/estados-por-check-alvo-c.md", "w").write("\n".join(md))
print(f"\nOK matriz: matrices/estados-por-check-alvo-c.md ({len(rows)} checks)")
