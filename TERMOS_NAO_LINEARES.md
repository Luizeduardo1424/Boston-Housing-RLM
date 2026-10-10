# Termos de potência e de interação no modelo

Este documento explica quando faz sentido usar **potências** de uma variável (por exemplo, `RM²`) e **produtos entre variáveis** (por exemplo, `RM·LSTAT`) na Regressão Linear Múltipla deste projeto, e quais variáveis do dataset são candidatas.

> Os números das seções 4 e 5 vêm de uma verificação exploratória, não do modelo final. Eles indicam o que vale testar, mas a decisão final deve considerar os diagnósticos dos resíduos e a validação cruzada.

---

## 1. O que são esses termos

### 1.1 Termo de potência (polinomial)

Em vez de somente $\beta_1 X$, o modelo recebe também $\beta_2 X^2$:

$$
Y = \beta_0 + \beta_1 X + \beta_2 X^2 + \varepsilon
$$

O efeito de $X$ sobre $Y$ deixa de ser constante e passa a **depender do próprio valor de $X$**:

$$
\frac{\partial Y}{\partial X} = \beta_1 + 2\beta_2 X
$$

- $\beta_2 > 0$: curva convexa (o efeito aumenta conforme $X$ aumenta).
- $\beta_2 < 0$: curva côncava (o efeito diminui, podendo mudar de sinal).

Isso permite representar curvaturas como o "joelho" observado em `DIS` na EDA.

### 1.2 Termo de interação (produto)

O modelo recebe o produto de duas variáveis:

$$
Y = \beta_0 + \beta_1 X + \beta_2 Z + \beta_3 X Z + \varepsilon
$$

O efeito de $X$ passa a **depender do valor de $Z$**:

$$
\frac{\partial Y}{\partial X} = \beta_1 + \beta_3 Z
$$

Exemplo: o valor de um cômodo a mais (`RM`) pode ser diferente em regiões ricas e em regiões pobres (`LSTAT`).

### 1.3 Continua sendo regressão linear

Os dois tipos de termo mantêm o modelo **linear nos parâmetros** $\beta$. A matriz de design apenas ganha novas colunas ($X^2$, $XZ$). Assim, todo o ferramental de RLM continua válido: mínimos quadrados, testes t e F, $R^2$ ajustado, VIF e diagnóstico de resíduos.

---

## 2. Quando faz sentido usar

Um termo novo só deve entrar no modelo quando existe **evidência** e, de preferência, uma **justificativa teórica**.

**Sinais a favor:**

- curva LOWESS claramente não linear nos gráficos de dispersão (Parte 3 da EDA);
- padrão curvo nos gráficos de resíduos contra um preditor, após o ajuste do modelo;
- teste F parcial (modelos aninhados) significativo ao adicionar o termo;
- melhora do $R^2$ ajustado, do AIC/BIC e, principalmente, do RMSE em validação cruzada;
- interpretação prática plausível.

**Riscos:**

- **Sobreajuste**: com 13 preditores, há 13 quadrados e 78 interações possíveis. Testar todos aumenta muito a chance de encontrar termos significativos por acaso. Teste poucos termos, escolhidos com critério.
- **Multicolinearidade**: $X$ e $X^2$ são quase colineares. Neste dataset, a correlação entre `RM` e `RM²` é **0,99**. Depois de **centralizar** `RM` (subtrair a média), a correlação cai para **0,21**. Sempre centralize antes de criar potências e produtos.
- **Princípio da hierarquia**: se $X^2$ ou $XZ$ estiver no modelo, mantenha também $X$ (e $Z$), mesmo que seu p-valor seja alto.
- **Interpretação mais difícil**: o coeficiente de $X$ sozinho deixa de ser "o efeito de $X$". Com variáveis centralizadas, ele passa a ser o efeito de $X$ **no ponto médio** dos dados.
- **Extrapolação**: um polinômio pode ter comportamento estranho fora da faixa observada.

**Potência, log e interação competem entre si.** Uma mesma curvatura pode ser representada por `log(X)`, por `X²` ou, às vezes, por uma interação. Neste dataset, a interação `RM·LSTAT` é muito forte na escala original, mas **desaparece** quando `LSTAT` entra como `logLSTAT` (seção 5). Ela estava apenas compensando a curvatura de `LSTAT`. Por isso, defina primeiro as transformações e só depois teste interações.

---

## 3. Análise variável por variável

| Variável | Potência faz sentido? | Motivo |
| --- | --- | --- |
| `RM` | **Sim, forte** | Imóveis com muitos cômodos valorizam mais que proporcionalmente (efeito convexo). Foi o termo quadrático mais forte em todas as especificações. |
| `LSTAT` | **Sim, mas compete com o log** | Relação fortemente curva (Spearman −0,82 contra Pearson −0,56). `logLSTAT` já resolve a maior parte; `logLSTAT²` ainda traz um ganho pequeno. |
| `DIS` | **Sim, compete com o log** | Formato de joelho na EDA. `DIS²` é significativo na escala original; `logDIS` é a alternativa. Use um ou outro, não os dois sem motivo. |
| `CRIM` | Fraco | `CRIM²` tem ganho pequeno (p = 0,03). Também há a opção `logCRIM`, que aumenta o VIF (ver Parte 4 da EDA). |
| `NOX` | Não | `NOX²` não foi significativo. |
| `AGE` | Não | `AGE²` não foi significativo. |
| `INDUS`, `PTRATIO`, `TAX` | Não indicado | A EDA não mostrou curvatura relevante. `TAX` já tem problema de colinearidade com `RAD`. |
| `ZN` | Não | O problema é o excesso de zeros, não curvatura. A EDA sugere uma indicadora `ZN > 0`. |
| `B` | Não | `B` já é uma transformação quadrática: $1000(B_k − 0,63)^2$. Elevar de novo não tem interpretação. |
| `CHAS` | **Não se aplica** | Variável 0/1: $0^2 = 0$ e $1^2 = 1$, então `CHAS² = CHAS`. |
| `RAD` | **Não se aplica** | É um fator categórico (8 indicadoras). Cada nível já tem seu próprio coeficiente, o que representa qualquer formato. Elevar códigos de categoria ao quadrado não faz sentido. |

---

## 4. Interações candidatas

| Interação | Pergunta prática | Resultado |
| --- | --- | --- |
| `RM · LSTAT` | O valor de um cômodo a mais depende do nível socioeconômico da região? | Muito forte na escala original, mas desaparece com `logLSTAT`. Provavelmente é curvatura de `LSTAT`, não interação real. |
| `RM · PTRATIO` | Imóveis grandes valem mais onde as escolas têm menos alunos por professor? | Significativo na escala original (p ≈ 1e-7), mas fraco no modelo com logs e `RM²` (p = 0,09). Tem boa justificativa, mas pouca evidência depois das transformações. |
| `NOX · DIS` | O efeito da poluição muda com a distância dos centros de emprego? | Nulo na escala original; pequeno com `logDIS` (p = 0,02). Fraco. |
| `CHAS · RM` | O efeito de cômodos é diferente perto do rio? | Não significativo. O grupo `CHAS = 1` tem apenas 35 observações. |
| `RAD=24 · CRIM` | O efeito da criminalidade é diferente no grupo `RAD = 24`? | Pequeno (p = 0,05). Fraco. |
| `RM · CRIM` | O efeito de cômodos depende da criminalidade? | Significativo na escala original, desaparece com logs. |
| `LSTAT · AGE` | — | Não significativo. |

Interações entre uma variável numérica e um fator (`CHAS`, `RAD`) significam **inclinações diferentes por grupo**. Elas consomem um grau de liberdade por nível. Com `RAD` em 8 indicadoras, cada interação com `RAD` custa 8 parâmetros, e alguns níveis têm menos de 25 observações. Se testar, prefira a versão agrupada `RAD = 24` contra os demais.

---

## 5. Evidência exploratória

**Como foi calculado:**

- 501 observações: foram removidas as 5 linhas suspeitas (índices 506 a 510) e as 5 linhas com `RM` ausente;
- variável resposta `logMEDV`;
- `CHAS` e `RAD` como fatores;
- variáveis centralizadas antes de criar potências e produtos;
- cada termo foi adicionado **sozinho** a um modelo base, e comparado pelo teste F parcial.

Modelos base:

- **Escala original:** `CRIM + ZN + INDUS + CHAS + NOX + RM + AGE + DIS + RAD + PTRATIO + B + LSTAT` ($R^2$ ajustado = 0,783; AIC = −216,2)
- **Com logs:** igual, mas com `logDIS` e `logLSTAT` ($R^2$ ajustado = 0,796; AIC = −246,2)

| Termo adicionado | Base original: $R^2_{aj}$ | p-valor | Base com logs: $R^2_{aj}$ | p-valor |
| --- | --- | --- | --- | --- |
| `RM²` | 0,783 → **0,809** | 4e-15 | 0,796 → **0,802** | 4e-5 |
| `LSTAT²` / `logLSTAT²` | 0,783 → 0,797 | 9e-9 | 0,796 → 0,799 | 0,001 |
| `DIS²` | 0,783 → 0,788 | 7e-4 | — | — |
| `CRIM²` | 0,783 → 0,785 | 0,03 | — | — |
| `NOX²` | 0,783 → 0,783 | 0,19 | 0,796 → 0,796 | 0,10 |
| `AGE²` | 0,783 → 0,783 | 0,28 | — | — |
| `RM·LSTAT` / `RM·logLSTAT` | 0,783 → **0,808** | 8e-15 | 0,796 → 0,795 | 0,45 |
| `RM·PTRATIO` | 0,783 → 0,795 | 9e-8 | — | — |
| `RM·CRIM` | 0,783 → 0,787 | 0,002 | 0,796 → 0,795 | 0,99 |
| `NOX·DIS` | 0,783 → 0,782 | 0,84 | 0,796 → 0,797 | 0,02 |
| `CHAS·RM` | 0,783 → 0,783 | 0,73 | 0,796 → 0,796 | 0,10 |
| `RAD=24·CRIM` | 0,783 → 0,784 | 0,05 | — | — |
| `LSTAT·AGE` | 0,783 → 0,783 | 0,14 | — | — |

Na base com logs, adicionar `RM²` e `RM·logLSTAT` juntos levou o $R^2$ ajustado de 0,796 para 0,805 (AIC −267,6).

**Leitura da tabela:**

1. Os maiores ganhos estão em **`RM²`** e na curvatura de **`LSTAT`**.
2. Depois que os logs entram, os ganhos dos termos extras ficam pequenos (menos de 1 ponto de $R^2$ ajustado). As transformações da EDA já capturam a maior parte da não linearidade.
3. Interações fortes na escala original (`RM·LSTAT`, `RM·CRIM`) somem com os logs, ou seja, eram efeito de curvatura.

---

## 6. Recomendação: isso cria um modelo melhor?

**Sim, para poucos termos bem escolhidos.** Principalmente `RM²`. Não vale a pena adicionar muitos termos: o ganho depois dos logs é pequeno, e cada termo novo deixa o modelo mais difícil de interpretar.

Sequência sugerida para a etapa de modelagem:

1. Ajustar o modelo base com as transformações da EDA (`logLSTAT`, `logDIS` ou `DIS`, `RAD` como fator, decisão sobre `TAX`).
2. Adicionar **`RM²` centralizado**. É o termo com melhor evidência e uma interpretação clara (ver seção 7 e a Parte 6 do notebook).
3. Testar a curvatura restante de `LSTAT` (`logLSTAT²`) e escolher entre `logDIS` e `DIS + DIS²`.
4. Testar **no máximo 1 ou 2 interações** com justificativa teórica, como `RM·PTRATIO`. No exemplo abaixo, depois de `RM²` ela tem p = 0,09: mantenha apenas se a validação cruzada mostrar ganho.
5. Comparar os modelos com teste F parcial, AIC/BIC e **RMSE em validação cruzada**.
6. Recalcular o VIF e verificar os resíduos contra cada preditor do modelo final.

Exemplo com `statsmodels`:

```python
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

# Centraliza antes de criar potências e produtos
for v in ["RM", "logLSTAT", "PTRATIO"]:
    df[f"{v}_c"] = df[v] - df[v].mean()

base = ("logMEDV ~ CRIM + ZN + INDUS + C(CHAS) + NOX + RM + AGE + logDIS"
        " + C(RAD) + PTRATIO + B + logLSTAT")

m0 = smf.ols(base, data=df).fit()
m1 = smf.ols(base + " + I(RM_c**2)", data=df).fit()
m2 = smf.ols(base + " + I(RM_c**2) + RM_c:PTRATIO_c", data=df).fit()

print(anova_lm(m0, m1, m2))  # teste F parcial entre modelos aninhados
print(m0.aic, m1.aic, m2.aic)
```

Na fórmula, `I(RM_c**2)` cria a potência e `RM_c:PTRATIO_c` cria somente o produto. `RM_c*PTRATIO_c` cria os dois efeitos principais **mais** o produto.

---

## 7. Por que `RM²` centralizado faz sentido

A ideia em uma frase: **um cômodo a mais não vale o mesmo em todas as casas.** Uma reta obriga um valor fixo por cômodo. O termo `RM²` deixa esse valor mudar com o tamanho da casa. O cálculo completo está na **Parte 6** de `notebooks/02-MRLM.ipynb` (mesmos dados da seção 5: 501 observações, resposta `logMEDV`).

### 7.1 Os dados mostram uma curva, não uma reta

Mediana de `MEDV` por faixa de `RM`:

| RM | Regiões | Mediana de MEDV (mil US$) | Ganho em relação à faixa anterior |
| --- | --- | --- | --- |
| ≤ 5,0 | 16 | 13,8 | — |
| 5,0–5,5 | 26 | 14,4 | +0,6 |
| 5,5–6,0 | 130 | 19,0 | +4,6 |
| 6,0–6,5 | 178 | 21,2 | +2,2 |
| 6,5–7,0 | 87 | 26,6 | +5,4 |
| 7,0–7,5 | 37 | 33,3 | +6,7 |
| 7,5–9,0 | 27 | 46,7 | +13,4 |

Cada faixa acrescenta meio cômodo, mas o salto de preço fica cada vez maior. Uma curva que fica mais inclinada conforme avança é **convexa**, e uma reta não consegue representá-la.

### 7.2 O que o modelo diz sobre um cômodo a mais

| Tamanho da casa (RM) | Modelo linear (só RM) | Modelo com RM² |
| --- | --- | --- |
| 6,0 | +7,1% | +4,8% |
| 6,28 (média) | +7,1% | +7,2% |
| 7,0 | +7,1% | **+13,4%** |
| 8,0 | +7,1% | **+22,8%** |

O modelo linear dá a todo cômodo extra o mesmo valor médio, +7,1%. Assim, ele **superestima** o preço das casas pequenas e **subestima** o das grandes. Com `RM²`, o efeito de um cômodo é $\beta_1 + 2\beta_2(RM - \overline{RM})$, com $\beta_2 \approx 0{,}039 > 0$: cada cômodo extra vale mais que o anterior.

Nos resíduos, o modelo linear tem resíduo médio de **+0,083** nas casas com 7,5 a 9 cômodos (subestima o preço). Com `RM²`, esse valor cai para **+0,007**, e todas as faixas de `RM` ficam perto de zero.

### 7.3 Por que isso faz sentido na prática

- A maioria das casas tem cerca de 5,5 a 6,5 cômodos. Nessa faixa, um cômodo a mais é uma mudança pequena, e o mercado paga um valor moderado por ele.
- Regiões com 7 a 8 ou mais cômodos são outro produto: casas grandes e de alto padrão em bairros ricos. Entrar nesse grupo aumenta o preço muito mais que o valor de um cômodo de espaço.
- Assim, a curva mostra que **o tamanho funciona como sinal de um bairro de alto padrão**, e esse efeito cresce rapidamente no topo.
- O estudo original do Boston Housing (Harrison & Rubinfeld, 1978) já usava `RM²`. Esse padrão não foi criado pelos dados deste trabalho.

### 7.4 Por que "centralizado" (RM − 6,28 em vez de RM)

As duas versões têm **o mesmo ajuste e as mesmas previsões** (mesmo AIC). A centralização muda apenas a leitura e a estabilidade dos coeficientes:

| | `RM`, `RM²` brutos | `RM_c`, `RM_c²` centralizados |
| --- | --- | --- |
| Correlação entre os dois termos | 0,99 | 0,21 |
| VIF entre os dois termos | **91,7** | **1,0** |
| Coeficiente de RM | −0,43 (EP 0,12) | 0,070 (EP 0,017) |
| Significado | Efeito de um cômodo quando RM = 0, o que não existe | Efeito de um cômodo na casa **média** (+7,2%) |

- Sem centralizar, `RM` e `RM²` são quase a mesma coluna. Isso infla o VIF e gera um coeficiente negativo para `RM` sem significado.
- Com a centralização, o coeficiente de `RM` mantém o sentido usual ("um cômodo a mais na casa média"), e o coeficiente do quadrado diz apenas quanto a curva se dobra.

### 7.5 Evidência

- Teste F parcial ao adicionar `RM²`: p ≈ 4 × 10⁻⁵. AIC de −246 para −262; R² ajustado de 0,796 para 0,802.
- **Sem as 16 observações censuradas** (`MEDV = 50`), `RM²` continua positivo e significativo ($\beta_2 \approx 0{,}047$; p ≈ 8 × 10⁻⁶). Assim, o efeito convexo **não** é causado pela censura.
- **Teste RESET:** o p-valor piora com `RM²` (de 0,29 para 0,0002), mas isso não indica um problema com `RM²`. A rejeição vem das casas **mais baratas** (menor quintil do valor ajustado, resíduo médio de −0,07), ou seja, de outra curvatura, ligada principalmente a `LSTAT`. Com um termo `logLSTAT²`, o p-valor do RESET sobe para 0,14. No modelo linear, as duas curvaturas se compensavam, e o RESET não as detectava.

### 7.6 Cuidados

- O vértice da parábola fica em `RM` ≈ 5,4. Abaixo dele, a curva desce um pouco (−3% por cômodo em `RM` = 5). Há apenas 42 regiões com `RM` < 5,5, então isso é a borda da parábola e não um resultado real.
- Não use o modelo para prever fora da faixa de 5 a 8,5 cômodos.
- A curvatura que ainda resta (casas mais baratas) deve ser tratada na modelagem final, por exemplo com `logLSTAT²`.

---

## Referências

- Montgomery, D. C.; Peck, E. A.; Vining, G. G. *Introduction to Linear Regression Analysis*. Wiley, 2012. Capítulo 7 (modelos polinomiais).
- Harrison, D.; Rubinfeld, D. L. (1978). *Hedonic prices and the demand for clean air*. O artigo original já usa `RM²` e `log(LSTAT)`.
