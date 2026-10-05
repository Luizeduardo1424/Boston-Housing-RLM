# Pressupostos estatísticos da análise

Este documento descreve os pressupostos estatísticos assumidos em cada etapa do notebook [`notebooks/EDA.ipynb`](../../notebooks/EDA.ipynb). Para cada etapa, ele indica a função de biblioteca usada, os parâmetros efetivamente aplicados (inclusive os padrões implícitos) e o que cada resultado permite ou não concluir. Os números de célula são os índices do notebook (contados a partir de 0).

Versões usadas na execução do notebook (`.venv`): pandas 3.0.6, numpy 2.5.3, scipy 1.18.1, statsmodels 0.15.0, seaborn 0.13.2. Os parâmetros padrão citados foram conferidos no código-fonte dessas versões.

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
| [`referencias.md`](referencias.md) | n/a | Referências |
