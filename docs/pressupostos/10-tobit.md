## 18. Censura em 50: modelo Tobit (Parte 10, células 91–102)

Células do notebook [`02-MRLM.ipynb`](../../notebooks/02-MRLM.ipynb).

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Dados | `df_t` (célula 49), todas as 501 linhas | as 16 linhas com `MEDV = 50` são o objeto desta parte, então o ajuste não usa `df_final` (que já perdeu 5 delas como influentes). Resposta `logMEDV`, limite superior $c = \log 50$. Indicadora `censurado_t = df_t["MEDV"] >= 50` (célula 93); confere com `logMEDV >= log 50` linha a linha |
| Modelo | $y_i = \min(y_i^*, c)$, $y_i^* = x_i'\beta + \varepsilon_i$, $\varepsilon_i \sim N(0, \sigma^2)$ (Tobin, 1958; Wooldridge, cap. 17) | mesma média de `formula_final` (célula 65). Linha não censurada: $\log\phi\big((y_i - x_i'\beta)/\sigma\big) - \log\sigma$. Linha censurada: $\log\big[1 - \Phi\big((c - x_i'\beta)/\sigma\big)\big]$, isto é, a probabilidade de o valor real ser 50 ou mais |
| Implementação | `class Tobit(GenericLikelihoodModel)` (célula 93) | `loglikeobs` com `stats.norm.logpdf` e `stats.norm.logsf` (estável na cauda). Parâmetros $\beta$ e $\gamma$, com $\log\sigma_i = z_i'\gamma$; sem `exog_var`, $z_i = 1$ e $\gamma$ = `log_sigma` (garante $\sigma > 0$). $X$ de `patsy.dmatrices(formula_final, df_t)`. Partida: MQO e $\log\hat\sigma_{\text{MQO}}$. Otimizador `bfgs`, `maxiter=5000`. O resultado é envolvido em `LikelihoodResultsWrapper` para que `params`, `bse` e `pvalues` tenham os nomes dos termos. Convergência conferida com `assert mle_retvals["converged"]` em todos os ajustes |
| Erros padrão | `fit()` e `fit(cov_type="HC0")` | padrão: inversa da hessiana numérica (supõe o modelo correto). Sanduíche $H^{-1}(S'S)H^{-1}$ com escores numéricos: robusto a heterocedasticidade, mas não corrige o viés de $\beta$ se a distribuição estiver errada |
| Conferência por simulação | célula 95 | mesma $X$; $\beta$ e $\sigma$ verdadeiros = MQO (`modelo_reduzido`); $c$ = quantil 95% de $y^*$ numa primeira amostra (fixo). 200 réplicas com `np.random.default_rng(42)`; em cada uma, Tobit e MQO em $\min(y^*, c)$. Critério: viés médio pequeno em relação ao desvio padrão entre réplicas |
| Conferência sem censura | `Tobit(y, X, np.inf)` (célula 95) | sem linhas censuradas, a verossimilhança é a da regressão normal: $\hat\beta$ = MQO e $\hat\sigma = \sqrt{SQR/n}$ (máxima verossimilhança, sem correção de graus de liberdade) |
| Três ajustes | célula 97 | MQO em `df_t` (`smf.ols(formula_final, df_t)`, igual a `modelo_reduzido`, com `cov_type="HC3"`); MQO sem `MEDV = 50` (485 linhas, HC3); Tobit em `df_t`. Efeito em % de `MEDV`: $100\,(e^\beta - 1)$. Mudança medida em erros padrão HC3 do MQO |
| Tobit heterocedástico | `Tobit(..., exog_var=[1, logLSTAT])` (célula 99) | $\log\sigma_i = \gamma_0 + \gamma_1 \log LSTAT_i$, a forma escolhida na [Seção 17](09-heterocedasticidade.md). Razão de verossimilhança contra o Tobit homocedástico, $\chi^2$ com 1 GL (`stats.chi2.sf`). Serve para medir quanto a heterocedasticidade enviesa o Tobit homocedástico |
| Validação cruzada | `prever_tobit` (célula 101) | as mesmas partes da [Seção 16](08-modelo-final.md) (`KFold(10, shuffle=True, random_state=42)` em `df_t`). Em cada treino, Tobit e MQO são ajustados de novo; $X$ de teste por `patsy.build_design_matrices` com o `design_info` do treino. Previsão do valor observado: $E[\min(MEDV, 50) \mid x] = e^{\mu + \sigma^2/2}\,\Phi(\alpha - \sigma) + 50\,[1 - \Phi(\alpha)]$, com $\alpha = (\log 50 - \mu)/\sigma$. Supõe $\log MEDV \mid x$ normal. Comparada com o modelo final (MQO + smearing de Duan, `prever_log`), no total e separando as 16 linhas censuradas |

### 18.1 Resultados

| Etapa | Resultado |
|---|---|
| Simulação (200 réplicas) | todas convergiram; censura média de 5,2%. Maior viés do Tobit nos coeficientes: 0,24 desvio padrão (`RM_c²`); em `log_sigma`, 0,53 (viés de $\sigma$ da máxima verossimilhança em amostra finita). MQO no $y$ censurado: `RM_c` 0,074 → 0,050 (viés de 1,3 desvio padrão) e `RM_c²` 0,056 → 0,039 (1,6) |
| Sem censura | maior diferença Tobit − MQO: 7,7·10⁻⁸; $\hat\sigma$ = 0,17429 = $\sqrt{SQR/n}$ |
| Convergência | Tobit em `df_t`: `converged = True` (também com sanduíche, no heterocedástico e nas 10 partes da validação) |
| $\hat\sigma$ | MQO 0,178; MQO sem `MEDV = 50` 0,168; Tobit 0,178 |
| Coeficientes: Tobit × MQO | todos a menos de 0,5 erro padrão HC3. Maiores: `RM_c²` 0,056 → 0,064 (+14%, 0,47 EP); `RM_c` 0,074 → 0,082 (+12%, 0,36 EP); `RAD = 8` (−0,29 EP); `CHAS` 0,110 → 0,121 (+11,6% → +12,9%). `logLSTAT` −0,383 → −0,386 (efeito −31,8% → −32,0%); `logLSTAT_c²` −0,109 → −0,103 |
| Coeficientes: sem 50 × MQO | `logLSTAT` −0,383 → −0,319 (1,9 EP); `logDIS` −0,191 → −0,122 (1,8 EP); `CHAS` 0,110 → 0,063 (1,1 EP); `RM_c` 0,074 → 0,098 (1,0 EP) |
| Significância | p < 0,05: 17 de 18 termos no MQO com HC3 (`RAD = 6`, p = 0,059); 18 de 18 no Tobit com sanduíche (`RAD = 6`, p = 0,0495) |
| EP sanduíche / EP hessiana | média 1,17, de 0,76 (`RAD = 7`) a 1,89 (`CRIM`); `RM_c²` 1,76, `RM_c` 1,50, `logLSTAT` 1,46 |
| Tobit heterocedástico | $\gamma_1$ = 0,343 (EP sanduíche 0,093), isto é, $\sigma^2 \propto LSTAT^{0{,}69}$ (MQGF: $LSTAT^{0{,}82}$). Razão de verossimilhança 41,9 (1 GL), p ≈ 10⁻¹⁰. Coeficientes mudam no máximo 0,87 EP sanduíche (`logDIS`); `RM_c` muda 0,02 EP. `RAD = 2`, `6` e `8` deixam de ser significativos a 5% |
| Validação cruzada (mil dólares) | final (MQO + Duan): RMSE 4,00, MAE 2,75, R² 0,79 (desvio padrão do RMSE 1,19); **Tobit: 3,83, 2,69, 0,81** (0,92) |
| Por grupo (10 partes juntas) | `MEDV` < 50 (485): RMSE 3,52 → 3,35, erro médio −0,35 → −0,38. `MEDV` = 50 (16): RMSE 12,8 → 11,9, erro médio (observado − previsto) +7,2 → +8,8 |

**O que os resultados permitem concluir.**

- A implementação está correta: sem censura ela reproduz o MQO, e com 5% de censura recupera $\beta$ sem viés, enquanto o MQO atenua os termos de `RM` em 1,3 a 1,6 desvio padrão.
- Nos dados reais, a censura **não muda as conclusões** do modelo final ([Seção 16](08-modelo-final.md)): os sinais, a significância e os efeitos de `LSTAT`, `NOX`, `CRIM`, `DIS` e `PTRATIO` ficam iguais. O efeito de `RM` no MQO está um pouco **atenuado** (12% a 14% menor que no Tobit, menos de 0,5 erro padrão). Com 16 linhas censuradas (3%), o viés do MQO é pequeno.
- A **remoção** das linhas com `MEDV = 50` (Parte 6, [Seção 13](05-termo-quadratico-rm.md)) muda mais os coeficientes e na direção errada (trunca a amostra e atenua `logLSTAT` e `logDIS` em quase 2 erros padrão). Ela não é um bom tratamento da censura.
- O modelo não está correto em toda a distribuição: os erros padrão sanduíche são até 1,9 vez os da hessiana, e a variância constante é rejeitada. A inferência do Tobit deve usar o sanduíche. Como os coeficientes do Tobit heterocedástico ficam a menos de 0,9 erro padrão, o viés causado pela heterocedasticidade é pequeno.
- Para previsão, o Tobit é melhor que o modelo final (RMSE 3,83 contra 4,00) e que o MQGF da [Seção 17](09-heterocedasticidade.md) (3,89). Ele prevê o valor observado, $\min(MEDV, 50)$, e não o valor real. As casas censuradas continuam mal previstas (erro médio de +8,8 mil dólares).
- Limitações: o Tobit supõe erros **normais** (os resíduos têm caudas pesadas, [Seção 16.1](08-modelo-final.md)) e de variância constante (rejeitada); o limite de 50 é tratado como conhecido e único; o ajuste usa as 501 linhas, com as 28 influentes; a correlação espacial ([Seção 14.1](06-transformacoes.md)) continua. O modelo final da Parte 8 é mantido; o Tobit fica como verificação de robustez. Juntar a censura e a variância modelada (Tobit heterocedástico na validação cruzada) é o próximo passo natural.
