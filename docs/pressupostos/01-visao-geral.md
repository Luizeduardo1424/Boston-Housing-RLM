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
