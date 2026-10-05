## 19. Correlação espacial (Parte 11, células 154–167)

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Fonte das coordenadas | `data/boston_corrected.csv` (célula 156) | versão corrigida do Boston Housing (Gilley e Pace, 1996; Pace e Gilley, 1997), baixada da StatLib (`https://lib.stat.cmu.edu/datasets/boston_corrected.txt`) em 05/10/2026. 506 linhas. Colunas `OBS`, `TOWN`, `TOWN_ID`, `TRACT`, `LON`, `LAT`, `MEDV`, `CMEDV` e as 13 variáveis explicativas. As colunas `OBS.` e `TOWN#` do arquivo original viraram `OBS` e `TOWN_ID`. `LON` e `LAT` são a posição do setor censitário |
| Ligação | `boston_c.loc[dados.index]` (célula 156) | pelo índice: `df_t` e `df_final` vêm de `df.loc[:505]` (célula 86) e mantêm o índice do arquivo, que segue a ordem da fonte. Conferência variável por variável com `np.isclose(..., atol=1e-3)`. A análise continua com `MEDV`, e não com `CMEDV`, para manter a comparação com as partes anteriores |
| Distâncias | `coordenadas_km` (célula 156) | km aproximados: $x = LON \cdot 111{,}32 \cos(\overline{LAT})$, $y = LAT \cdot 110{,}57$. Na escala da região (cerca de 40 km), a aproximação plana tem erro desprezível |
| Mapa dos resíduos | célula 156 | resíduos do `modelo_final` por `LON` e `LAT`, escala divergente simétrica (`RdBu_r`). Salvo em `results/figures/residuos_mapa.png` |
| Matriz KNN | `KNN.from_array(xy, k=6)`, `transform = "r"` (célula 158) | 6 vizinhos mais próximos por setor; padronizada por linha ($Wy$ = média dos vizinhos). Não é simétrica. Todos os setores têm vizinhos |
| Matriz de distância | `DistanceBand(xy, threshold=d, binary=True)`, `transform = "r"` (célula 158) | $d$ = `min_threshold_distance(xy)` = 5,27 km, o menor limiar sem setor isolado. Vizinhos por setor: mín. 1, mediana 88, máx. 204. Serve de verificação da escolha da matriz |
| I de Moran | `esda.moran.Moran(resid, w, permutations=999)` (célula 160) | `np.random.seed(42)` antes de cada chamada. `p_norm`: aproximação normal sob aleatorização; `p_sim`: unilateral por permutação ($I$ simulado ≥ observado), mínimo 0,001. Aplicado aos resíduos de MQO como se fossem erros: a média e a variância exatas para resíduos de regressão são ligeiramente diferentes, o que os testes LM tratam. Conferência: resíduos embaralhados entre os locais (`default_rng(42)`) |
| Testes LM | `spreg.OLS(y, X, w=w, spat_diag=True, moran=True)` (célula 162) | $X$ de `patsy.dmatrices(formula_final, df_final)` sem o intercepto (o spreg acrescenta). Confere que $\hat\beta$ = `modelo_final.params`. LM erro, LM defasagem, versões robustas (Anselin et al., 1996) e SARMA, todos $\chi^2$ assintóticos e com erros homocedásticos. Regra de decisão: o robusto de maior estatística |
| Modelos espaciais (ML) | `spreg.ML_Error`, `spreg.ML_Lag`, `method="full"` (célula 162) | SEM: $y = X\beta + u$, $u = \lambda W u + \varepsilon$. SAR: $y = \rho W y + X\beta + \varepsilon$. Máxima verossimilhança com $\varepsilon \sim N(0, \sigma^2 I)$; $W$ exógena e fixa. Comparados por log-verossimilhança e AIC. A saída de texto e os avisos do otimizador (`minimize_scalar` limitado) são descartados |
| SEM robusto | `spreg.GM_Error_Het(y, X, w=W_knn)` (célula 164) | GMM de Arraiz et al. (2010), robusto a heterocedasticidade de forma desconhecida e sem supor normalidade. É o estimador de referência, porque a variância não é constante ([Seção 17](09-heterocedasticidade.md)). Erros padrão e p-valores (normal) do próprio estimador |
| Resíduos após o modelo | célula 164 | I de Moran (KNN, 999 permutações) nos resíduos filtrados do SEM, $\hat\varepsilon = (I - \hat\lambda W)\hat u$ (`e_filtered`), e nos resíduos do SAR (`u`) |
| Comparação | `comparacao_espacial` (célula 164) | MQO com HC3 contra SEM (ML) e SEM (GMM het.); mudança em erros padrão HC3 do MQO, como na [Seção 18](10-tobit.md); efeito em % de `MEDV`: $100\,(e^\beta - 1)$ |
| Agrupamento por `TOWN` | `cov_type="cluster"`, `groups = pd.factorize(TOWN)[0]` (célula 166) | como na célula 122 ([Seção 16](08-modelo-final.md)), mas com a cidade verdadeira. Concordância com `cidade` pelo índice de Rand ajustado (`sklearn.metrics.adjusted_rand_score`) e pela fração de linhas cujo grupo aproximado tem a sua cidade como a mais frequente. Supõe independência entre cidades |

### 19.1 Resultados

| Etapa | Resultado |
|---|---|
| Ligação | `df_t`: 501 de 501 linhas iguais em 13 variáveis; `CRIM` igual em 500. `df_final`: 473 de 473 em 13 variáveis; `CRIM` em 472. A divergência é a linha 500: `CRIM` = 0,177783 em `housing.csv` e 0,22438 na fonte |
| `CMEDV` | difere de `MEDV` em 8 linhas de `df_t` (6 em `df_final`): linhas 7, 38, 190, 240, 437, 442, 454 e 505 |
| I de Moran, `modelo_final` (473) | KNN: I = 0,321, E[I] = −0,002, z = 13,0, p normal ≈ 10⁻³⁹, p permutação = 0,001. Distância: I = 0,046, z = 4,6, p permutação = 0,002 |
| I de Moran, `modelo_reduzido` (501) | KNN: I = 0,384, z = 16,0, p permutação = 0,001. Distância: I = 0,034, z = 3,7, p permutação = 0,003 |
| Conferência (ordem aleatória) | I = −0,016, p permutação = 0,31 |
| Testes LM (KNN) | LM erro 165; LM defasagem 112; LM erro robusto 81,0 (p ≈ 10⁻¹⁹); LM defasagem robusto 27,9 (p ≈ 10⁻⁷); SARMA 193 |
| Testes LM (distância) | LM erro 18,0; LM defasagem 14,1; LM erro robusto 10,8 (p = 0,001); LM defasagem robusto 6,9 (p = 0,009) |
| Ajustes (KNN) | MQO: logL 309,0, AIC −580. SEM: $\hat\lambda$ = 0,770 (z = 23,0), logL 389,4, AIC −741. SAR: $\hat\rho$ = 0,357 (z = 11,6), AIC −688 |
| Ajustes (distância) | SEM: $\hat\lambda$ = 0,867, AIC −610. SAR: $\hat\rho$ = 0,184, AIC −590 |
| SEM por GMM het. | $\hat\lambda$ = 0,693 (EP 0,035) |
| I de Moran depois | SEM (ML), filtrados: I = −0,041, p = 0,064. SEM (GMM het.), filtrados: I = −0,020, p = 0,25. SAR: I = 0,169, p = 0,001 |
| Coeficientes: SEM (GMM het.) × MQO | `CHAS` 0,091 → 0,022 (+9,6% → +2,2%; −3,1 EP HC3; p = 0,25; no ML, −0,001). `logDIS` −0,140 → −0,073 (2,8 EP; p = 0,072). `PTRATIO` −0,027 → −0,021 (2,1 EP). `logLSTAT` −0,311 → −0,269 (2,0 EP). `logLSTAT_c²` −0,089 → −0,054 (1,8 EP). `CRIM` −0,017 → −0,012 (1,6 EP). `NOX` −0,665 → −0,541 (1,1 EP). `RM_c` 0,115 → 0,125 (0,7 EP); `RM_c²` 0,068 → 0,061 (−0,9 EP) |
| Significância no SEM (GMM het.) | p ≥ 0,05: `CHAS`, `logDIS`, `RAD` = 2, 4, 6 e 8. Os demais termos continuam com p < 0,001 (exceto `RAD` = 5, 7 e 24, com p entre 0,003 e 0,012) |
| `TOWN` × `cidade` | 91 cidades em `df_final` (mediana de 4 linhas; maior: Cambridge, 28) contra 78 grupos aproximados. Rand ajustado 0,417; 81,2% das linhas no grupo da sua cidade mais frequente |
| Erros agrupados por `TOWN` | todos os termos com p < 0,05 (maior: `CHAS`, 0,019; `B`, 0,004). Razão EP `TOWN` / HC3 de 1,07 (`RM_c`) a 1,72 (`CHAS`). Com `cidade`, a razão vai de 0,44 (`CRIM`) a 2,25 (`logLSTAT`) |

**O que os resultados permitem concluir.**

- A ligação está correta: os valores coincidem em todas as variáveis e linhas, exceto um valor de `CRIM`. As coordenadas da fonte podem ser usadas com as linhas do projeto.
- Os resíduos do modelo final **têm correlação espacial** entre setores vizinhos, com as duas matrizes. A Seção 8.4 ([Seção 16](08-modelo-final.md)) tinha mostrado a dependência dentro da cidade; esta parte mostra a dependência entre vizinhos, que os erros agrupados não tratam.
- A dependência tem a forma de **erro espacial**: os testes LM robustos, o AIC e os resíduos dos dois modelos apontam para o SEM. O SAR deixa correlação nos resíduos. A explicação é um fator do lugar que não está no modelo, e não um efeito do preço dos vizinhos.
- As conclusões sobre `RM`, `LSTAT`, `CRIM`, `NOX`, `PTRATIO` e `B` **resistem**: os sinais e a significância se mantêm, e os coeficientes mudam no máximo 2,1 erros padrão HC3. `RM` quase não muda.
- As conclusões sobre `CHAS` e `DIS` **não resistem**: no SEM, os dois deixam de ser significativos a 5%, e `CHAS` muda 3,1 erros padrão. No MQO, parte do efeito de estar perto do rio Charles e da distância aos centros de emprego vinha de outros fatores do lugar. Esses efeitos devem ser apresentados como associações que dependem da localização.
- Os erros padrão agrupados, por `TOWN` ou por `cidade`, mantêm todos os termos significativos e por isso **subestimam** a incerteza de `CHAS` e `DIS`.
- Limitações: os resultados dependem da matriz $W$ (as duas matrizes dão a mesma conclusão qualitativa, mas $\hat\lambda$ muda de 0,77 para 0,87); o SEM por ML supõe erros normais e homocedásticos (o GMM heterocedástico não supõe, e dá as mesmas conclusões); o SEM foi ajustado em `df_final` (sem as 28 linhas influentes) e não foi avaliado na validação cruzada, porque a previsão espacial fora da amostra precisa dos resíduos dos vizinhos. O `modelo_final` continua sendo o MQO; o SEM fica como referência para a inferência sobre `CHAS` e `DIS`.
