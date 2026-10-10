## 14. Transformações, centralização e erros robustos (Parte 7, células 47–62)

Células do notebook [`02-MRLM.ipynb`](../../notebooks/02-MRLM.ipynb).

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Amostra | `df_t = df_rm.copy()` | a mesma da Parte 6 (n = 501). Todas as especificações usam as mesmas linhas, então os testes são comparáveis |
| Padronização | `(X − média) / desvio padrão` (`std` do pandas, `ddof=1`) nos 11 preditores numéricos | `CHAS` e `RAD` ficam como indicadoras. É uma mudança afim das colunas: o espaço gerado por $X$ (com intercepto) é o mesmo, então $\hat y$ e os resíduos são idênticos (`np.allclose`) |
| Box-Cox da resposta | `perfil_boxcox` (célula 51), feita à mão | perfil de verossimilhança $\ell(\lambda) = -\tfrac n2 \log(SQR(\lambda)/n)$ com a resposta dividida por $\dot y^{\lambda-1}$ (média geométrica), em uma grade de −0,6 a 1 com passo 0,01. IC 95% pela razão de verossimilhança ($\chi^2_1$). Supõe que existe um $\lambda$ com erros normais e homocedásticos. Calculado para dois conjuntos de preditores, pois $\hat\lambda$ depende de $X$ |
| Box-Cox marginal | `stats.boxcox(MEDV)` | $\lambda$ da distribuição de `MEDV` **sem** preditores. Só para comparação: o pressuposto é sobre os erros, não sobre $Y$ |
| Preditores | `stats.boxcox` (valores > 0) ou `stats.yeojohnson` (`ZN`, com zeros) | $\lambda$ por máxima verossimilhança da distribuição **marginal** de cada preditor. É um guia de simetria; a RLM não supõe preditores normais |
| Comparação | `diagnosticar` (célula 55) | correlação QQ e Shapiro-Wilk com o resíduo **externo**; assimetria, curtose, Breusch-Pagan, RESET e Durbin-Watson com o **bruto** (iguais aos da [Seção 11](03-modelo-completo-residuos.md)). AIC só entre modelos com a mesma resposta |
| Fonte da heterocedasticidade | `ols("e2 ~ ...").wald_test_terms()` | regressão auxiliar de $e^2$ sobre os termos do modelo E, com teste F de cada termo (covariância não robusta). Indica **quais** termos explicam a variância; não é o teste de Breusch-Pagan global |
| Erros robustos | `fit(cov_type="HC3")` | estimador sanduíche $(X'X)^{-1} X' \operatorname{diag}\!\big(e_i^2/(1-h_{ii})^2\big) X (X'X)^{-1}$. **Não** supõe variância constante, mas supõe erros **independentes**. Os coeficientes são os mesmos do MQO |
| Testes por termo | `wald_test_terms(scalar=True)` | teste de Wald de cada termo, com `RAD` como bloco de 8 indicadoras. Com HC3, a estatística F usa a covariância robusta |

Resultados que atualizam a [Seção 15](07-pendencias.md): com HC3 no modelo E, os erros padrão são em média 23% maiores, mas **nenhuma variável muda de conclusão** a 5%.

### 14.1 Limitação: independência dos erros

**O que o notebook faz.** A independência é verificada só pela **ordem das linhas do arquivo**:

| Onde | Teste | Resultado |
|---|---|---|
| Parte 5 (células 16 e 21), modelo completo | teste das sequências e Durbin-Watson ([Seção 11.4](03-modelo-completo-residuos.md)) | z = −8,11; DW = 0,95 |
| Parte 5 (continuação), 12 modelos distintos | Durbin-Watson em `avaliar` ([Seção 12.2](04-selecao-modelos.md)) | DW entre 0,95 e 1,27 |
| Parte 7 (célula 55), modelos A a E | Durbin-Watson em `diagnosticar` | DW entre 1,09 e 1,19 |
| Parte 7 (célula 57), modelo E com `log`, `raiz` e λ ótimo | Durbin-Watson em `diagnosticar` | DW entre 1,15 e 1,19 |

Um DW perto de 2 indica ausência de autocorrelação. Valores perto de 1 indicam **autocorrelação positiva**: resíduos de linhas vizinhas têm o mesmo sinal. Como o arquivo está ordenado por região, linhas vizinhas são regiões vizinhas, e o resultado indica **dependência espacial** ([Seção 11.4](03-modelo-completo-residuos.md)).

**Por que as transformações não resolvem.** Log, Box-Cox, centralização e termos quadráticos mudam a escala e a forma da relação entre as variáveis. Eles não mudam a **relação entre as observações**. Em todas as especificações da Parte 7, o DW fica entre 1,09 e 1,19. A diferença para a Parte 5 (0,95) vem da remoção das 5 linhas suspeitas: o modelo A, ainda sem transformações, já tem DW de 1,09. Remover outliers e pontos influentes (Parte 5, continuação) leva o DW no máximo a 1,27. Assim, a autocorrelação não é causada por alguns pontos atípicos nem pela forma funcional: é dependência entre regiões.

**Por que o HC3 também não resolve.** Os erros padrão HC3 corrigem a variância **não constante**, mas supõem erros **independentes** (matriz de covariância diagonal). Com dependência positiva entre vizinhos, a informação efetiva da amostra é menor que n = 501. Assim, mesmo com HC3, os erros padrão do notebook devem estar **subestimados**, e os p-valores e intervalos de confiança são **otimistas**.

**Consequências para a leitura dos resultados.**

- Os **coeficientes** continuam não viesados (o MQO não exige independência para isso), mas não são os mais eficientes.
- Os **p-valores** devem ser lidos como **aproximados**. Termos com p-valor perto de 0,05 (`CHAS` e `B` com HC3, Seção 14) são os mais sensíveis a esse problema.
- O **R²** e os gráficos de diagnóstico continuam válidos como descrição do ajuste. Os **testes** dos outros pressupostos (RESET, Breusch-Pagan, Shapiro-Wilk) também supõem independência, então seus p-valores também são aproximados.

**O que não foi feito.** O conjunto de dados do Kaggle não traz as coordenadas nem o nome da cidade de cada região. Sem isso, não é possível:

- calcular o **I de Moran** dos resíduos, que é o teste direto de dependência espacial;
- usar **erros padrão agrupados por cidade** (`cov_type="cluster"`) com a cidade real, ou **erros padrão espaciais** (Conley). A Parte 8 usa uma cidade **aproximada** (mesmos `TAX`, `PTRATIO`, `INDUS` e `ZN`; [Seção 16](08-modelo-final.md));
- ajustar um **modelo espacial** (defasagem ou erro espacial).

Os erros padrão HAC (Newey-West, `cov_type="HAC"`) usariam a ordem do arquivo como se fosse tempo. Eles não foram usados, pois a ordem é só uma aproximação da vizinhança. Por isso, a independência dos erros fica registrada como **limitação do modelo**.
