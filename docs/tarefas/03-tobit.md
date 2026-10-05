# Tarefa 03: modelo Tobit para a censura em `MEDV = 50`

## Contexto

`MEDV` foi limitado em 50 (mil dólares) na coleta. Para 16 setores de `df_t`, o valor real é **50 ou mais**, mas o arquivo mostra só 50. O MQO trata esses 16 valores como exatos. Isso puxa a parte de cima da reta para baixo e tende a **atenuar** as inclinações (Seção 9 de [`02-eda.md`](../pressupostos/02-eda.md)).

O modelo Tobit (regressão censurada) usa a informação certa: para uma linha censurada, a verossimilhança é a probabilidade de o valor ser maior ou igual a 50, e não a densidade no 50.

## Estado atual

- 16 linhas com `MEDV = 50` em `df_t` (n = 501). Sem elas, n = 485.
- Na Parte 6, a censura só foi verificada por remoção (modelo sem `MEDV = 50`, [Seção 13](../pressupostos/05-termo-quadratico-rm.md)). Remover as linhas censuradas também gera viés, porque elas são justamente as casas mais caras.
- 5 das 28 linhas influentes do modelo final têm `MEDV = 50`, então `df_final` já perdeu parte delas.

## O que fazer

1. **Dados.** Use `df_t` (todas as 501 linhas), e não `df_final`: as linhas censuradas são o objeto da tarefa. A resposta é `logMEDV`, com limite superior $c = \log 50$. Crie a indicadora `censurado = MEDV >= 50`.
2. **Verossimilhança.** O statsmodels não tem Tobit pronto. Crie uma subclasse de `statsmodels.base.model.GenericLikelihoodModel` com parâmetros $\beta$ e $\log\sigma$ (para manter $\sigma > 0$):
   - linha não censurada: $\log \phi\big((y_i - x_i'\beta)/\sigma\big) - \log\sigma$;
   - linha censurada: $\log\big[1 - \Phi\big((c - x_i'\beta)/\sigma\big)\big]$, calculado com `scipy.stats.norm.logsf` para estabilidade numérica.
   A matriz $X$ vem de `patsy.dmatrices(formula_final, df_t)`. Use os coeficientes do MQO como ponto de partida e `method="bfgs"` ou `"newton"`.
3. **Conferir a implementação.** Ajuste o Tobit num conjunto simulado com $\beta$ conhecido e censura de cerca de 5%. Os coeficientes estimados devem ficar perto dos verdadeiros. Confira também que, sem nenhuma linha censurada, o Tobit dá os mesmos coeficientes do MQO.
4. **Comparar três ajustes** de `formula_final`:
   - MQO em `df_t` (`modelo_reduzido`, célula 116);
   - MQO em `df_t` sem as linhas com `MEDV = 50`;
   - Tobit em `df_t`.
   Mostre os coeficientes, os erros padrão e os efeitos em % ($100 \cdot (e^{\beta} - 1)$). Destaque os termos em que o Tobit muda mais, em especial `RM_c`, `I(RM_c**2)` e `logLSTAT`, que explicam as casas caras.
5. **Pressupostos.** O Tobit supõe erros normais e de variância constante. Com a heterocedasticidade da [Tarefa 01](01-heterocedasticidade.md), os coeficientes do Tobit podem ser viesados. Registre isso. Se possível, use erros padrão robustos (sanduíche) e compare.
6. **Opcional.** Validação cruzada com as mesmas partes da célula 126, usando a previsão do valor esperado observado, $E[\min(y, c) \mid x]$, convertida para `MEDV`.

## Critério de pronto

- Tobit ajustado e convergido (`mle_retvals["converged"]` igual a `True`), com a verificação do passo 3.
- Tabela comparando os três ajustes (passo 4) e um parágrafo dizendo se a censura muda as conclusões do modelo final.
- Limitações do Tobit registradas (passo 5).

## Documentação a atualizar

- Novo `docs/pressupostos/NN-tobit.md`.
- `07-pendencias.md`: linha "Censura em 50".
- `02-eda.md`, Seção 9: a linha da censura passa a citar a nova seção. Não renumere as seções.
- `README.md` (raiz): "Limitações", terceiro item.

## Referências

- Tobin, J. (1958). Estimation of relationships for limited dependent variables. *Econometrica*, 26(1), 24–36.
- Wooldridge, J. M. *Introductory Econometrics*, cap. 17 (modelos censurados).
- statsmodels: `GenericLikelihoodModel`.
