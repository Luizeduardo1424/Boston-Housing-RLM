## 22. Colinearidade entre `NOX` e `logDIS` (Parte 14, células 194–209)

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Dados | `df_final` (célula 118) | as 473 linhas do modelo final, para que todas as variantes sejam comparadas nas mesmas linhas. A validação cruzada usa `df_t` (501 linhas), como na célula 126 |
| GVIF por termo | `gvif_termos(m)` (célula 196) | GVIF de Fox & Monette, como `calcular_vif` (célula 4), mas na matriz de desenho do modelo ajustado: $\det R_{11} \det R_{22} / \det R$ com a matriz de correlação das colunas sem o intercepto. Os blocos vêm de `m.model.data.model_spec.term_name_slices` (patsy): `C(RAD)` é um termo com 8 GL; `RM_c` e `I(RM_c**2)` são dois termos. Para GL = 1, GVIF = VIF. $\text{GVIF}^{1/(2\,GL)}$ é comparável com $\sqrt{\text{VIF}}$, o fator de aumento do erro padrão |
| Número de condição | `numero_condicao(m)` (célula 196) | `np.linalg.cond` das colunas da matriz de desenho padronizadas (média 0, desvio 1) com a constante, como `calcular_numero_condicao` (célula 4). Referência: acima de 30 indica colinearidade forte (Belsley, Kuh e Welsch, 1980) |
| Correlações | `DataFrame.corr()` (célula 196) | Pearson entre os termos numéricos do modelo final e com `INDUS`, `AGE` e `TAX`, que saíram do modelo. Mede só a relação linear entre pares |
| Retirar variáveis | `smf.ols(...).fit(cov_type="HC3")` e `.fit()` (célula 198) | variantes de `formula_final` sem `NOX`, sem `logDIS` e sem as duas; a função `retirar` confere que o trecho trocado existe na fórmula. Mudança de cada coeficiente em erros padrão HC3 do modelo final: $(\hat\beta_v - \hat\beta_f)/EP_{\text{HC3}}$; acima de 1 é sinal de viés de variável omitida. AIC, BIC, R² ajustado, VIF e `resumir_residuos` no ajuste MQO clássico |
| Padronização | célula 200 | mostra que a correlação de Pearson não muda com $x \mapsto (x-a)/b$. A centralização só ajuda entre `x` e `x²` ([Seção 13](05-termo-quadratico-rm.md)) |
| Residualização | `smf.ols("logDIS ~ NOX", df_final)` (célula 200) | `logDIS_r` = resíduo; `NOX` e `logDIS_r` têm correlação zero e geram o mesmo espaço de colunas que `NOX` e `logDIS`, então o ajuste, os resíduos e as previsões são idênticos (`np.allclose`). O coeficiente de `NOX` passa a ser $\beta_{NOX} + \beta_{logDIS}\gamma$, com $\gamma$ a inclinação do modelo auxiliar |
| Índice combinado | `com_indice(treino, outros, colunas)` (célula 200) | primeira componente principal (`np.linalg.eigh` da matriz de correlação) das colunas padronizadas com a média e o desvio do treino. Sinal escolhido para o peso de `NOX` ser positivo. Duas versões: `NOX`, `logDIS`; e `NOX`, `logDIS`, `INDUS`, `AGE`. O índice entra no lugar de `NOX + logDIS` |
| Ridge | `make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 61)))` (célula 202) | matriz de desenho de `formula_final` (`patsy.dmatrices`) sem o intercepto, colunas padronizadas, resposta `logMEDV`. `RidgeCV` escolhe λ por validação cruzada interna (padrão: leave-one-out eficiente, erro quadrático). Volta à escala de `MEDV` com o smearing de Duan dos resíduos do treino. Não dá erros padrão: serve só como referência de previsão |
| `TAX` e `RAD` | célula 204 | (a) `TAX + C(RAD == 24)` no lugar de `C(RAD)`; (b) `C(RAD) + I(TAX * (RAD != 24))`, `TAX` só fora de `RAD = 24`. A interação `TAX:C(RAD != 24)` do patsy não foi usada: sem o efeito principal, ela cria uma coluna igual a 666 vezes a indicadora de `RAD = 24`, colinear com o bloco |
| `RM_c` e `logLSTAT_c` | célula 206 | sem `RM_c + I(RM_c**2)` e sem `logLSTAT + I(logLSTAT_c**2)` (termo linear e quadrado saem juntos); residualização de `logLSTAT` em `RM_c` |
| Validação cruzada | célula 208 | as mesmas partes da célula 126: `KFold(n_splits=10, shuffle=True, random_state=42).split(df_t)`, todas as linhas do treino, previsão por `prever_log`. O modelo auxiliar da residualização, os pesos do índice e o λ do Ridge são ajustados só no treino de cada parte |
| Regra de decisão | células 194 e 208 | o modelo final muda só se a variante tiver RMSE menor que o do modelo final **e** RESET p ≥ 0,05, p do Shapiro-Wilk não menor que o do final e maior VIF (termos com 1 GL) não maior que o do final. O Ridge fica fora da regra |

### 22.1 Resultados

| Etapa | Resultado |
|---|---|
| Correlações (`df_final`) | `NOX` × `logDIS` −0,84 (−0,83 em `df_t`); `logLSTAT` × `RM_c` −0,69; `NOX` × `logLSTAT` +0,60; `logDIS` × `logLSTAT` −0,56. `NOX` com `INDUS` 0,76, `AGE` 0,74, `TAX` 0,67; `logDIS` com `INDUS` −0,75, `AGE` −0,78, `TAX` −0,58 |
| GVIF do modelo final | `NOX` 4,81; `logDIS` 4,12; `logLSTAT` 3,71; `CRIM` 3,05; `RM_c` 2,32; os outros abaixo de 2. Bloco `C(RAD)`: GVIF 6,43, $\text{GVIF}^{1/16}$ = 1,12. Número de condição 9,8 |
| Erros padrão | `NOX`: β = −0,665, EP HC3 0,117, p = 1·10⁻⁸, $\sqrt{\text{VIF}}$ = 2,19. `logDIS`: β = −0,140, EP HC3 0,025, p = 1·10⁻⁸, $\sqrt{\text{VIF}}$ = 2,03 |
| Sem `NOX` | `logDIS` −0,140 → −0,048 (+3,8 EP); `PTRATIO` +1,4 EP; `C(RAD)[T.24]` −1,3 EP. R² ajustado 0,872; BIC −472; RESET p 0,42; Shapiro-Wilk p 0,0001; RMSE 4,24 |
| Sem `logDIS` | `NOX` −0,665 → −0,194 (+4,0 EP); `PTRATIO`, `logLSTAT`, `I(RM_c**2)` e `C(RAD)[T.2]` mudam de 1,1 a 1,3 EP. R² ajustado 0,871; BIC −470; RESET p 0,33; Shapiro-Wilk p 0,0003; RMSE 4,37 |
| Sem as duas | `PTRATIO` +1,6 EP. R² ajustado 0,870; BIC −470; maior VIF 2,97; RMSE 4,36 |
| Padronização | correlação −0,8364 antes e depois |
| Residualização | `logDIS = 3,315 − 3,806·NOX` (R² = 0,70). Resíduos idênticos ao modelo final. `NOX`: −0,665 (EP 0,117) → −0,131 (EP 0,080, p = 0,10); `logDIS_r` = −0,140, igual a `logDIS`. VIF de `NOX` 4,81 → 2,60. RMSE 3,996 |
| Índice (`NOX`, `logDIS`) | variância explicada 91,8%; pesos +0,707 e −0,707. β = 0,003 (EP HC3 0,007, p = 0,71). R² ajustado 0,870; RMSE 4,36 |
| Índice (com `INDUS`, `AGE`) | variância explicada 81,4%; pesos `NOX` +0,51, `logDIS` −0,52, `INDUS` +0,48, `AGE` +0,48. β = 0,003 (p = 0,63). RMSE 4,35 |
| Ridge | λ = 3,98 em `df_final`; encolhimento dos coeficientes padronizados de `NOX` 6,2% e de `logDIS` 7,0%; dos outros termos fora de `C(RAD)`, até 3,7%. RMSE 4,004, MAE 2,725, R² 0,788; melhor que o final em 5 das 10 partes |
| `TAX + C(RAD == 24)` | 112 linhas com `RAD = 24`, todas com `TAX = 666`. β de `TAX` −0,00036 (EP HC3 0,00009, p < 0,001). GVIF: `C(RAD == 24)` 7,86, `TAX` 7,08. 12 parâmetros (contra 19). R² ajustado 0,879; BIC −526; RESET p 0,72; Shapiro-Wilk p 0,0006; RMSE 3,960, MAE 2,714 (melhor em 5 das 10 partes) |
| `C(RAD) + TAX` fora de `RAD = 24` | β −0,00031 (EP 0,00009, p = 0,001). GVIF: `TAX` 6,94, bloco `C(RAD)` 21,3 ($\text{GVIF}^{1/16}$ = 1,21). Número de condição 11,1. R² ajustado 0,883; BIC −504; RESET p 0,95; Shapiro-Wilk p 0,0004; RMSE 3,947 (melhor em 8 das 10 partes) |
| Sem `RM` | `logLSTAT` −5,4 EP, `PTRATIO` −3,8, `logDIS` −3,0, `I(logLSTAT_c**2)` +2,7. R² ajustado 0,839; RESET p 0,0003; RMSE 4,29 |
| Sem `logLSTAT` | `RM_c` +8,0 EP, `logDIS` +2,9, `NOX` −2,5, `B` +2,0, `PTRATIO` −2,0. R² ajustado 0,813; Shapiro-Wilk p 2·10⁻⁶; RMSE 4,98 |
| `logLSTAT` residualizado | resíduos idênticos; `RM_c` 0,115 → 0,300. RMSE 3,996 |
| Regra de decisão | nenhuma variante cumpre. O Breusch-Pagan rejeita em todas (p < 10⁻⁶) |

**O que os resultados permitem concluir.**

- O modelo final **não muda**. As variantes que retiram `NOX`, `logDIS` ou as duas têm RMSE de 4,24 a 4,37 (contra 4,00), BIC cerca de 30 pontos pior e Shapiro-Wilk pior. As residualizadas são o mesmo modelo.
- Retirar uma das duas causa **viés de variável omitida**: o coeficiente da que fica muda cerca de 4 erros padrão HC3, porque ela passa a carregar o efeito da outra.
- A colinearidade **não é um problema para a inferência** no MQO do modelo final: os erros padrão de `NOX` e `logDIS` aumentam cerca de 2 vezes ($\sqrt{\text{VIF}}$), mas os dois têm p HC3 ≈ 10⁻⁸. VIF máximo 4,8 e número de condição 9,8 estão abaixo das referências usuais (VIF 5 a 10, condição 30).
- O coeficiente de `NOX` é o efeito com a distância fixa. O efeito de `NOX` quando `logDIS` muda junto (residualização) é bem menor (−0,131, p = 0,10). As duas leituras são do mesmo modelo; a escolha depende da pergunta.
- O índice por componente principal **não serve**: os dois coeficientes são negativos e as variáveis têm correlação negativa, então o efeito está na segunda componente (8% da variância), e a primeira o anula. Juntar variáveis correlacionadas num índice supõe efeitos no mesmo sentido do índice, e isso não vale aqui.
- O Ridge quase não muda a previsão (RMSE 4,004): a variância extra dos coeficientes não prejudica a previsão do MQO.
- `TAX` tem informação além de `RAD` (p < 0,001 nas duas variantes) e melhora o RMSE em cerca de 1% (3,95 e 3,96). Pela regra, a decisão de deixar `TAX` fora continua valendo, porque o VIF sobe (7,9 e 6,9) e o Shapiro-Wilk piora. A variante `TAX + C(RAD == 24)` tem o melhor BIC (−526, com 7 parâmetros a menos) e fica como candidata para a comparação de modelos (tarefa 08).
- `RM_c` e `logLSTAT_c` também precisam ficar juntos: retirar um deles muda os coeficientes do outro em 5 a 8 erros padrão, piora o RMSE (4,29 e 4,98) e, sem `RM`, o RESET rejeita.
- Limitações: VIF e número de condição medem só colinearidade linear entre as colunas. A análise usa o MQO com HC3; a perda de significância de `logDIS` no modelo de erro espacial ([Seção 19](11-correlacao-espacial.md)) é coerente com o que foi visto aqui (`logDIS` é uma variável espacial, e o erro espacial absorve parte da mesma variação), mas não foi testada.
