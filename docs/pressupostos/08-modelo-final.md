## 16. Modelo final (Parte 8, células 63–76)

Células do notebook [`02-MRLM.ipynb`](../../notebooks/02-MRLM.ipynb).

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Amostra | `df_t` (célula 49) | a mesma da Parte 7 (n = 501: sem as linhas suspeitas 506 a 510 e sem `RM` ausente). `RM_c` e `logLSTAT_c` são centralizados na média desses 501 dados |
| Seleção de variáveis | `modelo_e_hc3.wald_test("ZN = 0, INDUS = 0, AGE = 0", scalar=True)` (célula 65) | teste de Wald **conjunto** com a covariância HC3 (estatística χ² com 3 GL, `use_f=False`, o padrão para covariância robusta). AIC e BIC com a verossimilhança normal do MQO; só comparáveis porque a resposta e as linhas são as mesmas |
| Fórmula final | `formula_final` | `logMEDV ~ CRIM + C(CHAS) + NOX + logDIS + C(RAD) + PTRATIO + B + logLSTAT + RM_c + I(RM_c**2) + I(logLSTAT_c**2)`. `TAX` já estava fora (colinear com `RAD`, [Seção 7](02-eda.md)) |
| Influentes | `linhas_influentes` (célula 67) | os mesmos cortes da [Seção 11.2](03-modelo-completo-residuos.md): Cook > 4/n ou \|DFFITS\| > 2·√(p/n), agora no modelo reduzido (p = 19). O modelo é reajustado sem essas linhas, como no S+I da [Seção 12](04-selecao-modelos.md) |
| VIF | `variance_inflation_factor` (célula 67) | VIF de cada termo do modelo final, exceto as indicadoras de `RAD` (bloco avaliado pelo GVIF na [Seção 7](02-eda.md)). Calculado com a matriz de delineamento, incluindo o intercepto |
| Resumo dos resíduos | `resumir_residuos` (célula 67) | como `diagnosticar` ([Seção 14](06-transformacoes.md)), mas com os quantis teóricos calculados para cada n. Acrescenta o teste de Bonferroni (`outlier_test`) |
| Inferência | `fit(cov_type="HC3")` (célula 69) | coeficientes iguais aos do MQO; erros padrão, IC 95% (normal, pois a covariância é robusta), p-valores e F global com HC3. Supõe erros independentes |
| Efeitos em % | `100 * (np.exp(β) - 1)` | preditor na escala original e indicadoras: efeito exato de +1 unidade (ou do nível) em `MEDV`. `logDIS` e `logLSTAT`: β é a elasticidade (+1% no preditor muda `MEDV` em cerca de β%); para `logLSTAT`, no ponto médio, por causa do termo quadrático centralizado. `RM_c`: efeito de +1 cômodo na casa média, $e^{\beta_1 + 2\beta_2(RM - \overline{RM})} - 1$ ([Seção 13](05-termo-quadratico-rm.md)) |
| Ordem aleatória | `durbin_watson(rng.permutation(resid))`, 1000 vezes, semente 42 (célula 71) | distribuição do DW sem dependência entre linhas vizinhas. Se o DW do arquivo ficar fora dessa faixa e a faixa ficar em torno de 2, a dependência vem da ordem das linhas e não da forma do modelo |
| Erros agrupados | `fit(cov_type="cluster", cov_kwds={"groups": cidade})` | `cidade` = `groupby(["TAX", "PTRATIO", "INDUS", "ZN"]).ngroup()`. Essas variáveis são medidas por cidade, então a combinação **aproxima** a cidade. Permite correlação qualquer dentro do grupo e supõe grupos independentes. Usa a correção de amostra finita padrão do statsmodels (`use_correction=True`). Os p-valores usam a normal (`use_t=False`, o padrão). Com 78 grupos e um grupo de 112 linhas, é uma verificação, não a inferência principal |
| Gráficos | célula 73 | QQ com envelope de 100 simulações N(0, 1) (semente 42), resíduos x ajustados com LOWESS, escala-locação $\sqrt{\lvert r_i \rvert}$ x ajustados, Cook por índice. Salvo em `results/figures/diagnostico_modelo_final.html` |
| Validação cruzada | `KFold(n_splits=10, shuffle=True, random_state=42)` (célula 75) | as mesmas partes para os três modelos. O modelo é reajustado em cada treino, e as previsões são feitas na parte de teste. A remoção das influentes é feita **só no treino**, com os cortes recalculados em cada rodada |
| Volta à escala de `MEDV` | `prever_log`: $e^{\hat y} \cdot \frac{1}{n}\sum e^{e_i}$ | fator de smearing de Duan (1983) com os resíduos do treino. Não supõe erros normais, mas supõe erros com a **mesma distribuição** para todo $x$. Com heterocedasticidade, a correção é aproximada. Com fator ≈ 1,015, o efeito no RMSE é pequeno |
| Medidas | RMSE, MAE, R² fora da amostra | todas em mil dólares, na escala de `MEDV`, para comparar o modelo linear (Parte 5) com o modelo em log. R² fora da amostra = 1 − SQR/SQT da parte de teste. A tabela mostra a média das 10 rodadas e o desvio padrão do RMSE |

### 16.1 Resultados

| Etapa | Resultado |
|---|---|
| Seleção | Wald (HC3) para `ZN`, `INDUS` e `AGE`: χ² = 0,32, p = 0,96. AIC −285 → −291; BIC −192 → −211; R² ajustado 0,812 → 0,813 |
| Influentes | 28 linhas (5,6%); só 10 em comum com as 24 da Parte 5; 5 com `MEDV = 50`; Cook máximo 0,23. Maior VIF do modelo final: 4,8 (`NOX`) |
| Resíduos sem as influentes (n = 473) | correlação QQ 0,993; curtose 1,3; 5 com \|t\| > 3 (1,3 esperados); Shapiro-Wilk p = 0,001; RESET p = 0,94; Breusch-Pagan p ≈ 10⁻¹¹; DW 1,41 |
| Ajuste | R² = 0,885; R² ajustado = 0,881; erro padrão residual 0,129 em log |
| Coeficientes (HC3) | todos os termos significativos a 5% (`RAD` como bloco); só o nível 6 de `RAD` não difere do nível 1 |
| Ordem aleatória | DW médio 2,00 (95%: 1,82 a 2,18) contra 1,41 no arquivo |
| Erros agrupados | 78 grupos; todos os termos continuam significativos. Erros padrão maiores em `logLSTAT` (×2,3), `logLSTAT²` (×1,9) e `RM_c` (×1,6); `CHAS` p = 0,03 |
| Validação cruzada (mil dólares) | linear completo: RMSE 4,80, MAE 3,39, R² 0,71; final: RMSE 4,00, MAE 2,75, R² 0,79; final sem influentes no treino: RMSE 4,07, MAE 2,66, R² 0,78 |

**O que os resultados permitem concluir.**

- A remoção de `ZN`, `INDUS` e `AGE` é apoiada pelo teste conjunto e pelos critérios de informação. O teste usa HC3, então não depende da variância constante.
- Sem as influentes, a forma funcional é aceita e os resíduos são quase normais. A heterocedasticidade continua (resíduos maiores nas casas baratas), por isso a inferência é feita com HC3.
- A permutação mostra que o DW baixo vem da ordem das linhas (vizinhança), e não da forma do modelo. Os erros agrupados tratam a correlação **dentro** das cidades aproximadas, mas não a correlação **entre** cidades vizinhas, que continua uma limitação ([Seção 14.1](06-transformacoes.md)).
- A validação cruzada mostra que o modelo final prevê melhor que o modelo linear completo. A remoção das influentes não melhora a previsão. Ela serve para estimar os coeficientes da população típica, e o modelo para previsão deve usar todas as linhas.
