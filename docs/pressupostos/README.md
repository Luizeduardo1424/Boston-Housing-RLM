# Pressupostos estatísticos da análise

Este documento descreve os pressupostos estatísticos assumidos em cada etapa dos dois notebooks do projeto: [`notebooks/01-AED.ipynb`](../../notebooks/01-AED.ipynb) (análise exploratória, Partes 1 a 4, Seções 2 a 9) e [`notebooks/02-MRLM.ipynb`](../../notebooks/02-MRLM.ipynb) (modelo de regressão linear múltipla, Partes 5 a 12, Seções 10 em diante). O `02-MRLM` lê o arquivo `data/housing_processed.csv`, salvo no final do `01-AED`. Para cada etapa, ele indica a função de biblioteca usada, os parâmetros efetivamente aplicados (inclusive os padrões implícitos) e o que cada resultado permite ou não concluir. Os números de célula são os índices de cada notebook (contados a partir de 0). Cada arquivo diz no início a qual notebook as células pertencem.

Os gráficos são interativos (Plotly). Ao passar o mouse sobre um ponto, o gráfico mostra a linha do arquivo, a cidade (`TOWN`), os valores do gráfico (ajustado, resíduo, alavanca, Cook) e `MEDV`, `CRIM`, `RM`, `LSTAT` e `RAD`. As curvas LOWESS e as linhas de referência também mostram o valor. As funções de gráfico ficam no módulo [`notebooks/graficos.py`](../../notebooks/graficos.py), usado pelos dois notebooks, e cada figura é salva em `results/figures/*.html`.

Versões usadas na execução do notebook (`.venv`): pandas 3.0.6, numpy 2.5.3, scipy 1.18.1, statsmodels 0.15.0, plotly 7.1.0, scikit-learn, libpysal 4.15.0, esda 2.10.0, spreg 1.9.1. Os parâmetros padrão citados foram conferidos no código-fonte dessas versões.

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
| [`16-pontos-influentes-modelo-final.md`](16-pontos-influentes-modelo-final.md) | §24 | Pontos que pioram o modelo final: linha 414 na ponta esquerda da escala-locação, outliers, 2ª rodada de influentes, reajuste e validação cruzada (Parte 12 do notebook) |
| [`referencias.md`](referencias.md) | n/a | Referências |

As seções §20 a §23 (interação `RM × logLSTAT`, indicadora `ZN > 0`, colinearidade entre `NOX` e `logDIS` e comparação sistemática dos modelos) foram retiradas do notebook: eram hipóteses de melhoria que não mudaram o modelo final. Os números das outras seções não mudam. A antiga Parte 16 do notebook passou a ser a Parte 12.

O antigo `notebooks/EDA.ipynb` foi dividido em `01-AED.ipynb` (células 0 a 52, com os mesmos índices) e `02-MRLM.ipynb`. No `02-MRLM`, a célula N corresponde à antiga célula N + 51.
