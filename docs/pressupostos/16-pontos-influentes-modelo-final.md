## 24. Pontos que pioram o modelo final (Parte 12, células 168–174)

| Aspecto | Código | Pressuposto ou detalhe |
|---|---|---|
| Dados | `df_final`, `modelo_final_classico` (célula 118) | modelo final já sem as 28 influentes (n = 473), ajuste clássico. O modelo final não muda: é uma análise de sensibilidade |
| Medidas por linha | `get_influence()` (célula 170) | resíduo studentizado externo, alavanca $h_{ii}$ (média p/n = 0,040; limite usual 2p/n = 0,080), distância de Cook e DFFITS |
| Linhas mostradas | `motivos` (célula 170) | as 2 com menor valor ajustado (ponta esquerda da escala-locação), $\lvert t\rvert > 3$, outlier de Bonferroni (`outlier_test(method="bonf")`, p < 0,05) e as 5 maiores distâncias de Cook |
| 2ª rodada | `linhas_influentes(modelo_final_classico)` (célula 170) | os critérios da Parte 8 (Cook > 4/n ou \|DFFITS\| > 2·√(p/n)) aplicados de novo. O corte 4/n é relativo, então cada rodada marca novas linhas |
| Escala-locação | célula 171 | $\sqrt{\lvert r_i\rvert}$ (resíduo studentizado interno) contra o valor ajustado, com LOWESS (`frac=2/3`, [Seção 4](02-eda.md)), com e sem a linha de menor valor ajustado; eixos iguais. A inclinação vem de MQO de $\sqrt{\lvert r_i\rvert}$ no valor ajustado. Figura `results/figures/escala_locacao_sem_extremo.html` |
| Reajuste | `cenarios_16` (célula 173) | sem a linha 414, sem as linhas com $\lvert t\rvert > 3$, sem a 2ª rodada. Mudança dos coeficientes medida em erros padrão HC3 do modelo final |
| Validação cruzada | `regras_16` (célula 173) | as 10 partes da célula 126 (`KFold`, semente 42). Em cada rodada: influentes da 1ª rodada saem do treino, depois a regra do cenário é aplicada ao treino. O teste mantém todas as linhas. Previsão com `prever_log` (smearing de Duan). A referência é "Final (sem influentes no treino)" (RMSE 4,072), não o ajuste com todas as linhas (3,996) |
| Saída | célula 173 | `results/tables/sensibilidade_pontos_modelo_final.csv` |

### 24.1 Resultados

| Etapa | Resultado |
|---|---|
| Linha da ponta esquerda | **414**: `MEDV` = 7,0, `CRIM` = 45,7, `RM` = 4,5, `LSTAT` = 37%, `RAD` = 24. Maior alavanca (0,21) e maior Cook (0,063). Ajustado 5,5 mil dólares, t = 2,1: variáveis extremas, erro moderado |
| Outras linhas | 385, 391, 397 (Bonferroni, t = −4,7), 407 e 413 com $\lvert t\rvert > 3$; 404 e 427 com alavanca alta; 161 (`MEDV = 50`). 8 das 9 têm `RAD = 24` (Boston). A 2ª rodada marca 23 linhas, 65% com `RAD = 24` |
| Escala-locação | sem a 414, a curva continua alta na esquerda; inclinação −0,24 nos dois casos; Breusch-Pagan rejeita nos dois. A subida é heterocedasticidade real nas casas baratas ([Seção 17](09-heterocedasticidade.md)), não efeito de um ponto |
| Sem a 414 | RMSE (VC) 4,062 contra 4,072; maior mudança 0,5 EP (`CRIM`) |
| Sem $\lvert t\rvert > 3$ (5 linhas) | Shapiro-Wilk p = 0,21, correlação QQ 0,998; RMSE (VC) 4,090 |
| Sem a 2ª rodada (23 linhas) | R² ajustado 0,903, Shapiro-Wilk p = 0,48; RMSE (VC) 4,180; `CRIM` muda 1,7 EP |
| Decisão | nenhuma linha a mais sai do modelo final. As remoções melhoram o ajuste e a normalidade dentro da amostra, mas não a previsão |

O que o resultado **não** permite concluir: que essas linhas são erros de registro. Os valores são plausíveis para a região central de Boston, e a concentração em `RAD = 24` é coerente com a dependência espacial da [Seção 19](11-correlacao-espacial.md).
