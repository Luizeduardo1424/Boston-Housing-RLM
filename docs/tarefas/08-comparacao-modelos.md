# Tarefa 08: comparar os modelos possíveis e escolher os 2 melhores

## Contexto

O notebook comparou modelos em etapas: seleção na Parte 5 ([Seção 12](../pressupostos/04-selecao-modelos.md)), transformações na Parte 7 ([Seção 14](../pressupostos/06-transformacoes.md)) e remoção de `ZN`, `INDUS` e `AGE` na Parte 8 ([Seção 16](../pressupostos/08-modelo-final.md)). Cada etapa partiu da anterior, então combinações de outros caminhos nunca foram testadas (por exemplo, `MEDV` na escala original com preditores em log, ou um modelo pequeno com 5 variáveis).

Esta tarefa faz uma comparação **sistemática**: muitos modelos, com e sem transformações, avaliados com os mesmos critérios. No fim, escolha 2 modelos:

- **Modelo A**: o que fica mais perto de cumprir todos os pressupostos, com boa previsão. Pode ter mais variáveis.
- **Modelo B**: um modelo com **menos variáveis** que o A, quase tão bom (um pouco pior), mais fácil de interpretar.

## Estado atual

- Modelo final: `formula_final` (célula 116), 11 termos (19 colunas com as indicadoras de `RAD`). Validação cruzada: RMSE 4,00, MAE 2,75, R² 0,79.
- Funções prontas: `resumir_residuos` e `linhas_influentes` (célula 118), `prever_log` (célula 126), `calcular_vif` (célula 4), `perfil_boxcox` (célula 102), `W_knn` (célula 158).

## O que fazer

1. **Espaço de busca.** Defina e registre o espaço antes de rodar:
   - **Resposta**: `MEDV` e `logMEDV`. Opcional: Box-Cox com o λ ótimo da célula 102.
   - **Preditores**: `CRIM`, `ZN`, `INDUS`, `CHAS`, `NOX`, `RM`, `AGE`, `DIS`, `RAD`, `TAX`, `PTRATIO`, `B`, `LSTAT`. `TAX` e `RAD` entram como alternativas, nunca juntos ([Seção 7](../pressupostos/02-eda.md)).
   - **Versões de cada preditor**: original; log (`CRIM`, `DIS`, `LSTAT`); termo quadrático centralizado (`RM`, `logLSTAT`); indicadora `ZN > 0`.
   - **Padronização** (z-score): registre que ela gera o **mesmo modelo**. Ajuste, resíduos, testes e previsões não mudam; só muda a escala dos coeficientes. Não conte como candidato separado; use-a só para comparar o tamanho dos efeitos.
2. **Busca.** Para cada combinação "resposta × versões", procure o melhor subconjunto de preditores **por tamanho** (1 a 13 variáveis) pelo BIC. Se o número de combinações passar de cerca de 100 mil, use seleção passo a passo para frente e para trás (`AIC`/`BIC`) e registre a troca. Ajuste em `df_t` (n = 501). Guarde o melhor modelo de cada tamanho.
3. **Avaliação.** Para cada candidato guardado:
   - validação cruzada da célula 126 (mesmas partes; para `logMEDV`, volte à escala de `MEDV` com `prever_log`), com RMSE, MAE e R² fora da amostra em mil dólares;
   - R² ajustado e BIC;
   - VIF máximo (GVIF para `RAD`);
   - `resumir_residuos`: RESET, Shapiro-Wilk, correlação QQ, Breusch-Pagan e DW;
   - I de Moran dos resíduos (opcional, com uma matriz KNN das linhas usadas).
4. **Escore de pressupostos.** Para cada candidato, conte quantos destes passam: RESET p > 0,05, Shapiro-Wilk p > 0,05 **ou** correlação QQ > 0,99, Breusch-Pagan p > 0,05, VIF máximo < 5. Registre o escore ao lado do RMSE. Nenhum modelo deve passar no Breusch-Pagan e no Moran; isso fica como limitação comum, tratada por HC3 e pela [Seção 19](../pressupostos/11-correlacao-espacial.md).
5. **Escolha dos 2 modelos.**
   - **Modelo A**: maior escore de pressupostos; no empate, menor RMSE.
   - **Modelo B**: o candidato com **menos variáveis** que o A, RMSE até cerca de 5% acima do A e escore igual ou um ponto abaixo.
   - Para A e B: reajuste em `df_final` (sem as influentes, como na Parte 8), coeficientes com HC3, efeitos em %, e os 4 gráficos de diagnóstico da célula 124. Compare com o modelo final atual em uma tabela.
6. **Decisão.** Diga se o Modelo A deve substituir o modelo final. Use o critério das outras tarefas: RMSE menor que 4,00 e nenhum pressuposto pior. Se a [Tarefa 06](06-colinearidade-nox-dis.md) já estiver feita, inclua as variantes dela como candidatas.

## Critério de pronto

- Tabela de todos os candidatos guardados (resposta, versões, variáveis, número de termos, métricas e escore) salva em `results/tables/comparacao_modelos.csv`.
- Gráfico de RMSE da validação cruzada pelo número de variáveis, uma curva por combinação "resposta × versões", com A e B marcados. Salve em `results/figures/`.
- Tabela final "Modelo A × Modelo B × modelo final" e a justificativa da escolha.

## Documentação a atualizar

- Novo `docs/pressupostos/NN-comparacao-modelos.md` com o próximo número livre. Se passar de cerca de 250 linhas, divida em dois arquivos (busca e escolha).
- `07-pendencias.md`: linha "Modelo final".
- `README.md` (raiz), "Resultados" e "Limitações", se o modelo final mudar.

## Referências

- Schwarz, G. (1978). Estimating the dimension of a model. *The Annals of Statistics*, 6(2), 461–464 (BIC).
- James, G.; Witten, D.; Hastie, T.; Tibshirani, R. (2021). *An Introduction to Statistical Learning*. 2. ed. Springer (capítulo 6: seleção de subconjuntos e validação cruzada).
