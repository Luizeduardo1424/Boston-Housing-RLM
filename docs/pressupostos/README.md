# Pressupostos estatísticos da análise

Este documento descreve os pressupostos estatísticos assumidos em cada etapa do notebook [`notebooks/EDA.ipynb`](../../notebooks/EDA.ipynb). Para cada etapa, ele indica a função de biblioteca usada, os parâmetros efetivamente aplicados (inclusive os padrões implícitos) e o que cada resultado permite ou não concluir. Os números de célula são os índices do notebook (contados a partir de 0).

Versões usadas na execução do notebook (`.venv`): pandas 3.0.6, numpy 2.5.3, scipy 1.18.1, statsmodels 0.15.0, seaborn 0.13.2, scikit-learn, libpysal 4.15.0, esda 2.10.0, spreg 1.9.1. Os parâmetros padrão citados foram conferidos no código-fonte dessas versões.

---

## Índice

Leia este índice e abra só o arquivo da seção necessária.

| Arquivo | Seções | Conteúdo |
|---|---|---|
| [`01-visao-geral.md`](01-visao-geral.md) | §1 | Visão geral e resíduos usados |
| [`02-eda.md`](02-eda.md) | §2–§9 | Análise exploratória (tipagem, univariada, linearidade, grupos, correlação, VIF, condição) |
| [`03-modelo-completo-residuos.md`](03-modelo-completo-residuos.md) | §10–§11 | Modelo completo e diagnóstico dos resíduos (Parte 5) |
| [`04-selecao-modelos.md`](04-selecao-modelos.md) | §12 | Sensibilidade e seleção de modelos |
| [`05-termo-quadratico-rm.md`](05-termo-quadratico-rm.md) | §13 | Termo quadrático de RM (Parte 6) |
| [`06-transformacoes.md`](06-transformacoes.md) | §14 | Transformações, centralização, HC3 e independência (Parte 7) |
| [`07-pendencias.md`](07-pendencias.md) | §15 | O que ainda não foi verificado |
| [`08-modelo-final.md`](08-modelo-final.md) | §16 | Modelo final: seleção, influentes, HC3, erros agrupados e validação cruzada (Parte 8) |
| [`09-heterocedasticidade.md`](09-heterocedasticidade.md) | §17 | Heterocedasticidade: forma da variância, MQGF, volta à escala de `MEDV` e cobertura dos intervalos de previsão (Parte 9) |
| [`10-tobit.md`](10-tobit.md) | §18 | Censura em `MEDV = 50`: modelo Tobit, conferência por simulação, comparação com o MQO e validação cruzada (Parte 10) |
| [`11-correlacao-espacial.md`](11-correlacao-espacial.md) | §19 | Correlação espacial: coordenadas da versão corrigida, I de Moran, testes LM, modelo de erro espacial e erros agrupados por `TOWN` (Parte 11) |
| [`12-interacoes.md`](12-interacoes.md) | §20 | Interação `RM × logLSTAT`: teste de Wald com HC3, alavanca da linha 365, efeito de um cômodo por quartil de `LSTAT` e validação cruzada (Parte 12) |
| [`13-indicadora-zn.md`](13-indicadora-zn.md) | §21 | Indicadora `ZN > 0`: Mann-Whitney por grupo, teste de Wald com HC3 e agrupado por cidade, colinearidade com `NOX` e `DIS` e validação cruzada (Parte 13) |
| [`14-colinearidade.md`](14-colinearidade.md) | §22 | Colinearidade entre `NOX` e `logDIS`: GVIF por termo, retirar variáveis, residualização, índice por componente principal, Ridge, volta de `TAX` e o par `RM_c` × `logLSTAT_c`, com validação cruzada (Parte 14) |
| [`referencias.md`](referencias.md) | n/a | Referências |
