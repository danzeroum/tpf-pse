#!/usr/bin/env python3
"""Revisão (parecer rodada 2): indicadores de cobertura a partir do laudo 'alvo-b'."""
import json
from collections import Counter

BASE = "/home/z/my-project/tpf-pse-fastetl"
n = json.load(open(f"{BASE}/evidence/raw/laudo-alvo-b-bruto.json"))

ex = n["checks_executados"]           # lista de IDs
pl = n["checks_pulados"]              # [{id, motivo}]
nh = n["checks_nao_habilitados"]      # [{id, motivo}]
finds = n["findings"]
cob = n["cobertura"]

achado_checks = sorted({f["check_id"] for f in finds})
sem_achado = sorted(set(ex) - set(achado_checks))

# Regra de classificação com precedência declarada (nota metodológica do relatório 07, §10.1):
# 1. guarda E-00 (ética/IA fora de escopo)            -> não aplicável
# 2. vetor estrutural ausente no perfil sem IA        -> não aplicável
#    (pulo cujo motivo indica ausência de chamada de treino ou de barramento append-only)
# 3. demais pulos = artefato declarativo/convensão    -> dependente de contexto
# 4. não habilitados (Trabalho A sem alvo autorizado) -> dependente de contexto
def classificar(p):
    m = p["motivo"]
    if "fora de escopo" in m and "etica" in m:
        return "nao_aplicavel"
    if m.startswith("nenhuma chamada de treino") or m.startswith("nenhuma producao de evento em barramento"):
        return "nao_aplicavel"
    return "dependente_contexto"

mot_etica = [p for p in pl if classificar(p) == "nao_aplicavel" and "etica" in p["motivo"]]
estrut = [p for p in pl if classificar(p) == "nao_aplicavel" and "etica" not in p["motivo"]]
mot_declar = [p for p in pl if classificar(p) == "dependente_contexto"]

print("executados:", len(ex), "| pulados:", len(pl), "| nao habilitados:", len(nh))
print("IDs com achado (distintos):", achado_checks)
print("n checks com achado:", len(achado_checks), "| sem achado:", len(sem_achado))
print("sem achado IDs:", sem_achado)
print()
print("pulos ética (guarda E-00):", [p["id"] for p in mot_etica], "→", len(mot_etica))
print("pulos dependentes de contexto (declarativo ausente):", [p["id"] for p in mot_declar], "→", len(mot_declar))
print("pulos por vetor estrutural ausente:", [(p["id"], p["motivo"][:60]) for p in estrut])
print()

total = cob["catalogo_total"]
etica_n = len(mot_etica)
nao_hab_n = len(nh)
aplicaveis = total - etica_n - nao_hab_n
print(f"(1) cobertura bruta do catálogo = {len(ex)}/{total} = {len(ex)/total:.1%}")
print(f"(2) potencialmente aplicáveis = {total} - {etica_n} (ética/IA fora de escopo) - {nao_hab_n} (Trabalho A) = {aplicaveis}")
print(f"    cobertura sobre aplicáveis = {len(ex)}/{aplicaveis} = {len(ex)/aplicaveis:.1%}")
nao_aplic = etica_n + len(estrut)
dep_contexto = len(mot_declar) + nao_hab_n
print(f"(3) não aplicáveis ao perfil (ética guarda {etica_n} + vetores estruturalmente ausentes {len(estrut)}) = {nao_aplic}")
print(f"    IDs estruturais: {[p['id'] for p in estrut]}")
print(f"(4) dependentes de contexto = declarativos ausentes {len(mot_declar)} + Trabalho A {nao_hab_n} = {dep_contexto}")
soma = len(ex) + nao_aplic + dep_contexto
print(f"PARTICAO: {len(ex)} + {nao_aplic} + {dep_contexto} = {soma} (catálogo = {total}) "
      f"{'OK - partição mutuamente exclusiva' if soma == total else 'ERRO - NÃO É PARTIÇÃO'}")
print()
print("severidades findings:", Counter(f["severidade"] for f in finds))
print("achados por check:", Counter(f["check_id"] for f in finds))
