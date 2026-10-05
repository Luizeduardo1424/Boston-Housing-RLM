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
| Resíduos × ajustados | `sns.regplot(x=fittedvalues, y=resid, lowess=True)` | resíduo **bruto**. LOWESS robusta com `frac=2/3` e `it=3` (padrões, [Seção 4](02-eda.md)) |
| RESET de Ramsey | `linear_reset(modelo, power=2, use_f=True)` | acrescenta **apenas** $\hat y^2$ (o padrão do statsmodels é `power=3`, que acrescenta $\hat y^2$ e $\hat y^3$). Teste F com covariância **não robusta** (`cov_type='nonrobust'`). Detecta curvatura em função de $\hat y$, mas não diz qual variável a causa |
| Breusch-Pagan | `het_breuschpagan(modelo.resid, modelo.model.exog)` | resíduo **bruto**. O padrão `robust=True` usa a versão de **Koenker** (LM = $n R^2$ da regressão de $e^2$ sobre as colunas), que **não supõe erros normais**. As variáveis auxiliares são as próprias colunas do modelo, inclusive as indicadoras. O notebook usa o LM e seu p-valor $\chi^2_{20}$ |
