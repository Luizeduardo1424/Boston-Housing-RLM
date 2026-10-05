# Tarefas pendentes

Esta pasta lista o que ainda falta fazer no projeto. Cada arquivo é **uma tarefa**, escrita para que uma pessoa ou um agente de IA possa executá-la sem ler o histórico das conversas.

## Índice

| Arquivo | Tarefa | Prioridade | Situação |
|---|---|---|---|
| [`09-heterocedasticidade.md`](../pressupostos/09-heterocedasticidade.md) (registro) | Modelar a variância não constante dos erros (MQP/MQGF) | alta | feita (PR #11) |
| [`02-correlacao-espacial.md`](02-correlacao-espacial.md) | Verificar a correlação entre cidades vizinhas com coordenadas | média | aberta |
| [`10-tobit.md`](../pressupostos/10-tobit.md) (registro) | Ajustar um modelo Tobit para a censura em `MEDV = 50` | média | feita (PR #12) |
| [`04-interacao-rm-lstat.md`](04-interacao-rm-lstat.md) | Testar a interação `RM × logLSTAT` | baixa | aberta |
| [`05-indicadora-zn.md`](05-indicadora-zn.md) | Testar a indicadora `ZN > 0` | baixa | aberta |

As tarefas são independentes. As tarefas 04 e 05 são curtas e podem ser feitas juntas, numa mesma parte do notebook.

## Antes de começar

1. Leia `CLAUDE.md` (raiz do repositório). Ele define a língua (português) e a regra da documentação.
2. Leia [`docs/pressupostos/README.md`](../pressupostos/README.md) (índice) e [`08-modelo-final.md`](../pressupostos/08-modelo-final.md) (Seção 16). O modelo final e os números citados nas tarefas estão lá.
3. Leia só as células do notebook que a tarefa cita. O notebook tem mais de 120 células.

## Objetos do notebook que as tarefas usam

Todos estão em `notebooks/EDA.ipynb`. Os índices das células contam a partir de 0.

| Objeto | Célula | O que é |
|---|---|---|
| `df_t` | 100 | dados usados nas Partes 7 e 8: n = 501 (sem as linhas suspeitas 506 a 510 e sem `RM` ausente). Já tem `logMEDV`, `logDIS`, `logLSTAT`, `RM_c` e `logLSTAT_c` |
| `formula` | Parte 5 | fórmula do modelo linear completo, com `MEDV` na escala original |
| `formula_final` | 116 | `logMEDV ~ CRIM + C(CHAS) + NOX + logDIS + C(RAD) + PTRATIO + B + logLSTAT + RM_c + I(RM_c**2) + I(logLSTAT_c**2)` |
| `modelo_reduzido` | 116 | `formula_final` ajustada em `df_t` (todas as 501 linhas), MQO |
| `linhas_influentes(m)` | 118 | índices das linhas com Cook > 4/n ou \|DFFITS\| > 2·√(p/n) |
| `resumir_residuos(m)` | 118 | dicionário com R² ajustado, QQ, Shapiro-Wilk, Breusch-Pagan, RESET, DW e outros |
| `df_final` | 118 | `df_t` sem as 28 linhas influentes (n = 473) |
| `modelo_final` | 118 | `formula_final` em `df_final`, com `cov_type="HC3"` |
| `cidade` | 122 | grupos de cidade aproximada: `df_final.groupby(["TAX", "PTRATIO", "INDUS", "ZN"]).ngroup()` (78 grupos) |
| `prever_log(m, dados)` | 126 | previsão em mil dólares: $e^{\hat y}$ vezes o fator de smearing de Duan |
| `ajustar_mqgf(dados, forma)` | 132 | MQGF de `formula_final` com pesos $1/\exp(\hat g)$; devolve `(m_wls, aux, m_ols)`. Forma padrão: `logLSTAT` |
| `variancia_log(m_wls, aux, m_ols, dados)` | 132 | variância estimada de `log(MEDV)` em cada linha |
| `prever_log_hetero(m_wls, aux, m_ols, dados)` | 138 | previsão em mil dólares com a correção lognormal $e^{\hat y + \hat\sigma^2(x)/2}$ |
| `Tobit(endog, exog, limite, exog_var=None)` | 144 | regressão censurada (subclasse de `GenericLikelihoodModel`) com censura superior em `limite` e $\log\sigma_i$ = `exog_var` @ $\gamma$. `.fit()` devolve resultados com nomes; `.fit(cov_type="HC0")` dá erros padrão sanduíche |
| `modelo_tobit` | 148 | Tobit de `formula_final` em `df_t` (501 linhas), limite $\log 50$, variância constante |
| `prever_tobit(m, X_novo)` | 152 | previsão em mil dólares do valor observado $E[\min(MEDV, 50) \mid x]$ |
| validação cruzada | 126 | `KFold(n_splits=10, shuffle=True, random_state=42).split(df_t)`, com RMSE, MAE e R² fora da amostra |

Referência para comparar: o modelo final tem RMSE 4,00, MAE 2,75 e R² fora da amostra 0,79 na validação cruzada (Seção 16.1).

## Como trabalhar

- Atualize `main`, crie uma branch a partir dela e abra o PR para `main`.
- Cada tarefa vira uma **nova parte** no fim do notebook (Parte 9, Parte 10, ...), com uma célula de introdução em Markdown e uma conclusão no fim. Não altere as células antigas.
- Reaproveite os objetos acima em vez de reescrever o código. Use as mesmas partes da validação cruzada para que as comparações sejam justas.
- Rode o notebook inteiro do zero antes do commit: `jupyter nbconvert --to notebook --execute --inplace notebooks/EDA.ipynb`.
- No mesmo commit: crie `docs/pressupostos/NN-assunto.md` com o próximo número livre, atualize o índice `docs/pressupostos/README.md`, a linha da tarefa em `docs/pressupostos/07-pendencias.md` e, se o resultado mudar o modelo final, as seções "Resultados" e "Limitações" do `README.md` da raiz.
- Novas referências bibliográficas vão em `docs/pressupostos/referencias.md`.

## Quando uma tarefa terminar

Mude a situação no índice acima para "feita", com o número do PR, e apague o arquivo da tarefa. O registro do que foi feito fica em `docs/pressupostos/`.
