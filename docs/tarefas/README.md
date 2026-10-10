# Tarefas pendentes

Esta pasta lista o que ainda falta fazer no projeto. Cada arquivo é **uma tarefa**, escrita para que uma pessoa ou um agente de IA possa executá-la sem ler o histórico das conversas.

## Índice

| Arquivo | Tarefa | Prioridade | Situação |
|---|---|---|---|
| [`09-heterocedasticidade.md`](../pressupostos/09-heterocedasticidade.md) (registro) | Modelar a variância não constante dos erros (MQP/MQGF) | alta | feita (PR #11) |
| [`11-correlacao-espacial.md`](../pressupostos/11-correlacao-espacial.md) (registro) | Verificar a correlação entre cidades vizinhas com coordenadas | média | feita (PR #13) |
| [`10-tobit.md`](../pressupostos/10-tobit.md) (registro) | Ajustar um modelo Tobit para a censura em `MEDV = 50` | média | feita (PR #12) |
| [`07-pressupostos-pendentes.md`](07-pressupostos-pendentes.md) | Quadro do que falta para cumprir os pressupostos da RLM e fechar o projeto | alta | pendente |

As tarefas 01 a 06 e 08 foram feitas. As tarefas 04 (interação `RM × logLSTAT`), 05 (indicadora `ZN > 0`), 06 (colinearidade entre `NOX` e `logDIS`) e 08 (comparação dos modelos) não mudaram o modelo final e foram retiradas do notebook (antigas Partes 12 a 15). Falta só a tarefa 07, que usa os resultados das outras para fechar o projeto.

## Antes de começar

1. Leia `CLAUDE.md` (raiz do repositório). Ele define a língua (português) e a regra da documentação.
2. Leia [`docs/pressupostos/README.md`](../pressupostos/README.md) (índice) e [`08-modelo-final.md`](../pressupostos/08-modelo-final.md) (Seção 16). O modelo final e os números citados nas tarefas estão lá.
3. Leia só as células do notebook que a tarefa cita. O `02-MRLM.ipynb` tem mais de 120 células.

## Objetos do notebook que as tarefas usam

As funções de cálculo de VIF estão em `notebooks/01-AED.ipynb`; os outros objetos estão em `notebooks/02-MRLM.ipynb`. Os índices das células contam a partir de 0 em cada notebook.

| Objeto | Célula | O que é |
|---|---|---|
| `calcular_vif(df, colunas)`, `calcular_numero_condicao(df, colunas)` | 4 (`01-AED`) | GVIF de Fox & Monette por termo e número de condição com colunas padronizadas ([Seção 7](../pressupostos/02-eda.md) e [Seção 8](../pressupostos/02-eda.md)) |
| `perfil_boxcox(dados, lado_direito, lambdas)` | 51 | perfil de verossimilhança do λ de Box-Cox da resposta para um lado direito de fórmula |
| `df_t` | 49 | dados usados nas Partes 7 e 8: n = 501 (sem as linhas suspeitas 506 a 510 e sem `RM` ausente). Já tem `logMEDV`, `logDIS`, `logLSTAT`, `RM_c` e `logLSTAT_c` |
| `formula` | Parte 5 | fórmula do modelo linear completo, com `MEDV` na escala original |
| `formula_final` | 65 | `logMEDV ~ CRIM + C(CHAS) + NOX + logDIS + C(RAD) + PTRATIO + B + logLSTAT + RM_c + I(RM_c**2) + I(logLSTAT_c**2)` |
| `modelo_reduzido` | 65 | `formula_final` ajustada em `df_t` (todas as 501 linhas), MQO |
| `linhas_influentes(m)` | 67 | índices das linhas com Cook > 4/n ou \|DFFITS\| > 2·√(p/n) |
| `resumir_residuos(m)` | 67 | dicionário com R² ajustado, QQ, Shapiro-Wilk, Breusch-Pagan, RESET, DW e outros |
| `df_final` | 67 | `df_t` sem as 28 linhas influentes (n = 473) |
| `modelo_final` | 67 | `formula_final` em `df_final`, com `cov_type="HC3"` |
| `cidade` | 71 | grupos de cidade aproximada: `df_final.groupby(["TAX", "PTRATIO", "INDUS", "ZN"]).ngroup()` (78 grupos) |
| `prever_log(m, dados)` | 75 | previsão em mil dólares: $e^{\hat y}$ vezes o fator de smearing de Duan |
| `ajustar_mqgf(dados, forma)` | 81 | MQGF de `formula_final` com pesos $1/\exp(\hat g)$; devolve `(m_wls, aux, m_ols)`. Forma padrão: `logLSTAT` |
| `variancia_log(m_wls, aux, m_ols, dados)` | 81 | variância estimada de `log(MEDV)` em cada linha |
| `prever_log_hetero(m_wls, aux, m_ols, dados)` | 87 | previsão em mil dólares com a correção lognormal $e^{\hat y + \hat\sigma^2(x)/2}$ |
| `Tobit(endog, exog, limite, exog_var=None)` | 93 | regressão censurada (subclasse de `GenericLikelihoodModel`) com censura superior em `limite` e $\log\sigma_i$ = `exog_var` @ $\gamma$. `.fit()` devolve resultados com nomes; `.fit(cov_type="HC0")` dá erros padrão sanduíche |
| `modelo_tobit` | 97 | Tobit de `formula_final` em `df_t` (501 linhas), limite $\log 50$, variância constante |
| `prever_tobit(m, X_novo)` | 101 | previsão em mil dólares do valor observado $E[\min(MEDV, 50) \mid x]$ |
| `boston_c` | 105 | `data/boston_corrected.csv` (506 linhas, mesmo índice de `df`): `TOWN`, `TRACT`, `LON`, `LAT`, `CMEDV`. Ligue com `boston_c.loc[dados.index]` |
| `coordenadas_km(indice)` | 105 | coordenadas planas em km das linhas `indice` |
| `matrizes_vizinhanca(indice)` | 107 | dicionário com a matriz KNN (k = 6) e a de distância, padronizadas por linha |
| `W_knn` | 107 | matriz KNN (k = 6) das 473 linhas de `df_final` |
| `sem_het` | 113 | modelo de erro espacial de `formula_final` em `df_final` por GMM robusto a heterocedasticidade (`spreg.GM_Error_Het`) |
| validação cruzada | 75 | `KFold(n_splits=10, shuffle=True, random_state=42).split(df_t)`, com RMSE, MAE e R² fora da amostra |

Referência para comparar: o modelo final tem RMSE 4,00, MAE 2,75 e R² fora da amostra 0,79 na validação cruzada (Seção 16.1).

## Como trabalhar

- Atualize `main`, crie uma branch a partir dela e abra o PR para `main`.
- Cada tarefa vira uma **nova parte** no fim do notebook `02-MRLM.ipynb` (Parte 13, Parte 14, ...), com uma célula de introdução em Markdown e uma conclusão no fim. Não altere as células antigas.
- Reaproveite os objetos acima em vez de reescrever o código. Use as mesmas partes da validação cruzada para que as comparações sejam justas.
- Rode os dois notebooks do zero, nesta ordem, antes do commit: `jupyter nbconvert --to notebook --execute --inplace notebooks/01-AED.ipynb notebooks/02-MRLM.ipynb`.
- No mesmo commit: crie `docs/pressupostos/NN-assunto.md` com o próximo número livre, atualize o índice `docs/pressupostos/README.md`, a linha da tarefa em `docs/pressupostos/07-pendencias.md` e, se o resultado mudar o modelo final, as seções "Resultados" e "Limitações" do `README.md` da raiz.
- Novas referências bibliográficas vão em `docs/pressupostos/referencias.md`.

## Quando uma tarefa terminar

Mude a situação no índice acima para "feita", com o número do PR, e apague o arquivo da tarefa. O registro do que foi feito fica em `docs/pressupostos/`.
