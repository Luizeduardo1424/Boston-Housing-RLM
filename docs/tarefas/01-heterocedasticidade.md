# Tarefa 01: modelar a variância não constante dos erros

## Contexto

O modelo final (Seção 16 de [`08-modelo-final.md`](../pressupostos/08-modelo-final.md)) usa erros padrão HC3. O HC3 corrige os erros padrão, os intervalos e os testes quando a variância dos erros muda com $x$. Mas ele **não remove** a heterocedasticidade: os coeficientes continuam os do MQO, que deixam de ser os mais eficientes, e os intervalos de **previsão** continuam supondo uma variância única.

A heterocedasticidade também afeta a volta à escala de `MEDV`. O fator de smearing de Duan em `prever_log` supõe que os erros têm a mesma distribuição para todo $x$.

## Estado atual

- Breusch-Pagan no modelo final (n = 473): p ≈ 10⁻¹¹.
- Os resíduos são maiores nas casas baratas (valores ajustados baixos). Ver o gráfico escala-locação em `results/figures/diagnostico_modelo_final.png` (célula 124).
- Fator de smearing ≈ 1,015.
- Validação cruzada do modelo final: RMSE 4,00, MAE 2,75, R² 0,79.

## O que fazer

1. **Encontrar a forma da variância.** Com `modelo_final_classico` (célula 118), ajuste uma regressão auxiliar de $\log(e_i^2)$ em:
   - (a) os valores ajustados $\hat y$;
   - (b) `logLSTAT`;
   - (c) todos os preditores do modelo.
   Compare o R² dessas regressões e o p-valor do teste F. Escolha a forma mais simples que explica a variância.
2. **Ajustar MQGF (mínimos quadrados generalizados factíveis).** Os pesos são $w_i = 1 / \exp(\hat g_i)$, em que $\hat g_i$ é o valor previsto pela regressão auxiliar escolhida. Use `smf.wls(formula_final, data=df_final, weights=w).fit()`. Ajuste também com `cov_type="HC3"`, caso a forma da variância esteja errada.
3. **Verificar os resíduos ponderados.** Aplique Breusch-Pagan em $\sqrt{w_i}\,e_i$ (os resíduos ponderados, `m.wresid`). Refaça o gráfico escala-locação com esses resíduos.
4. **Comparar com o modelo final.** Monte uma tabela com os coeficientes e os erros padrão do MQO com HC3 e do MQGF. Os coeficientes devem ficar próximos. Uma mudança grande indica erro de especificação, não só heterocedasticidade.
5. **Rever a volta à escala de `MEDV`.** Com variância $\sigma^2(x)$, a previsão de `MEDV` é aproximadamente $e^{\hat y + \hat\sigma^2(x)/2}$ (se os erros forem quase normais) ou um smearing calculado por faixa de valores ajustados. Implemente uma das duas opções.
6. **Validação cruzada.** Repita a validação da célula 126 com as mesmas partes. Em cada treino, estime de novo a regressão auxiliar e os pesos. Compare RMSE, MAE e R² com o modelo final. Avalie também a cobertura dos intervalos de previsão de 95% na parte de teste (proporção de `MEDV` dentro do intervalo), com variância constante e com variância modelada.

## Critério de pronto

- Forma da variância escolhida e justificada (passo 1).
- Breusch-Pagan nos resíduos ponderados com p maior que no MQO, e o gráfico escala-locação mais plano.
- Tabela de comparação dos coeficientes (passo 4).
- RMSE na validação cruzada igual ou menor que 4,00. Se for maior, mantenha o MQO com HC3 e registre o resultado.
- Cobertura dos intervalos de previsão perto de 95% em todas as faixas de preço.

## Documentação a atualizar

- Novo `docs/pressupostos/NN-heterocedasticidade.md`: funções, pesos, pressupostos do MQGF (forma da variância correta), resultados.
- `07-pendencias.md`: linha "Erros padrão robustos (HC3)".
- `README.md` (raiz): "Limitações", primeiro item.

## Referências

- Wooldridge, J. M. *Introductory Econometrics*, cap. 8 (MQP e MQGF).
- Duan, N. (1983). Smearing estimate: a nonparametric retransformation method. *JASA*, 78(383), 605–610.
- statsmodels: `statsmodels.regression.linear_model.WLS`.
