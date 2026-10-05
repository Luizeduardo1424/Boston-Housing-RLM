# Pressupostos estatísticos da análise

Este documento descreve os pressupostos estatísticos assumidos em cada etapa do notebook [`notebooks/EDA.ipynb`](notebooks/EDA.ipynb). Para cada etapa, ele indica a função de biblioteca usada, os parâmetros efetivamente aplicados (inclusive os padrões implícitos) e o que cada resultado permite ou não concluir. Os números de célula são os índices do notebook (contados a partir de 0).

Versões usadas na execução do notebook (`.venv`): pandas 3.0.6, numpy 2.5.3, scipy 1.18.1, statsmodels 0.15.0, seaborn 0.13.2. Os parâmetros padrão citados foram conferidos no código-fonte dessas versões.

---

## 1. Visão geral

O modelo de RLM supõe

$$
Y = X\beta + \varepsilon,\qquad \varepsilon \sim N(0, \sigma^2 I),
$$

ou seja: média linear em $X$, erros independentes, variância constante e normalidade (esta última necessária para que os testes t e F sejam exatos).

O notebook tem duas fases:

- **Partes 1 a 4 (EDA, células 0–52):** descrevem as **distribuições marginais** das variáveis. Elas não usam resíduos e só fornecem **indícios** sobre os pressupostos (Seções 2 a 8).
- **Partes 5 a 7 (modelos, células 53–113):** ajustam modelos por MQO com `statsmodels` e verificam os pressupostos com os **resíduos** (Seções 10 a 15).

### 1.1 Qual resíduo é usado em cada lugar

O notebook usa **três tipos de resíduo**, e cada diagnóstico usa um tipo diferente:

| Nome no notebook | Acesso (statsmodels) | Definição |
|---|---|---|
| Resíduo | `modelo.resid` | bruto: $e_i = y_i - \hat y_i$ |
| Res. padronizado ($r_i$) | `get_influence().resid_studentized_internal` | studentizado **interno**: $r_i = e_i / (\hat\sigma\sqrt{1-h_{ii}})$ |
| Res. studentizado ($t_i$) | `get_influence().resid_studentized_external` | studentizado **externo**: $t_i = e_i / (\hat\sigma_{(i)}\sqrt{1-h_{ii}})$, com $\hat\sigma_{(i)}$ estimado sem a observação $i$ e $t_i \sim t_{n-p-1}$ |

| Diagnóstico | Resíduo usado | Célula |
|---|---|---|
| Shapiro-Wilk, Jarque-Bera, Anderson-Darling, assimetria e curtose dos resíduos | **bruto** | 70 |
| Gráfico QQ, envelope simulado e correlação do gráfico QQ | **studentizado externo** | 70 |
| Faixa $2 < \lvert r \rvert \le 3$, teste binomial, gráficos por índice e por valor ajustado | **studentizado interno** | 67–68 |
| $\lvert t \rvert > 3$ e teste de Bonferroni (`outlier_test`) | **studentizado externo** | 64 |
| Distância de Cook | calculada com o **interno** | 59 |
| DFFITS | calculado com o **externo** | 59 |
| Teste das sequências, Durbin-Watson, Breusch-Pagan, RESET, resíduos × ajustados (LOWESS) | **bruto** | 67, 72 |
| Alavanca × resíduo (gráfico) | **studentizado externo** | 62 |
| Análise de sensibilidade (`resumir`): Shapiro-Wilk | **bruto** | 76 |
| Seleção de modelos (`avaliar`): Shapiro-Wilk e correlação QQ | **studentizado externo** | 80 |
| Seleção de modelos (`avaliar`): faixa 2–3 e teste binomial | **studentizado interno** | 80 |
| Parte 6: resíduos médios por faixa, resíduo parcial | **bruto** (escala log) | 94, 96 |

> **Atenção à comparação.** O Shapiro-Wilk da Seção 5.6 (W = 0,78) usa o resíduo **bruto**, e o da seleção de modelos (W = 0,73 no modelo completo) usa o **studentizado externo**. Os dois valores de W se referem ao mesmo modelo, mas não são comparáveis entre si. Dentro de cada tabela, a comparação entre modelos é consistente.

Por que isso importa: o resíduo bruto **não** tem variância constante mesmo quando o modelo é correto ($\text{Var}(e_i) = \sigma^2(1-h_{ii})$). Os resíduos studentizados corrigem isso e são a escala adequada para os gráficos e para os cortes $\lvert r \rvert > 2$ e $\lvert t \rvert > 3$. Para os testes de normalidade, a diferença é pequena quando $h_{ii}$ é pequeno, mas cresce com pontos de alavanca alta, como a observação 509 ($h = 0{,}32$).

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
- Assimetria e curtose são **descritivas**. Nenhum teste formal de normalidade foi aplicado às variáveis. Os testes de normalidade são aplicados aos **resíduos**, na Parte 5 (Seção 11.5).
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

- A curva mostra a relação **marginal** (bivariada) entre `MEDV` e cada preditor. A RLM supõe linearidade **condicional** aos demais preditores, que só pode ser avaliada com os resíduos do modelo: resíduos × ajustados e RESET na Parte 5 (Seção 11.6) e resíduo parcial de `RM` na Parte 6 (Seção 13).
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

| Característica | Pressuposto afetado | Situação no notebook |
|---|---|---|
| `MEDV` censurada em 50 (16 obs.) | média linear e erros normais na parte superior. O valor real pode ser maior que 50, então os resíduos dessas linhas são grandes e **positivos** (o modelo prevê 16–30 em 365–372) e as inclinações tendem a ser **atenuadas** | identificada. Na Parte 6, só como verificação (modelo sem `MEDV = 50`); o modelo censurado (Tobit) não foi ajustado |
| 5 linhas suspeitas (índices 506–510) | todas as estimativas por momentos (assimetria, Pearson, VIF, MQO) | mantidas no modelo completo, removidas na sensibilidade (5.9), na seleção (grupo S) e na Parte 6 |
| 5 `RM` ausentes | número de observações e comparabilidade entre análises | excluídas por linha (`dropna`) em todos os modelos |
| `ZN` com excesso de zeros | linearidade da relação com `MEDV` | indicadora `ZN > 0` sugerida, não usada |
| `TAX` = 666 em todos os `RAD = 24` | multicolinearidade (GVIF de `TAX` ≈ 9,90) | `TAX` fica no modelo completo e sai da base da Parte 6 |
| Dados geográficos, arquivo ordenado por região | **independência** dos erros | rejeitada: teste das sequências z = −8,11; Durbin-Watson 0,95 (Seção 11.4) |

---

## 10. Modelo completo (Parte 5, células 53–57)

### 10.1 Especificação

| Aspecto | Código | O que fica implícito |
|---|---|---|
| Ajuste | `smf.ols(formula, data=df_modelo).fit()` | MQO com intercepto (a fórmula do patsy inclui o intercepto) |
| Fatores | `C(CHAS)`, `C(RAD)` | codificação de **tratamento**: a referência é o primeiro nível (`CHAS = 0`, `RAD = 1`). O efeito de cada indicadora é a diferença para a referência |
| Ausentes | `df[colunas_modelo].dropna()` | exclusão por lista: n = 506 (5 linhas com `RM` ausente saem) |
| Tamanho | `p = df_model + 1` | p = 21 (20 coeficientes + intercepto), 485 GL no resíduo, 24 observações por parâmetro |
| Escala | `MEDV` sem transformação | a assimetria de `MEDV` e a censura em 50 passam para os resíduos |

### 10.2 Inferência: erros padrão não robustos

`modelo.summary()`, `modelo.bse`, `modelo.pvalues`, `modelo.conf_int()` (IC 95% pela distribuição $t_{485}$) e o teste F global usam o padrão **`cov_type='nonrobust'`**:

$$
\widehat{\text{Var}}(\hat\beta) = \hat\sigma^2 (X'X)^{-1}.
$$

Essa fórmula **supõe erros homocedásticos e independentes**. O próprio notebook rejeita os dois pressupostos depois (Breusch-Pagan p ≈ 5 × 10⁻⁸; Durbin-Watson 0,95). Portanto, **todos os p-valores e intervalos de confiança das Partes 5 e 6 são aproximados e provavelmente otimistas** (erros padrão subestimados). As conclusões recomendam erros padrão robustos (HC3), mas eles **não foram aplicados** em nenhuma célula.

### 10.3 ANOVA tipo II

`anova_lm(modelo, typ=2)` calcula a soma de quadrados de **tipo II**: cada termo é testado depois de todos os outros termos que não o contêm. Isso permite testar `C(RAD)` como **bloco** de 8 indicadoras (teste F parcial com 8 GL). Como não há interações no modelo, o tipo II é igual ao teste "último termo a entrar" e não depende da ordem da fórmula. O teste usa a mesma covariância não robusta da Seção 10.2.

---

## 11. Diagnóstico dos resíduos (Parte 5, células 58–74)

### 11.1 Medidas por observação (célula 59)

| Medida | Código | Corte usado | Observação |
|---|---|---|---|
| Alavanca $h_{ii}$ | `influencia.hat_matrix_diag` | $2p/n = 0{,}083$ e $3p/n = 0{,}125$ | soma de $h_{ii}$ = p (verificado na célula) |
| Cook $D_i$ | `influencia.cooks_distance[0]` | $4/n$ e $1$ | statsmodels calcula $D_i = r_i^2\,h_{ii} / [p\,(1-h_{ii})]$ com o resíduo **interno**. O índice `[1]` (não usado) traz p-valores pela distribuição F |
| DFFITS | `influencia.dffits[0]` | $2\sqrt{p/n}$ | statsmodels calcula $t_i\sqrt{h_{ii}/(1-h_{ii})}$ com o resíduo **externo**. O índice `[1]` traz o mesmo corte $2\sqrt{p/n}$ |

Os cortes $4/n$, $2p/n$ e $2\sqrt{p/n}$ são **regras práticas** e não testes: com n = 506, sempre haverá observações acima deles.

### 11.2 Outliers (célula 64)

- $\lvert t_i \rvert > 3$ usa o resíduo **studentizado externo**.
- A quantidade esperada ($n \cdot 2P(Z > 3) \approx 1{,}4$) usa a **normal padrão**. O resíduo externo segue $t_{n-p-1} = t_{484}$, mas a diferença é desprezível com 484 GL.
- `modelo.outlier_test(method="bonf")`: p-valor bilateral de cada $t_i$ pela distribuição $t$ com `df_resid − 1` = 484 GL, multiplicado por n (Bonferroni, `multipletests`). Supõe **erros normais**: com caudas pesadas, como aqui, o teste aponta mais outliers.

### 11.3 Faixa $2 < \lvert r \rvert \le 3$ (célula 67)

- Usa o resíduo **studentizado interno**. A probabilidade de referência (4,3%) vem da normal padrão. O resíduo interno não é exatamente normal (é limitado a $\lvert r_i \rvert \le \sqrt{n-p}$), mas a aproximação é boa com n = 506.
- `stats.binomtest(k, n, p)`: teste binomial **exato e bilateral** (padrão `alternative='two-sided'`). Supõe que as n observações caiam na faixa de forma **independente**, o que é discutível porque os resíduos são correlacionados (matriz $I - H$) e há autocorrelação.
- O notebook observa que poucos pontos na faixa não indicam bom ajuste: os outliers extremos inflam $\hat\sigma$ e reduzem todos os $r_i$.

### 11.4 Independência (células 67 e 72)

| Teste | Código | Detalhe |
|---|---|---|
| Sequências | `runstest_1samp(np.sign(modelo.resid.values), cutoff=0)` | resíduo **bruto**. O indicador é `x >= 0`, e as sequências são contadas na **ordem do arquivo**. Usa a aproximação normal (z) |
| Durbin-Watson | `durbin_watson(modelo.resid)` | resíduo **bruto**, na ordem do arquivo; mede autocorrelação de 1ª ordem (≈ 2 = ausente) |

Os dois testes **só fazem sentido se a ordem das linhas tiver significado**. Aqui o arquivo está ordenado por região, então eles detectam **dependência espacial** entre regiões vizinhas. Se as linhas fossem embaralhadas, os dois testes deixariam de detectar essa dependência, mas ela continuaria existindo. Um teste espacial (I de Moran com coordenadas) seria a verificação direta, e não foi feito.

### 11.5 Normalidade (célula 70)

| Elemento | Detalhe |
|---|---|
| Quantis teóricos | posições de **Blom**: $\Phi^{-1}\!\left(\frac{i - 0{,}375}{n + 0{,}25}\right)$ |
| Pontos do gráfico | resíduo **studentizado externo** ordenado |
| Envelope | 100 amostras **iid** $N(0,1)$ de tamanho n (`default_rng(42)`), bandas **pontuais** de 2,5% e 97,5% |
| Correlação do gráfico QQ | `np.corrcoef(quantis, resíduos ordenados)`. Filliben (1975) usa as medianas das estatísticas de ordem; com as posições de Blom, o valor é praticamente o mesmo |
| Shapiro-Wilk | `stats.shapiro(modelo.resid)`, resíduo **bruto** |
| Jarque-Bera | `stats.jarque_bera(modelo.resid)`, resíduo **bruto**, aproximação $\chi^2_2$ assintótica |
| Anderson-Darling | `stats.anderson(modelo.resid, dist="norm", method="interpolate")`, resíduo **bruto**. O p-valor é **interpolado** na tabela de valores críticos, então fica limitado aos extremos da tabela ("≤ 0,01") |
| Assimetria e curtose | `stats.skew` e `stats.kurtosis` com o padrão **`bias=True`** (sem correção de viés). Na EDA, o pandas usa a versão **corrigida**; os dois valores não são comparáveis diretamente |

Limitações do envelope:

- Ele é uma **simplificação** do envelope de Atkinson (1985). As amostras são iid, mas os resíduos do modelo são correlacionados ($I - H$) e não têm exatamente a distribuição $N(0,1)$. O envelope de Atkinson simula novas respostas a partir do modelo ajustado, reajusta o modelo e calcula os resíduos de novo.
- As bandas são **pontuais**: mesmo com resíduos normais, espera-se que cerca de 5% dos pontos fiquem fora. Por isso, os 78% fora do envelope indicam um desvio real, mas um valor próximo de 5% não seria evidência contra a normalidade.

### 11.6 Linearidade e homocedasticidade (célula 72)

| Teste | Código | Detalhe e pressupostos |
|---|---|---|
| Resíduos × ajustados | `sns.regplot(x=fittedvalues, y=resid, lowess=True)` | resíduo **bruto**. LOWESS robusta com `frac=2/3` e `it=3` (padrões, Seção 4) |
| RESET de Ramsey | `linear_reset(modelo, power=2, use_f=True)` | acrescenta **apenas** $\hat y^2$ (o padrão do statsmodels é `power=3`, que acrescenta $\hat y^2$ e $\hat y^3$). Teste F com covariância **não robusta** (`cov_type='nonrobust'`). Detecta curvatura em função de $\hat y$, mas não diz qual variável a causa |
| Breusch-Pagan | `het_breuschpagan(modelo.resid, modelo.model.exog)` | resíduo **bruto**. O padrão `robust=True` usa a versão de **Koenker** (LM = $n R^2$ da regressão de $e^2$ sobre as colunas), que **não supõe erros normais**. As variáveis auxiliares são as próprias colunas do modelo, inclusive as indicadoras. O notebook usa o LM e seu p-valor $\chi^2_{20}$ |

---

## 12. Análise de sensibilidade e seleção de modelos (células 75–84)

### 12.1 Sensibilidade sem as linhas suspeitas (célula 76)

O modelo é reajustado sem os índices 506–510 (n = 501). A função `resumir` usa o resíduo **bruto** no Shapiro-Wilk, o interno na faixa 2–3 e o externo em $\lvert t \rvert > 3$. O corte de alavanca usa o mesmo p e o n de cada modelo.

### 12.2 Seleção entre 16 combinações de remoção (células 80–84)

| Aspecto | Detalhe |
|---|---|
| Grupos | S (506–510), O ($\lvert t \rvert > 3$), L ($h > 2p/n$), I (Cook $> 4/n$ ou $\lvert DFFITS \rvert > 2\sqrt{p/n}$), marcados **uma única vez** no modelo completo (sem iterar) |
| Métricas (`avaliar`) | correlação QQ e Shapiro-Wilk com o resíduo **externo**; faixa 2–3 e binomial com o **interno**; Bonferroni (externo); Breusch-Pagan, RESET e Durbin-Watson com o **bruto**; significância pela ANOVA tipo II |
| Nota final | média de três postos com **pesos iguais** (R² ajustado, resíduos, significância). Os pesos e a composição do posto de resíduos são escolhas do trabalho, e não um critério estatístico padrão |
| Limite | candidatos que removem mais de 10% de n saem da escolha (nenhum saiu: máximo de 8,7%) |

Pressupostos e limitações:

- **Inferência após seleção.** As linhas foram removidas **com base nos próprios resíduos** do modelo. Por isso, os p-valores, os erros padrão, o F e o R² dos modelos reduzidos são **otimistas**: não levam em conta que a amostra foi escolhida para se ajustar bem. Isso vale principalmente para os grupos O e I.
- **R² de amostras diferentes.** Retirar linhas com resíduo grande sempre aumenta o R², e os R² de amostras diferentes não são estritamente comparáveis (o notebook já registra esse cuidado).
- **Validade externa.** Com exceção de 506–510, as linhas removidas são regiões reais. O modelo S+I descreve as regiões "típicas" e não deve ser usado para prever as regiões removidas.
- Os testes de cada candidato continuam usando a covariância **não robusta** (Seção 10.2).

---

## 13. Termo quadrático de `RM` (Parte 6, células 85–97)

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Amostra | `df.loc[:505].dropna(subset=["RM"])` | remove as linhas 506–510 e as 5 linhas com `RM` ausente: n = 501. **Não** remove os grupos O, L e I da Seção 12 |
| Resposta | `logMEDV` = $\ln(MEDV)$ | o modelo supõe erros normais e homocedásticos na escala **log**, isto é, erros multiplicativos em `MEDV` |
| Preditores | `logDIS`, `logLSTAT`; `TAX` fora da fórmula | transformações sugeridas nas Partes 2–4 |
| Centralização | `RM_c = RM − média` (média de `df_rm`) | reduz a colinearidade entre `RM` e `RM²` (VIF de 91,7 para 1,0, pela função `variance_inflation_factor` do statsmodels, que aqui é o VIF clássico e não o GVIF da Seção 7). Não muda o ajuste nem as previsões |
| Comparação | `anova_lm(modelo_rm_linear, modelo_rm_quad)` | teste F para **modelos aninhados**. É válido porque os dois modelos usam as mesmas 501 linhas. Supõe erros normais e homocedásticos |
| AIC | `modelo.aic` | AIC da verossimilhança **gaussiana** ($-2\ell + 2p$). Só compara modelos com a mesma resposta (`logMEDV`) e as mesmas linhas |
| Efeito por cômodo | `exp(β₁ + 2β₂(RM − média)) − 1` | efeito **percentual** sobre a **média geométrica** (mediana, se os erros forem simétricos) de `MEDV`, e não sobre a média aritmética. É uma derivada pontual, aproximada para um cômodo inteiro |
| Resíduo parcial | `resid + predict(fixar_demais(df_rm))` | construído à mão: resíduo **bruto** do modelo quadrático mais a previsão com os demais preditores fixos (média ou moda). É um gráfico de componente + resíduo; supõe que o efeito dos outros preditores é aditivo |
| Verificações | modelo sem `MEDV = 50` (n = 485) e com `I(logLSTAT_c**2)` | reajustes com a mesma fórmula; p-valores **não robustos** |

O RESET da Parte 6 usa o mesmo `power=2` e a mesma covariância não robusta da Seção 11.6.

---

## 14. Transformações, centralização e erros robustos (Parte 7, células 98–113)

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Amostra | `df_t = df_rm.copy()` | a mesma da Parte 6 (n = 501). Todas as especificações usam as mesmas linhas, então os testes são comparáveis |
| Padronização | `(X − média) / desvio padrão` (`std` do pandas, `ddof=1`) nos 11 preditores numéricos | `CHAS` e `RAD` ficam como indicadoras. É uma mudança afim das colunas: o espaço gerado por $X$ (com intercepto) é o mesmo, então $\hat y$ e os resíduos são idênticos (`np.allclose`) |
| Box-Cox da resposta | `perfil_boxcox` (célula 102), feita à mão | perfil de verossimilhança $\ell(\lambda) = -\tfrac n2 \log(SQR(\lambda)/n)$ com a resposta dividida por $\dot y^{\lambda-1}$ (média geométrica), em uma grade de −0,6 a 1 com passo 0,01. IC 95% pela razão de verossimilhança ($\chi^2_1$). Supõe que existe um $\lambda$ com erros normais e homocedásticos. Calculado para dois conjuntos de preditores, pois $\hat\lambda$ depende de $X$ |
| Box-Cox marginal | `stats.boxcox(MEDV)` | $\lambda$ da distribuição de `MEDV` **sem** preditores. Só para comparação: o pressuposto é sobre os erros, não sobre $Y$ |
| Preditores | `stats.boxcox` (valores > 0) ou `stats.yeojohnson` (`ZN`, com zeros) | $\lambda$ por máxima verossimilhança da distribuição **marginal** de cada preditor. É um guia de simetria; a RLM não supõe preditores normais |
| Comparação | `diagnosticar` (célula 106) | correlação QQ e Shapiro-Wilk com o resíduo **externo**; assimetria, curtose, Breusch-Pagan, RESET e Durbin-Watson com o **bruto** (iguais aos da Seção 11). AIC só entre modelos com a mesma resposta |
| Fonte da heterocedasticidade | `ols("e2 ~ ...").wald_test_terms()` | regressão auxiliar de $e^2$ sobre os termos do modelo E, com teste F de cada termo (covariância não robusta). Indica **quais** termos explicam a variância; não é o teste de Breusch-Pagan global |
| Erros robustos | `fit(cov_type="HC3")` | estimador sanduíche $(X'X)^{-1} X' \operatorname{diag}\!\big(e_i^2/(1-h_{ii})^2\big) X (X'X)^{-1}$. **Não** supõe variância constante, mas supõe erros **independentes**. Os coeficientes são os mesmos do MQO |
| Testes por termo | `wald_test_terms(scalar=True)` | teste de Wald de cada termo, com `RAD` como bloco de 8 indicadoras. Com HC3, a estatística F usa a covariância robusta |

Resultados que atualizam a Seção 15: com HC3 no modelo E, os erros padrão são em média 23% maiores, mas **nenhuma variável muda de conclusão** a 5%.

### 14.1 Limitação: independência dos erros

**O que o notebook faz.** A independência é verificada só pela **ordem das linhas do arquivo**:

| Onde | Teste | Resultado |
|---|---|---|
| Parte 5 (células 67 e 72), modelo completo | teste das sequências e Durbin-Watson (Seção 11.4) | z = −8,11; DW = 0,95 |
| Parte 5 (continuação), 12 modelos distintos | Durbin-Watson em `avaliar` (Seção 12.2) | DW entre 0,95 e 1,27 |
| Parte 7 (célula 106), modelos A a E | Durbin-Watson em `diagnosticar` | DW entre 1,09 e 1,19 |
| Parte 7 (célula 108), modelo E com `log`, `raiz` e λ ótimo | Durbin-Watson em `diagnosticar` | DW entre 1,15 e 1,19 |

Um DW perto de 2 indica ausência de autocorrelação. Valores perto de 1 indicam **autocorrelação positiva**: resíduos de linhas vizinhas têm o mesmo sinal. Como o arquivo está ordenado por região, linhas vizinhas são regiões vizinhas, e o resultado indica **dependência espacial** (Seção 11.4).

**Por que as transformações não resolvem.** Log, Box-Cox, centralização e termos quadráticos mudam a escala e a forma da relação entre as variáveis. Eles não mudam a **relação entre as observações**. Em todas as especificações da Parte 7, o DW fica entre 1,09 e 1,19. A diferença para a Parte 5 (0,95) vem da remoção das 5 linhas suspeitas: o modelo A, ainda sem transformações, já tem DW de 1,09. Remover outliers e pontos influentes (Parte 5, continuação) leva o DW no máximo a 1,27. Assim, a autocorrelação não é causada por alguns pontos atípicos nem pela forma funcional: é dependência entre regiões.

**Por que o HC3 também não resolve.** Os erros padrão HC3 corrigem a variância **não constante**, mas supõem erros **independentes** (matriz de covariância diagonal). Com dependência positiva entre vizinhos, a informação efetiva da amostra é menor que n = 501. Assim, mesmo com HC3, os erros padrão do notebook devem estar **subestimados**, e os p-valores e intervalos de confiança são **otimistas**.

**Consequências para a leitura dos resultados.**

- Os **coeficientes** continuam não viesados (o MQO não exige independência para isso), mas não são os mais eficientes.
- Os **p-valores** devem ser lidos como **aproximados**. Termos com p-valor perto de 0,05 (`CHAS` e `B` com HC3, Seção 14) são os mais sensíveis a esse problema.
- O **R²** e os gráficos de diagnóstico continuam válidos como descrição do ajuste. Os **testes** dos outros pressupostos (RESET, Breusch-Pagan, Shapiro-Wilk) também supõem independência, então seus p-valores também são aproximados.

**O que não foi feito.** O conjunto de dados do Kaggle não traz as coordenadas nem o nome da cidade de cada região. Sem isso, não é possível:

- calcular o **I de Moran** dos resíduos, que é o teste direto de dependência espacial;
- usar **erros padrão agrupados por cidade** (`cov_type="cluster"`) ou **erros padrão espaciais** (Conley);
- ajustar um **modelo espacial** (defasagem ou erro espacial).

Os erros padrão HAC (Newey-West, `cov_type="HAC"`) usariam a ordem do arquivo como se fosse tempo. Eles não foram usados, pois a ordem é só uma aproximação da vizinhança. Por isso, a independência dos erros fica registrada como **limitação do modelo**.

---

## 15. O que ainda não foi verificado

| Pressuposto ou cuidado | Situação |
|---|---|
| Erros padrão robustos (HC3) | aplicados **só ao modelo E** da Parte 7 (Seção 14). As Partes 5 e 6 continuam com `cov_type='nonrobust'` |
| Independência espacial | rejeitada pela ordem do arquivo em todos os modelos (DW entre 0,95 e 1,27). Nenhuma transformação nem o HC3 corrigem. Sem coordenadas, não há I de Moran, erros padrão agrupados ou modelo espacial. Registrada como **limitação** (Seção 14.1) |
| Censura em 50 | tratada apenas parcialmente (remoção, para verificação). Sem modelo Tobit |
| Diagnóstico do modelo da Parte 6 | gráfico QQ, Shapiro-Wilk, Breusch-Pagan e Durbin-Watson feitos na Parte 7 (modelos D e E). Ainda faltam as medidas de influência (alavanca, Cook, DFFITS) |
| Modelo final | forma funcional definida na Parte 7 (modelo E com HC3). Falta combinar com a remoção S+I da Parte 5 |
| Capacidade preditiva | não avaliada: não há divisão treino/teste nem validação cruzada |

---

## Referências

- Belsley, D. A.; Kuh, E.; Welsch, R. E. (1980). *Regression Diagnostics: Identifying Influential Data and Sources of Collinearity*. Wiley.
- Fox, J.; Monette, G. (1992). Generalized collinearity diagnostics. *Journal of the American Statistical Association*, 87(417), 178–183.
- Montgomery, D. C.; Peck, E. A.; Vining, G. G. (2012). *Introduction to Linear Regression Analysis*. 5. ed. Wiley.
- Cleveland, W. S. (1979). Robust locally weighted regression and smoothing scatterplots. *Journal of the American Statistical Association*, 74(368), 829–836.
- Atkinson, A. C. (1985). *Plots, Transformations and Regression*. Oxford University Press.
- Filliben, J. J. (1975). The probability plot correlation coefficient test for normality. *Technometrics*, 17(1), 111–117.
- Koenker, R. (1981). A note on studentizing a test for heteroscedasticity. *Journal of Econometrics*, 17(1), 107–112.
- Box, G. E. P.; Cox, D. R. (1964). An analysis of transformations. *Journal of the Royal Statistical Society B*, 26(2), 211–252.
- Long, J. S.; Ervin, L. H. (2000). Using heteroscedasticity consistent standard errors in the linear regression model. *The American Statistician*, 54(3), 217–224.
- Yeo, I.-K.; Johnson, R. A. (2000). A new family of power transformations to improve normality or symmetry. *Biometrika*, 87(4), 954–959.
- Ramsey, J. B. (1969). Tests for specification errors in classical linear least-squares regression analysis. *Journal of the Royal Statistical Society B*, 31(2), 350–371.
- Documentação: [pandas `Series.skew`/`kurt`](https://pandas.pydata.org/docs/reference/api/pandas.Series.skew.html), [scipy `mannwhitneyu`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html), [scipy `kruskal`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html), [statsmodels `OLSInfluence`](https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.OLSInfluence.html).
