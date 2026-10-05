## 20. Interação `RM × logLSTAT` (Parte 12, células 168–179)

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Fórmula | `formula_interacao = formula_final + " + RM_c:logLSTAT_c"` (célula 170) | o efeito de `RM` em `log(MEDV)` passa a depender de `logLSTAT`. `RM_c` e `logLSTAT_c` são centralizados na média de `df_t` (célula 100), e os coeficientes principais continuam sendo os efeitos no ponto médio (Aiken e West, 1991). A interação usa `logLSTAT_c`; o efeito principal continua com `logLSTAT` sem centralizar, como no modelo final |
| Dados | `df_final` (célula 118) | as mesmas 473 linhas do modelo final, para que o teste e o AIC comparem os dois modelos nas mesmas linhas |
| Ajuste | `smf.ols(formula_interacao, data=df_final).fit(cov_type="HC3")` e `.fit()` (célula 170) | MQO. Erros padrão HC3 para o teste; o ajuste clássico serve para AIC, BIC, R² ajustado, VIF, alavanca e `resumir_residuos` |
| Teste | `modelo_interacao.wald_test("RM_c:logLSTAT_c = 0", scalar=True)` (célula 170) | Wald com HC3, $\chi^2$ com 1 GL. O teste t clássico é mostrado só para comparação, porque a variância não é constante ([Seção 17](09-heterocedasticidade.md)) |
| VIF | `variance_inflation_factor(exog, i)` (célula 170) | como na célula 118 ([Seção 16](08-modelo-final.md)), sem as indicadoras de `RAD` |
| Linhas influentes | `linhas_influentes(smf.ols(formula_interacao, df_t).fit())` (célula 172) | mesmos critérios da célula 118 (Cook > 4/n ou \|DFFITS\| > 2·√(p/n)), agora com a nova fórmula. O teste é repetido sem as novas influentes |
| Alavanca | `get_influence().hat_matrix_diag` (célula 172) | $h_{ii}$ nos dois modelos. O HC3 divide cada resíduo ao quadrado por $(1 - h_{ii})^2$, e uma linha com alavanca alta aumenta muito o erro padrão. Referência: $2p/n$. O teste é repetido sem a linha de maior alavanca (`linha_rara`) |
| Efeito de +1 cômodo | `efeito_comodo(params, rm, lstat)` (célula 174) | $100 \cdot \big(e^{\beta_{RM} + 2\beta_{RM^2}(RM - \overline{RM}) + \beta_{int}(\log LSTAT - \overline{\log LSTAT})} - 1\big)$, com as médias de `df_t`. É a fórmula da Seção 8.3 com o termo da interação (sem `lstat`, é a do modelo final). `RM` = 6, 7 e 8; `LSTAT` nos quartis 25%, 50% e 75% de `df_t`. Figura em `results/figures/efeito_rm_por_lstat.png` (`RM` de 5 a 8,5) |
| Validação cruzada | célula 176 | as mesmas partes da célula 126: `KFold(n_splits=10, shuffle=True, random_state=42).split(df_t)`; os dois modelos com todas as linhas do treino, previsão por `prever_log` (smearing de Duan). Verificação: os dois modelos sem `linha_rara` no treino. A parte de teste mantém todas as linhas |
| Resíduos | `resumir_residuos` (célula 178) | nos dois ajustes MQO clássicos em `df_final`. RESET com `power=2` |
| Regra de decisão | célula 168 | a interação entra no modelo final só se o Wald com HC3 der p < 0,05 **e** o RMSE da validação cruzada for menor que 4,00 |

### 20.1 Resultados

| Etapa | Resultado |
|---|---|
| Coeficiente | $\hat\beta_{int}$ = −0,0759; EP HC3 = 0,0871; IC 95% = [−0,247; 0,095] |
| Wald (HC3) | $\chi^2$ = 0,76 (1 GL); **p = 0,38** |
| Teste t clássico | EP = 0,0275; p = 0,006 |
| Ajuste (MQO, 473 linhas) | R² ajustado 0,881 → 0,883; AIC −580,0 → −585,9; BIC −501,0 → −502,7 |
| VIF | interação 6,13; maior dos outros termos 4,81 (`NOX`). Correlação entre `RM_c` e `logLSTAT_c` em `df_final`: −0,69 |
| Outros coeficientes (HC3) | `RM_c` 0,115 → 0,109; `RM_c²` 0,068 → 0,048 (p = 0,24); `logLSTAT` −0,311 → −0,321; `logLSTAT_c²` −0,089 → −0,141 (p = 0,004) |
| Linhas influentes | 29 com a interação contra 28 no modelo final; 28 em comum; nova: linha 397. Sem as 29: $\hat\beta$ = −0,080, p HC3 = 0,37 |
| Alavanca | linha 365 (`RM` = 3,561, o menor dos dados; `LSTAT` = 7,12; `MEDV` = 27,5): $h$ = 0,34 no modelo final e 0,69 com a interação ($2p/n$ = 0,085). As outras linhas mudam pouco (próxima: linha 414, 0,21) |
| Sem a linha 365 (472 linhas) | $\hat\beta$ = −0,159; EP clássico 0,040; EP HC3 0,042; p HC3 = 0,0002 |
| Efeito de +1 cômodo (%) | `RM` = 6: +12,2 (Q25 de `LSTAT` = 6,92), +8,1 (mediana = 11,38), +4,8 (Q75 = 16,94); modelo final +7,9. `RM` = 7: +23,5, +18,9, +15,3; final +23,6. `RM` = 8: +35,8, +30,8, +26,9; final +41,7 |
| Validação cruzada | final: RMSE 3,996, MAE 2,753, R² 0,788. Com interação: RMSE **4,020**, MAE 2,751, R² 0,784. A interação tem RMSE menor em 5 das 10 partes. Sem a linha 365 no treino: 4,013 (final) contra 4,016 (interação) |
| Resíduos (final → interação) | R² ajustado 0,881 → 0,883; correlação QQ 0,993 nos dois; Shapiro-Wilk p 0,0012 → 0,0009; Breusch-Pagan p 6·10⁻¹² → 2·10⁻¹¹; RESET p 0,94 → 0,34; Durbin-Watson 1,41 → 1,42 |

**O que os resultados permitem concluir.**

- A interação **não entra** no modelo final: o Wald com HC3 não rejeita $\beta_{int} = 0$ (p = 0,38) e o RMSE da validação cruzada piora (4,02 contra 4,00). Nenhuma das duas condições da regra vale.
- O sinal é o da hipótese: um cômodo a mais vale menos onde `LSTAT` é alto. O teste clássico e o AIC dariam a interação como significativa, mas eles supõem variância constante, que é rejeitada.
- O resultado do teste HC3 depende de **uma linha**: a 365, com o menor `RM` dos dados e `LSTAT` baixo. A interação dobra a sua alavanca, e o HC3 triplica o erro padrão. Sem ela, p = 0,0002. Cook e DFFITS não marcam essa linha, porque o ajuste passa perto dela.
- Mesmo sem a linha 365, a previsão **não melhora** (RMSE 4,016 contra 4,013). A segunda condição continua falsa.
- Com a interação, o termo quadrático de `RM` perde força (0,068 → 0,048, p = 0,24). `RM` e `LSTAT` têm correlação −0,69, e os dados não separam bem um efeito de `RM` que cresce com `RM` de um efeito que cresce quando `LSTAT` é baixo. Por isso a tabela de efeitos deve ser lida como uma descrição alternativa, e não como uma correção do modelo final.
- Limitações: só uma interação foi testada; a indicadora `ZN > 0` continua pendente ([Seção 15](07-pendencias.md)). O teste foi feito no MQO com HC3; a correlação espacial ([Seção 19](11-correlacao-espacial.md)) não foi considerada aqui.
