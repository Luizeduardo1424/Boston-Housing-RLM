# Tarefa 06: colinearidade entre `NOX` e `logDIS`

## Contexto

O par de preditores mais correlacionado da EDA era `TAX` e `RAD`: `TAX = 666` em todas as linhas com `RAD = 24`, e o GVIF de `TAX` era cerca de 9,9 ([Seção 7](../pressupostos/02-eda.md) e [Seção 9](../pressupostos/02-eda.md)). Por isso `TAX` saiu da base da Parte 6 e não está no modelo final.

Entre os preditores que **continuam** no modelo final, o par mais correlacionado é `NOX` e `logDIS` (Pearson 0,83 nos dados sem as linhas suspeitas). Setores longe dos centros de emprego têm ar mais limpo, então as duas variáveis medem em parte a mesma coisa. `NOX` tem o maior VIF do modelo final (4,8, [Seção 16.1](../pressupostos/08-modelo-final.md)). O segundo par é `RM` e `logLSTAT` (−0,69 em `df_final`, [Seção 20](../pressupostos/12-interacoes.md)).

A colinearidade não causa viés, mas aumenta os erros padrão e deixa os coeficientes instáveis. Há um sinal disso: no modelo de erro espacial da Parte 11, `logDIS` deixa de ser significativo (p = 0,072, [Seção 19](../pressupostos/11-correlacao-espacial.md)).

A pergunta da tarefa: o modelo fica melhor sem uma das duas variáveis (ou sem as duas)? Ou há um jeito de reduzir a correlação e manter as duas?

## Estado atual

- `formula_final` (célula 116) tem `NOX` e `logDIS`. Os dois são significativos com HC3 no modelo final.
- VIF do modelo final: célula 118, sem as indicadoras de `RAD`.
- GVIF e número de condição: funções `calcular_vif` e `calcular_numero_condicao` (célula 4).
- Validação cruzada do modelo final: RMSE 4,00, MAE 2,75, R² 0,79 (célula 126).

## O que fazer

1. **Diagnóstico.** Em `df_final`: matriz de correlação dos termos do modelo final, VIF de cada termo, GVIF do bloco `C(RAD)` e número de condição. Confirme que `NOX` e `logDIS` são o par principal. Calcule também a correlação de `NOX` e `logDIS` com `INDUS` e `AGE` (que saíram na Parte 8), porque elas formam o mesmo grupo.
2. **Retirar as variáveis.** Ajuste três variantes de `formula_final` em `df_final` com `cov_type="HC3"`: sem `NOX`, sem `logDIS` e sem as duas. Para cada uma, compare com o modelo final:
   - coeficientes que mudam mais de 1 erro padrão HC3 (sinal de viés de variável omitida);
   - R² ajustado, AIC e BIC (ajuste MQO não robusto);
   - `resumir_residuos` (célula 118): RESET, Shapiro-Wilk, Breusch-Pagan, DW;
   - validação cruzada da célula 126, com as mesmas partes.
3. **Reduzir a correlação e manter as duas.** Teste estas opções e registre o efeito de cada uma:
   - **Residualização.** Troque `logDIS` pelo resíduo de `logDIS ~ NOX` (ou o inverso). Os dois termos ficam sem correlação. O ajuste, os resíduos e as previsões **não mudam**; só muda a interpretação do coeficiente (o efeito de `NOX` passa a incluir a parte comum). Explique isso no texto.
   - **Índice combinado.** Primeira componente principal de `NOX` e `logDIS` padronizados (com `INDUS` e `AGE` como opção). Um termo no lugar de dois. Registre a variância explicada pela componente e os pesos.
   - **Ridge.** `sklearn.linear_model.RidgeCV` com os preditores padronizados, como referência de previsão. Não dá erros padrão, então não substitui o MQO na inferência.
   - Deixe claro que **centralizar ou padronizar não reduz** a correlação entre dois termos lineares. A centralização só ajuda entre `x` e `x²` ([Seção 13](../pressupostos/05-termo-quadratico-rm.md)).
4. **Reconfirmar `TAX` e `RAD`.** Teste duas variantes com `TAX` de volta: (a) `TAX` com a indicadora `RAD = 24` no lugar do bloco `C(RAD)`; (b) `TAX` só para `RAD ≠ 24` (interação `TAX:C(RAD == 24)`). GVIF e validação cruzada. O objetivo é registrar se a decisão de tirar `TAX` continua certa.
5. **`RM_c` e `logLSTAT_c`.** Repita, de forma breve, os passos 2 e 3 para este par. Atenção: os dois têm termo quadrático, então retire o termo linear e o quadrado juntos.

## Critério de pronto

- Tabela com uma linha por variante: VIF máximo, número de condição, R² ajustado, BIC, p-valores do RESET e do Breusch-Pagan, RMSE, MAE e R² da validação cruzada.
- Mude o modelo final **só se** a variante tiver RMSE menor que 4,00 na validação cruzada **e** nenhum pressuposto piorar (RESET, normalidade, VIF). Caso contrário, registre o resultado e mantenha o modelo final.
- Conclusão em texto: a colinearidade de `NOX` e `logDIS` é um problema para a inferência ou não?

## Documentação a atualizar

- Novo `docs/pressupostos/NN-colinearidade.md` com o próximo número livre.
- `07-pendencias.md`: nova linha "Multicolinearidade".
- `README.md` (raiz), seções "Resultados" e "Limitações", se o modelo final mudar.

## Referências

- Belsley, D. A.; Kuh, E.; Welsch, R. E. (1980). *Regression Diagnostics*. Wiley.
- Fox, J.; Monette, G. (1992). Generalized collinearity diagnostics. *Journal of the American Statistical Association*, 87(417), 178–183.
- Hoerl, A. E.; Kennard, R. W. (1970). Ridge regression: biased estimation for nonorthogonal problems. *Technometrics*, 12(1), 55–67.
