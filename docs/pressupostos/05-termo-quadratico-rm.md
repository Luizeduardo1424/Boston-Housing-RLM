## 13. Termo quadrático de `RM` (Parte 6, células 34–46)

Células do notebook [`02-MRLM.ipynb`](../../notebooks/02-MRLM.ipynb).

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Amostra | `df.loc[:505].dropna(subset=["RM"])` | remove as linhas 506–510 e as 5 linhas com `RM` ausente: n = 501. **Não** remove os grupos O, L e I da [Seção 12](04-selecao-modelos.md) |
| Resposta | `logMEDV` = $\ln(MEDV)$ | o modelo supõe erros normais e homocedásticos na escala **log**, isto é, erros multiplicativos em `MEDV` |
| Preditores | `logDIS`, `logLSTAT`; `TAX` fora da fórmula | transformações sugeridas nas Partes 2–4 |
| Centralização | `RM_c = RM − média` (média de `df_rm`) | reduz a colinearidade entre `RM` e `RM²` (VIF de 91,7 para 1,0, pela função `variance_inflation_factor` do statsmodels, que aqui é o VIF clássico e não o GVIF da [Seção 7](02-eda.md)). Não muda o ajuste nem as previsões |
| Comparação | `anova_lm(modelo_rm_linear, modelo_rm_quad)` | teste F para **modelos aninhados**. É válido porque os dois modelos usam as mesmas 501 linhas. Supõe erros normais e homocedásticos |
| AIC | `modelo.aic` | AIC da verossimilhança **gaussiana** ($-2\ell + 2p$). Só compara modelos com a mesma resposta (`logMEDV`) e as mesmas linhas |
| Efeito por cômodo | `exp(β₁ + 2β₂(RM − média)) − 1` | efeito **percentual** sobre a **média geométrica** (mediana, se os erros forem simétricos) de `MEDV`, e não sobre a média aritmética. É uma derivada pontual, aproximada para um cômodo inteiro |
| Resíduo parcial | `resid + predict(fixar_demais(df_rm))` | construído à mão: resíduo **bruto** do modelo quadrático mais a previsão com os demais preditores fixos (média ou moda). É um gráfico de componente + resíduo; supõe que o efeito dos outros preditores é aditivo |
| Verificações | modelo sem `MEDV = 50` (n = 485) e com `I(logLSTAT_c**2)` | reajustes com a mesma fórmula; p-valores **não robustos** |

O RESET da Parte 6 usa o mesmo `power=2` e a mesma covariância não robusta da [Seção 11.6](03-modelo-completo-residuos.md).
