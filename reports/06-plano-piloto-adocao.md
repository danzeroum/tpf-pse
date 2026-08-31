# 06 — Plano de piloto futuro de adoção (Fase 11)

**Natureza:** proposta hipotética. **Nenhum piloto ocorreu nesta rodada.** Números mencionados são hipóteses iniciais a calibrar, não requisitos legais nem fatos científicos.

## 1. Escopo do piloto

- **Repositório voluntário e autorizado:** um repositório interno cujo dono formalize a adoção por escrito (termo de escopo e autorização), preferencialmente um consumidor real do FastETL em ambiente institucional com processo de proteção de dados já designado.
- **Modo estático, sem rede, como única etapa inicial:** `pse_inventory` sobre o clone do repositório voluntário, exatamente como nesta rodada. Nenhum Trabalho A (passivo/ativo) na fase 1 do piloto; caminho para passivo/dinâmico apenas em homologação isolada, com autorização formal e identidades sintéticas, num passo posterior.
- **Baseline inicial de alertas:** a primeira execução produz o baseline; nada bloqueia nele. Política **"alertar antes de bloquear"**: o gate de CI com exit codes 10/20 como bloqueantes é ativado apenas após o baseline ser triado e aceito pelos donos.

## 2. Papéis

| Papel | Responsabilidade |
|---|---|
| Revisor técnico | interpretar achados no contexto arquitetural (ex.: hook lendo `conn.password` é padrão Airflow; URL em User-Agent não é egresso) |
| DPO/compliance | decidir quais controles são pertinentes e quem é o dono de cada artefato declarativo (catálogo, manifesto, consent model, residency) |
| Dono do repositório | aprovar baseline, adotar artefatos declarativos, decidir política de gate no próprio CI |

## 3. Sanitização e retenção

- Laudos brutos permanecem em área não publicada (`evidence/raw` análogo); apenas a versão sanitizada circula — regra já exercida nesta TPF.
- Retenção dos laudos definida pelo consumidor (a carcaça de referência usa 90 dias; número a calibrar pelo piloto), com igualdade fiscalizada entre as declarações de retenção (padrão herdado do consumidor de referência).
- Snippets de credencial/PII nunca saem do local de execução: `[REDACTED]` por política, antes de qualquer anexo.

## 4. Severidade e triagem humana

- Fluxo obrigatório: achado → triagem humana com as categorias da Fase 7 → decisão documentada → retorno de calibração.
- Critérios de severidade: usar o vocabulário da suite (CRÍTICO/ALTO/MÉDIO) sem convertê-lo em classificação legal; contextos de teste seguem o comportamento de rebaixamento já implementado (ratificação 11), com a dúvida **visível e não suprimida**.
- Falso positivo confirmado entra no inventário de calibração do piloto (insumo para evolução da suite — ver matriz central §4).

## 5. Métricas de adoção (hipóteses a calibrar)

| Métrica | Definição proposta | Hipótese inicial |
|---|---|---|
| Cobertura de execução | executados / catálogo | Baseline desta rodada: 18/58 do catálogo (18/29 dos potencialmente aplicáveis ao perfil — indicadores no relatório 03, §1.1); alvo de piloto: os static-relevantes ao perfil executarem 100% |
| Tempo de execução | duração do inventory | Segundos (2,0 s nesta rodada); preparação em horas — mantê-la fora do CI é o objetivo |
| Confirmação humana | % de achados classificados em ≤ 1 ciclo de triagem | ≥ 80% (hipótese) |
| Ruído | achados classificados possivel-falso-positivo / total | Medir por check (nesta rodada: S-04 1/4, P-06 2/2) — insumo de calibração, não meta |
| Indeterminados | contagem por rodada | Meta: zero; qualquer indeterminado bloqueia e exige insumo provisionado (lição M6) |
| Esforço de remediação | artefatos declarativos adotados por sprint | Catálogo e manifesto primeiro (destravam P-02/P-08/P-18/S-05/S-08) |

## 6. Calibração de regras com regressão

- Cada falso positivo confirmado vira **caso de regressão** no padrão do consumidor: fixture mínima que a próxima versão da suite deve não-acusar (sem que a correção silencie achados reais — o mesmo princípio das mutações canônicas da própria suite).
- As mutações controladas desta rodada (M1–M8) já servem de modelo: cada correção de regra nasce com uma mutação que a prova.

## 7. Expansão gradual (fora do piloto fase 1)

1. **Passiva (`pse_passive`)** em ambiente de homologação isolado, com atestação de escopo, sem dado de titular real, somente após o estático estar estável.
2. **Dinâmica (navegador)** apenas se o alvo tiver superfície web — não é o caso do perfil FastETL; registrar formalmente como não aplicável.
3. **Ativa (`pse_active`)** apenas com `workflow_dispatch`, revisores obrigatórios, identidades sintéticas e nunca contra produção (recusa embutida na suite).
4. E-08 com `lineage.jsonl` do pipeline é a expansão de maior valor potencial para o perfil Airflow (ver matriz central).

## 8. Critérios de encerramento do piloto

- Baseline triado 100% com classificação humana documentada.
- Artefatos declarativos essenciais adotados ou formalmente recusados com justificativa.
- Taxa de ruído conhecida por check e inventário de regressão iniciado.
- Decisão de gate documentada pelo dono (política de CI declarativa e protegida — "uma trava que o vigiado pode desligar em silêncio não é uma trava").
