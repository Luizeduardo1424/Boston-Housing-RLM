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
| Densidade | `scipy.stats.gaussian_kde` (célula 4) | KDE gaussiano, largura de banda pela regra de **Scott** (padrão), na escala da frequência; classes do histograma pela regra `auto` do numpy | n/a |

Observações:

- Os valores ausentes são ignorados (`skipna=True`); em `RM`, as medidas usam 506 observações.
- Assimetria e curtose são **descritivas**. Nenhum teste formal de normalidade foi aplicado às variáveis. Os testes de normalidade são aplicados aos **resíduos**, na Parte 5 ([Seção 11.5](03-modelo-completo-residuos.md)).
- A normalidade **marginal** de `MEDV` ou de `logMEDV` **não é pressuposto** da RLM. O pressuposto é sobre os **erros** condicionais a $X$. A simetria de `logMEDV` é só um indício de que essa escala pode produzir resíduos mais próximos da normal.

Transformações (célula 25):

| Variável nova | Função | Motivo |
|---|---|---|
| `logCRIM`, `logZN` | `np.log1p(x)` = $\ln(1+x)$ | admite zeros (`ZN` tem muitos zeros) |
| `logDIS`, `logLSTAT`, `logMEDV` | `np.log(x)` | variáveis estritamente positivas |

`log1p` não é exatamente um logaritmo para valores pequenos ($\ln(1+x) \approx x$ quando $x \to 0$). Em `CRIM`, cujos valores são em sua maioria menores que 1, a transformação é mais fraca que $\ln(x)$.

---

## 4. Linearidade exploratória (células 29–30)

Função: `curva_lowess(x, y)` (célula 4), que chama `statsmodels.nonparametric.smoothers_lowess.lowess(y, x, frac=2/3)` **com os parâmetros padrão**:

| Parâmetro | Valor | Significado |
|---|---|---|
| `frac` | 2/3 | cada ajuste local usa 2/3 das observações (curva bastante suave) |
| `it` | 3 | 3 iterações **robustas** (pesos bisquare), que reduzem o peso de valores extremos |
| intervalo de confiança | não desenhado | a LOWESS não dá IC |
| ausentes | removidos | linhas com `NaN` em `x` ou `y` são descartadas |

Limitações:

- A curva mostra a relação **marginal** (bivariada) entre `MEDV` e cada preditor. A RLM supõe linearidade **condicional** aos demais preditores, que só pode ser avaliada com os resíduos do modelo: resíduos × ajustados e RESET na Parte 5 ([Seção 11.6](03-modelo-completo-residuos.md)) e resíduo parcial de `RM` na Parte 6 ([Seção 13](05-termo-quadratico-rm.md)).
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
| `MEDV` censurada em 50 (16 obs.) | média linear e erros normais na parte superior. O valor real pode ser maior que 50, então os resíduos dessas linhas são grandes e **positivos** (o modelo prevê 16–30 em 365–372) e as inclinações tendem a ser **atenuadas** | identificada. Na Parte 6, só como verificação (modelo sem `MEDV = 50`). Na Parte 10, tratada pelo modelo Tobit ([Seção 18](10-tobit.md)): a atenuação existe nos termos de `RM` (12% a 14%), mas é pequena e não muda as conclusões |
| 5 linhas suspeitas (índices 506–510) | todas as estimativas por momentos (assimetria, Pearson, VIF, MQO) | mantidas no modelo completo, removidas na sensibilidade (5.9), na seleção (grupo S) e na Parte 6 |
| 5 `RM` ausentes | número de observações e comparabilidade entre análises | excluídas por linha (`dropna`) em todos os modelos |
| `ZN` com excesso de zeros | linearidade da relação com `MEDV` | indicadora `ZN > 0` sugerida, não usada |
| `TAX` = 666 em todos os `RAD = 24` | multicolinearidade (GVIF de `TAX` ≈ 9,90) | `TAX` fica no modelo completo e sai da base da Parte 6 |
| Dados geográficos, arquivo ordenado por região | **independência** dos erros | rejeitada: teste das sequências z = −8,11; Durbin-Watson 0,95 ([Seção 11.4](03-modelo-completo-residuos.md)) |
