## 21. Indicadora `ZN > 0` (Parte 13, células 180–193)

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Descrição | `mannwhitneyu(medv_com, medv_sem, alternative="two-sided")` (célula 182) | como na Parte 3: compara as distribuições de `MEDV` nos dois grupos sem supor normalidade e **sem controlar** os outros preditores. Feito em `df_t` e `df_final`. Aviso de pouco poder se um grupo tiver menos de 30 linhas. Também conta os grupos `cidade` (célula 122) de cada lado, porque `ZN` é medida por cidade e a indicadora é igual dentro da cidade |
| Fórmula | `formula_zn = formula_final + " + C(ZN > 0)"` (célula 184) | o patsy calcula a expressão dentro de `C()`; o coeficiente é `C(ZN > 0)[T.True]`, com `ZN = 0` como referência. `cidade` continua usando `ZN` original |
| Dados | `df_final` (célula 118) | as mesmas 473 linhas do modelo final, para que o teste e o AIC comparem os dois modelos nas mesmas linhas |
| Ajuste | `smf.ols(formula_zn, data=df_final).fit(cov_type="HC3")` e `.fit()` (célula 184) | MQO. Erros padrão HC3 para o teste; o ajuste clássico serve para AIC, BIC, R² ajustado, VIF, alavanca e `resumir_residuos` |
| Teste | `modelo_zn.wald_test("C(ZN > 0)[T.True] = 0", scalar=True)` (célula 184) | Wald com HC3, $\chi^2$ com 1 GL. Para comparação: teste t clássico e erros agrupados por `cidade` (`cov_type="cluster"`, como na célula 122), o teste mais exigente para uma variável que só muda entre cidades |
| Linhas influentes | `linhas_influentes(smf.ols(formula_zn, df_t).fit())` (célula 186) | mesmos critérios da célula 118 (Cook > 4/n ou \|DFFITS\| > 2·√(p/n)) com a nova fórmula; o teste é repetido sem as novas influentes |
| Alavanca | `get_influence().hat_matrix_diag` (célula 186) | $h_{ii}$ nos dois modelos, como na [Seção 20](12-interacoes.md). Referência $2p/n$. A tabela mostra as 5 linhas cuja alavanca mais sobe |
| Colinearidade | `variance_inflation_factor(exog, i)` e `Series.corr` (célula 188) | VIF como na célula 118, sem as indicadoras de `RAD`. Correlação ponto-bisserial da indicadora com `INDUS`, `NOX`, `logDIS` e `logMEDV` em `df_final`. Mudança dos coeficientes de `NOX` e `logDIS` |
| Efeito | célula 190 | $100 \cdot (e^{\beta} - 1)\%$ em `MEDV` entre setores com e sem lotes grandes, com o resto fixo (Seção 8.3). IC 95%: os limites do IC HC3 de $\beta$ na mesma transformação |
| Validação cruzada | célula 192 | as mesmas partes da célula 126: `KFold(n_splits=10, shuffle=True, random_state=42).split(df_t)`; os dois modelos com todas as linhas do treino, previsão por `prever_log` (smearing de Duan) |
| Resíduos | `resumir_residuos` (célula 192) | nos dois ajustes MQO clássicos em `df_final`. RESET com `power=2` |
| Regra de decisão | célula 180 | a indicadora entra no modelo final só se o Wald com HC3 der p < 0,05 **e** o RMSE da validação cruzada for menor que 4,00 |

### 21.1 Resultados

| Etapa | Resultado |
|---|---|
| Grupos | `df_final`: 131 linhas com `ZN > 0` (27,7%) e 342 com `ZN = 0`; `df_t`: 132 e 369. Grupos `cidade`: 47 com `ZN > 0` e 31 com `ZN = 0` (de 78) |
| Mann-Whitney (`df_final`) | mediana de `MEDV` 25,0 (`ZN > 0`) contra 19,9 (`ZN = 0`); p = 4·10⁻²² (em `df_t`: 25,1 contra 19,8; p = 2·10⁻²²) |
| Coeficiente | $\hat\beta$ = −0,0032; EP HC3 = 0,0173; IC 95% = [−0,037; 0,031] |
| Wald (HC3) | $\chi^2$ = 0,03 (1 GL); **p = 0,85** |
| Comparação | teste t clássico: EP 0,0206, p = 0,88. Agrupado por `cidade`: EP 0,0270, p = 0,91 |
| Ajuste (MQO, 473 linhas) | R² ajustado 0,8809 → 0,8806; AIC −580,0 → −578,1; BIC −501,0 → −494,9 |
| Efeito | −0,3% em `MEDV`; IC 95% de −3,6% a +3,1% |
| Colinearidade | correlação de `ZN > 0` com `INDUS` −0,58, `NOX` −0,52, `logDIS` +0,61, `logMEDV` +0,42. VIF da indicadora 2,42; maior dos outros 4,84 (`NOX`). `NOX` −0,665 → −0,666 (+0,2%); `logDIS` −0,140 → −0,139 (−0,9%); os dois com p HC3 < 0,001 |
| Linhas influentes | 28 nos dois modelos, 27 em comum (nova: 342; sai: 419). Sem as 28: $\hat\beta$ = −0,011, p HC3 = 0,50 |
| Alavanca | maior $h$ 0,342 contra 0,340 no modelo final ($2p/n$ = 0,085). Maior aumento: linha 269 (0,066 → 0,087) |
| Validação cruzada | final e com `ZN > 0`: RMSE 3,996, MAE 2,753, R² 0,788. A indicadora tem RMSE menor em 6 das 10 partes; a maior diferença por parte é 0,007 |
| Resíduos (final → com `ZN > 0`) | R² ajustado 0,881 nos dois; correlação QQ 0,993 nos dois; Shapiro-Wilk p 0,0012 → 0,0013; Breusch-Pagan p 6·10⁻¹² → 1·10⁻¹¹; RESET p 0,94 → 0,95; Durbin-Watson 1,41 nos dois |

**O que os resultados permitem concluir.**

- A indicadora **não entra** no modelo final: o Wald com HC3 não rejeita $\beta = 0$ (p = 0,85) e o RMSE da validação cruzada não muda (3,996 nos dois). Nenhuma das duas condições da regra vale.
- A diferença bruta (mediana de `MEDV` 25% maior com `ZN > 0`) é explicada pelos outros preditores. Os setores com lotes grandes são subúrbios com pouca indústria, `NOX` baixo e longe dos centros de emprego, e `NOX` e `logDIS` já estão no modelo.
- O resultado não vem de colinearidade (VIF 2,4) nem de pouco poder (131 linhas com `ZN > 0`): o IC 95% exclui efeitos maiores que cerca de 4% para os dois lados. Nenhuma linha decide o teste, ao contrário da interação da [Seção 20](12-interacoes.md).
- A decisão da Parte 8 ([Seção 16](08-modelo-final.md)) de deixar `ZN` fora vale também para a forma de indicadora.
- Limitações: a indicadora só muda entre cidades, e há 78 grupos `cidade`; os erros agrupados dão a mesma conclusão. O teste foi feito no MQO com HC3; a correlação espacial ([Seção 19](11-correlacao-espacial.md)) não foi considerada aqui.
