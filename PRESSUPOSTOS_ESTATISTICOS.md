# Pressupostos estatísticos da análise

Este documento descreve os pressupostos estatísticos assumidos em cada etapa do notebook [`notebooks/EDA.ipynb`](notebooks/EDA.ipynb). Para cada etapa, ele indica a função de biblioteca usada, os parâmetros efetivamente aplicados (inclusive os padrões implícitos) e o que cada resultado permite ou não concluir.

Versões usadas na execução do notebook (`.venv`): pandas 3.0.6, numpy 2.5.3, scipy 1.18.1, statsmodels 0.15.0, seaborn 0.13.2.

---

## 1. Situação atual: nenhum modelo foi ajustado

O notebook atual é uma **análise exploratória**. Ele **não ajusta nenhum modelo de regressão**: não há `sm.OLS(...).fit()`, `smf.ols` nem `LinearRegression`. Por isso:

- **não foram calculados resíduos**, nem os resíduos brutos (padrão) nem os padronizados ou studentizados;
- **nenhum pressuposto do modelo de regressão foi testado ainda**. Normalidade dos erros, homocedasticidade, independência, linearidade condicional e pontos influentes dependem dos resíduos de um modelo ajustado;
- as medidas de assimetria, curtose, LOWESS e correlação descritas abaixo se referem às **distribuições marginais** das variáveis, e não aos erros do modelo.

O modelo de RLM supõe

$$
Y = X\beta + \varepsilon,\qquad \varepsilon \sim N(0, \sigma^2 I),
$$

ou seja, média linear em $X$, erros independentes, variância constante e normalidade (esta última necessária para os testes t e F exatos). A EDA só fornece **indícios** sobre esses pontos. A verificação formal fica para a etapa de modelagem (ver Seção 10).

---

## 2. Tipagem das variáveis (célula 3)

| Variável | Tratamento | Código | Consequência |
|---|---|---|---|
| `CHAS` | categórica nominal (binária) | `astype("category")` | Fora da correlação de Pearson e de Spearman. No VIF entra como 1 indicadora (referência `CHAS = 0`). |
| `RAD` | categórica **ordinal** (9 níveis: 1–8 e 24) | `astype(pd.CategoricalDtype(ordered=True))` | Fora de Pearson. Em Spearman entra por `cat.codes` (0–8), o que supõe **apenas a ordem** dos níveis e não a distância entre eles. No VIF entra como 8 indicadoras (referência `RAD = 1`). |
| Demais | numéricas contínuas | `float64` / `int64` (`TAX`) | Tratadas como contínuas em todas as etapas. |

Pressuposto implícito: a distância de 8 para 24 em `RAD` não é interpretável como medida. Por isso não se ajusta uma inclinação única para `RAD`.

---

## 3. Análise univariada (células 4, 24–26)

| Medida | Função | Definição efetiva | Referência sob normalidade |
|---|---|---|---|
| Assimetria | `Series.skew()` (pandas) | coeficiente de Fisher–Pearson **ajustado** $G_1$, com correção de viés amostral | 0 |
| Curtose | `Series.kurt()` (pandas) | curtose **em excesso**, com correção de viés (Fisher) | **0** (e não 3) |
| Densidade | `sns.histplot(kde=True)` | KDE gaussiano, largura de banda pela regra de **Scott** (`bw_method='scott'`, `bw_adjust=1`) | — |

Observações:

- Os valores ausentes são ignorados (`skipna=True`); em `RM`, as medidas usam 506 observações.
- Assimetria e curtose são **descritivas**. Nenhum teste formal de normalidade (Shapiro–Wilk, Jarque–Bera, Anderson–Darling) foi aplicado.
- A normalidade **marginal** de `MEDV` ou de `logMEDV` **não é pressuposto** da RLM. O pressuposto é sobre os **erros** condicionais a $X$. A simetria de `logMEDV` é só um indício de que essa escala pode produzir resíduos mais próximos da normal.

Transformações (célula 25):

| Variável nova | Função | Motivo |
|---|---|---|
| `logCRIM`, `logZN` | `np.log1p(x)` = $\ln(1+x)$ | admite zeros (`ZN` tem muitos zeros) |
| `logDIS`, `logLSTAT`, `logMEDV` | `np.log(x)` | variáveis estritamente positivas |

`log1p` não é exatamente um logaritmo para valores pequenos ($\ln(1+x) \approx x$ quando $x \to 0$). Em `CRIM`, cujos valores são em sua maioria menores que 1, a transformação é mais fraca que $\ln(x)$.

---

## 4. Linearidade exploratória (células 29–30)

Função: `sns.regplot(..., lowess=True)`. O seaborn chama `statsmodels.nonparametric.smoothers_lowess.lowess(y, x)` **com os parâmetros padrão**:

| Parâmetro | Valor | Significado |
|---|---|---|
| `frac` | 2/3 | cada ajuste local usa 2/3 das observações (curva bastante suave) |
| `it` | 3 | 3 iterações **robustas** (pesos bisquare), que reduzem o peso de valores extremos |
| intervalo de confiança | não desenhado | o seaborn não calcula IC quando `lowess=True` |
| ausentes | removidos | linhas com `NaN` em `x` ou `y` são descartadas |

Limitações:

- A curva mostra a relação **marginal** (bivariada) entre `MEDV` e cada preditor. A RLM supõe linearidade **condicional** aos demais preditores, que só pode ser avaliada com gráficos de resíduos parciais (CCPR) ou de resíduos contra valores ajustados.
- Por ser robusta, a LOWESS pode suavizar o efeito dos valores censurados em `MEDV = 50` e das 5 linhas suspeitas, que ainda assim afetam um ajuste por MQO.

---

## 5. Comparação entre grupos (células 32 e 34)

| Teste | Função | Configuração efetiva | Pressupostos |
|---|---|---|---|
| Mann–Whitney U (`MEDV` por `CHAS`) | `scipy.stats.mannwhitneyu(x, y, alternative='two-sided')` | `method='auto'`: com ties e amostras grandes (35 e 476), usa a **aproximação normal assintótica** com correção de ties e **correção de continuidade** (`use_continuity=True`) | observações independentes. Para interpretar como diferença de **medianas**, as duas distribuições devem ter a mesma forma. Sem isso, o teste compara $P(X > Y)$ com 1/2. |
| Kruskal–Wallis H (`MEDV` por `RAD`) | `scipy.stats.kruskal(*grupos)` | H com correção de ties; p-valor pela **aproximação $\chi^2$** com $k-1 = 8$ GL | observações independentes e mesma forma de distribuição entre grupos (para leitura como medianas). A aproximação $\chi^2$ pede grupos com pelo menos ~5 observações; o menor tem 17 (`RAD = 7`). |

Os testes não paramétricos foram escolhidos porque `MEDV` é assimétrica e censurada. A censura em 50 gera **ties** (16 valores iguais), tratados pela correção de ties dos dois testes. Nenhum teste de comparações múltiplas (p. ex. Dunn) foi feito após o Kruskal–Wallis, então não se sabe **quais** níveis de `RAD` diferem entre si.

---

## 6. Correlação (células 38 e 40)

| Medida | Função | Pressuposto / interpretação |
|---|---|---|
| Pearson | `DataFrame.corr()` (padrão `method='pearson'`) | mede associação **linear**, é sensível a valores extremos e assimetria |
| Spearman | `DataFrame.corr(method='spearman')` | mede associação **monotônica** (correlação de Pearson dos postos); com ties, usa postos médios |

Tratamento de ausentes: `DataFrame.corr` usa **exclusão par a par** (cada par usa as linhas em que ambas as variáveis existem). O VIF usa **exclusão por lista** (`dropna`), então as duas análises não usam exatamente as mesmas linhas (511 linhas, ou 506 nos pares com `RM`, contra 506).

As matrizes também incluem as colunas transformadas e `MEDV`. Isso é útil na leitura, mas `MEDV` não participa do diagnóstico de multicolinearidade.

---

## 7. Multicolinearidade: VIF generalizado (células 4, 43–46)

O VIF **não** é calculado com `statsmodels.stats.outliers_influence.variance_inflation_factor`. A função própria `calcular_vif` implementa o **GVIF** de Fox & Monette (1992):

$$
\text{GVIF}_j = \frac{\det(R_{jj})\,\det(R_{-j,-j})}{\det(R)}
$$

onde $R$ é a matriz de correlação das colunas da matriz de design (sem intercepto), $R_{jj}$ é o bloco das colunas do termo $j$ e $R_{-j,-j}$ é o bloco das demais.

| Aspecto | Detalhe |
|---|---|
| Codificação | categóricas viram $k-1$ indicadoras (`pd.get_dummies(drop_first=True)`); referências `CHAS = 0` e `RAD = 1` |
| Equivalência | para termos com 1 GL, o GVIF é **igual** ao VIF clássico $1/(1-R_j^2)$ (conferido contra o statsmodels) |
| Comparação entre termos | $\text{GVIF}^{1/(2\cdot GL)}$, comparável a $\sqrt{\text{VIF}}$ |
| Limiares | 2,24 (≈ VIF 5) e 3,16 (≈ VIF 10) |
| Invariância | o GVIF não depende da categoria de referência escolhida |
| Ausentes | `dropna` (exclusão por lista) |

Pressuposto: o VIF mede apenas **dependência linear** entre preditores, e não mede relações não lineares. Como usa correlações amostrais, também é sensível às 5 observações suspeitas.

---

## 8. Número de condição (células 4 e 48)

Função própria `calcular_numero_condicao`:

1. aplica `pd.get_dummies(drop_first=True)` aos preditores;
2. **padroniza** cada coluna ($z = (x - \bar x)/s$);
3. adiciona o intercepto (`statsmodels.tools.tools.add_constant`);
4. calcula `np.linalg.cond`: norma 2, razão entre o maior e o menor valor singular.

O resultado é comparado com o limiar **30** de Belsley, Kuh & Welsch (1980).

Atenção: BKW propõem escalar as colunas para comprimento unitário **sem centralizar**, para que a colinearidade com o intercepto também apareça. Aqui as colunas são **centralizadas**, então o intercepto fica ortogonal aos demais preditores e o número mede só a colinearidade **entre os preditores**. Os valores obtidos (11–13) não são diretamente comparáveis ao número de condição que o `summary()` do statsmodels mostra (calculado sobre a matriz não padronizada).

---

## 9. Características dos dados que afetam os pressupostos

| Característica | Pressuposto afetado | Situação |
|---|---|---|
| `MEDV` censurada em 50 (16 obs.) | média linear e erros normais na parte superior; os resíduos tendem a ser negativos nessa faixa | identificada, sem tratamento |
| 5 linhas suspeitas (índices 506–510) | todas as estimativas por momentos (assimetria, Pearson, VIF, MQO) | mantidas e sinalizadas |
| 5 `RM` ausentes | número de observações e comparabilidade entre análises | mantidas; cada etapa exclui de forma diferente |
| `ZN` com excesso de zeros | linearidade da relação com `MEDV` | sugerida indicadora `ZN > 0` |
| `TAX` = 666 em todos os `RAD = 24` | multicolinearidade (GVIF de `TAX` ≈ 9,90) | decisão pendente |
| Dados geográficos (setores censitários) | **independência** dos erros: setores vizinhos tendem a ter erros correlacionados (autocorrelação espacial) | não avaliada |

---

## 10. Pendente para a etapa de modelagem

> Esta seção é uma **recomendação**. Nada aqui foi executado no notebook atual.

### 10.1 Tipos de resíduo disponíveis no statsmodels

Com `res = sm.OLS(y, X).fit()` e `infl = res.get_influence()`:

| Resíduo | Acesso | Definição | Uso indicado |
|---|---|---|---|
| Bruto (padrão) | `res.resid` | $e_i = y_i - \hat y_i$ | gráficos gerais. É o resíduo usado pelo `summary()` (Omnibus, Jarque–Bera, Durbin–Watson) e pelo `het_breuschpagan`. |
| Studentizado **interno** (padronizado) | `infl.resid_studentized_internal` | $r_i = e_i / (\hat\sigma\sqrt{1-h_{ii}})$ | QQ-plot e scale-location, porque corrige a variância desigual causada pela alavancagem |
| Studentizado **externo** | `infl.resid_studentized_external` | $t_i = e_i / (\hat\sigma_{(i)}\sqrt{1-h_{ii}})$, segue $t_{n-p-1}$ | detecção de outliers: $\lvert t_i\rvert > 3$, ou `res.outlier_test()` com correção de Bonferroni |

Os resíduos brutos **não** têm variância constante mesmo quando o modelo é correto ($\text{Var}(e_i) = \sigma^2(1-h_{ii})$). Por isso, os diagnósticos gráficos e de outliers devem usar os resíduos studentizados.

### 10.2 Verificações sugeridas por pressuposto

| Pressuposto | Gráfico | Teste | Função |
|---|---|---|---|
| Linearidade | resíduos × ajustados; resíduos parciais (CCPR) | RESET de Ramsey | `sm.graphics.plot_ccpr_grid`, `statsmodels.stats.diagnostic.linear_reset` |
| Homocedasticidade | scale-location ($\sqrt{\lvert r_i\rvert}$ × ajustados) | Breusch–Pagan / White | `het_breuschpagan`, `het_white` |
| Normalidade | QQ-plot dos studentizados | Shapiro–Wilk, Jarque–Bera | `sm.qqplot`, `scipy.stats.shapiro`, `summary()` |
| Independência | resíduos × ordem / mapa | Durbin–Watson (pouco informativo em dados transversais, porque depende da ordem das linhas) | `summary()` |
| Pontos influentes | resíduos × alavancagem | $h_{ii} > 2p/n$; Cook $D_i > 4/n$; DFFITS; DFBETAS | `infl.hat_matrix_diag`, `infl.cooks_distance`, `sm.graphics.influence_plot` |
| Multicolinearidade | — | GVIF (Seção 7) | `calcular_vif` |

### 10.3 Inferência

- O `summary()` do statsmodels usa por padrão erros-padrão de MQO **não robustos** (`cov_type='nonrobust'`), que só são válidos sob homocedasticidade.
- Se o Breusch–Pagan indicar heterocedasticidade, usar `fit(cov_type='HC3')`.
- Os testes t e F supõem normalidade dos erros. Com $n \approx 500$, eles são aproximadamente válidos por argumento assintótico mesmo com desvios moderados.
- A censura em 50 viola o modelo linear na parte superior. As alternativas são remover essas observações (com justificativa), usar um modelo Tobit ou registrar a limitação na interpretação.

---

## Referências

- Belsley, D. A.; Kuh, E.; Welsch, R. E. (1980). *Regression Diagnostics: Identifying Influential Data and Sources of Collinearity*. Wiley.
- Fox, J.; Monette, G. (1992). Generalized collinearity diagnostics. *Journal of the American Statistical Association*, 87(417), 178–183.
- Montgomery, D. C.; Peck, E. A.; Vining, G. G. (2012). *Introduction to Linear Regression Analysis*. 5. ed. Wiley.
- Cleveland, W. S. (1979). Robust locally weighted regression and smoothing scatterplots. *Journal of the American Statistical Association*, 74(368), 829–836.
- Documentação: [pandas `Series.skew`/`kurt`](https://pandas.pydata.org/docs/reference/api/pandas.Series.skew.html), [scipy `mannwhitneyu`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html), [scipy `kruskal`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html), [statsmodels `OLSInfluence`](https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.OLSInfluence.html).
