## 17. Heterocedasticidade: MQGF (Parte 9, células 128–141)

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Ponto de partida | `modelo_final_classico` (célula 118) | resíduos do MQO do modelo final (n = 473, sem as 28 influentes). A Parte 8 corrige só os erros padrão (HC3); aqui a variância é **modelada** |
| Forma da variância | `smf.ols("log_e2 ~ z", data=dados_aux)` (célula 130) | modelo multiplicativo $\operatorname{Var}(\varepsilon_i \mid x_i) = \sigma^2 \exp(z_i'\delta)$, estimado pela regressão de $\log(e_i^2)$ em $z$ (Wooldridge, cap. 8). Três formas: (a) $z = \hat y$; (b) $z$ = `logLSTAT`; (c) $z$ = todos os preditores de `formula_final`. Comparação por R², F global, BIC e F parcial (c) contra (b) (`compare_f_test`, as formas são aninhadas). A forma exponencial garante variância positiva |
| Forma escolhida | `forma_variancia = "logLSTAT"` (célula 132) | a mais simples com bom ajuste: um termo, R² maior que (a) e o menor BIC. (c) é rejeitada como forma mais simples pelo F parcial, mas tem 18 termos e prevê pior na validação cruzada |
| MQGF | `ajustar_mqgf(dados, forma)` (célula 132) | 1) MQO; 2) regressão auxiliar de $\log(e^2)$, com $\hat g_i$ = valor ajustado; 3) `smf.wls(formula_final, data=dados, weights=1/exp(ĝ))`. Pressuposto principal: a **forma da variância está correta**. Se estiver errada, os coeficientes continuam consistentes, mas os erros padrão do WLS não; por isso também `cov_type="HC3"` (`modelo_mqgf_hc3`) |
| Escala da variância | `variancia_log` (célula 132) | $\hat\sigma^2(x) = s^2_{\text{MQGF}} \cdot \exp(\hat g(x))$. A constante de $\hat g$ é viesada ($E[\log\chi^2_1] \approx -1{,}27$), mas o viés fica absorvido no `scale` do WLS, pois os pesos só precisam ser proporcionais a $1/\sigma^2_i$ |
| Resíduos ponderados | `het_breuschpagan(m.wresid, m.model.exog)` (célula 134) | Breusch-Pagan em $\sqrt{w_i}\,e_i$ com os mesmos regressores do teste no MQO (versão studentizada de Koenker, `robust=True`, o padrão). Supõe resíduos independentes |
| Gráfico | célula 134 | escala-locação do MQO ($\sqrt{\lvert r_i \rvert}$ studentizado interno) e do MQGF ($\sqrt{\lvert \sqrt{w_i}\,e_i/s \rvert}$), com LOWESS. Inclinação resumida pela correlação de Spearman com o valor ajustado. Salvo em `results/figures/escala_locacao_mqgf.png` |
| Comparação dos coeficientes | célula 136 | MQO e MQGF estimam os mesmos $\beta$ se a média está bem especificada. Diferença medida em erros padrão HC3 do MQO; diferenças de várias unidades indicariam erro de especificação |
| Volta à escala de `MEDV` | `prever_log_hetero` (célula 138) | correção lognormal $e^{\hat y + \hat\sigma^2(x)/2}$. Supõe $\log(MEDV) \mid x$ aproximadamente **normal**; razoável sem as influentes (correlação QQ 0,993, [Seção 16.1](08-modelo-final.md)). Comparada com o fator único de Duan (`prever_log`) |
| Validação cruzada | célula 140 | as mesmas partes da [Seção 16](08-modelo-final.md) (`KFold(10, shuffle=True, random_state=42)` em `df_t`, todas as linhas do treino). Em cada treino, MQO, regressão auxiliar e pesos são estimados de novo; o teste só é usado para prever. Compara o modelo final (MQO + Duan) com o MQGF nas três formas |
| Intervalos de previsão | `get_prediction(teste, weights=...).summary_frame(alpha=0.05)` | colunas `obs_ci_*` em log, levadas por $e^x$ (os quantis passam pela exponencial, sem correção). MQO: variância única $s^2$. MQGF: variância $s^2/w$, com `weights = scale / variancia_log(...)` na parte de teste. Supõem erros normais. Cobertura = proporção de `MEDV` dentro do intervalo, juntando as 10 partes, no total e por quartil de `MEDV` (`pd.qcut(df_t["MEDV"], 4)`) |

### 17.1 Resultados

| Etapa | Resultado |
|---|---|
| Forma da variância | (a) $\hat y$: R² 0,034, BIC 2125; (b) `logLSTAT`: R² 0,044, BIC 2120, coeficiente 0,82 ($\sigma^2_i \propto LSTAT_i^{0{,}82}$); (c) todos: R² 0,123, BIC 2184. F parcial (c) contra (b): F = 2,39 (17 GL), p = 0,002 |
| Pesos | razão maior/menor de 12,6. Desvio padrão em log de 0,058 a 0,207 (MQO: 0,129 para todas as linhas) |
| Breusch-Pagan | MQO p ≈ 6·10⁻¹²; MQGF (resíduos ponderados) p ≈ 2·10⁻⁶ |
| Escala-locação | Spearman($\sqrt{\lvert r \rvert}$, ajustado): −0,22 (MQO) → −0,02 (MQGF). Resta uma leve curva em U nas pontas |
| Coeficientes | maior diferença: 1,2 EP HC3 (`CHAS`, 0,091 → 0,065, isto é, +9,6% → +6,7%). Todos os termos significativos a 5% no MQGF, com e sem HC3. EP HC3 do MQGF / EP HC3 do MQO: 1,00 em média |
| Volta à escala | fator lognormal de 1,014 (1º quartil de $\hat y$) a 1,004 (4º quartil); média 1,008, igual ao fator de Duan (1,008 em `df_final`) |
| Validação cruzada (mil dólares) | final (MQO): RMSE 4,00, MAE 2,75, R² 0,79; MQGF (a): 3,92, 2,71, 0,80; **MQGF (b): 3,89, 2,71, 0,80**; MQGF (c): 4,01, 2,63, 0,79 |
| Cobertura 95% (MQO → MQGF (b)) | `MEDV` ≤ 17: 87,3% → 91,3%; 17 a 21,2: 99,2% → 99,2%; 21,2 a 25: 96,8% → 96,8%; > 25: 94,4% → 94,4%; total: 94,4% → 95,4% |
| Largura média do intervalo (MQO → MQGF (b)) | `MEDV` ≤ 17: 10,1 → 12,5; > 25: 24,4 → 17,2 mil dólares |

**O que os resultados permitem concluir.**

- A variância dos erros cresce com `LSTAT`: as regiões pobres, de casas baratas, têm erros maiores. Uma forma com um só termo (`logLSTAT`) basta; a forma com todos os preditores ajusta melhor $\log(e^2)$, mas é instável e prevê pior.
- O MQGF remove a tendência da variância com o nível de preço (escala-locação sem inclinação). O Breusch-Pagan ainda rejeita, então a forma da variância não é exata; por isso a inferência do MQGF também é dada com HC3.
- Os coeficientes do MQGF ficam a menos de 1,2 erro padrão dos do MQO: não há sinal de erro de especificação da média, e as conclusões da [Seção 16](08-modelo-final.md) (sinais e significância) se mantêm. O ganho de eficiência é pequeno.
- Para **previsão**, o MQGF com pesos por `logLSTAT` é melhor: RMSE 3,89 contra 4,00 (critério da tarefa: ≤ 4,00), e intervalos de previsão que se ajustam ao preço, com cobertura total de 95,4%.
- A cobertura nas casas mais baratas (91,3%) continua abaixo de 95%. Ali estão as caudas pesadas (centro de Boston, [Seção 16.1](08-modelo-final.md)), que o intervalo normal não cobre. Um intervalo por quantis empíricos ou por bootstrap seria o próximo passo.
- Limitações do MQGF: supõe a forma da variância correta e erros independentes; a correlação espacial ([Seção 14.1](06-transformacoes.md)) continua.
