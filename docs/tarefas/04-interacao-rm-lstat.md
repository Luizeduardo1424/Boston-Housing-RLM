# Tarefa 04: testar a interação `RM × logLSTAT`

## Contexto

No modelo final, o efeito de um cômodo a mais (`RM`) depende só do próprio `RM` (termo quadrático). Mas um cômodo a mais pode valer menos numa região com muita população de baixa renda (`LSTAT` alto). A interação `RM_c:logLSTAT_c` testa essa ideia. Nenhuma interação foi testada no projeto.

## Estado atual

- `formula_final` (célula 116) não tem interações.
- Efeito de +1 cômodo na casa média (Seção 16): −5,8% com 5 cômodos, +7,9% com 6, +23,6% com 7, +41,7% com 8.
- Validação cruzada do modelo final: RMSE 4,00, MAE 2,75, R² 0,79.
- `RM_c` e `logLSTAT_c` já estão centralizados na média de `df_t`. Com variáveis centralizadas, os coeficientes principais continuam sendo os efeitos no ponto médio, e a colinearidade com a interação fica baixa.

## O que fazer

1. **Fórmula.** `formula_interacao = formula_final + " + RM_c:logLSTAT_c"`.
2. **Ajuste.** Use os mesmos dados do modelo final: `df_final` (n = 473), com `cov_type="HC3"`. Para ser justo, confira também se as linhas influentes mudam com a nova fórmula (`linhas_influentes` sobre o ajuste em `df_t`). Se mudarem muito, registre.
3. **Teste.** Wald com HC3 para `RM_c:logLSTAT_c = 0` (`m.wald_test("RM_c:logLSTAT_c = 0", scalar=True)`). Compare AIC e BIC com o modelo final (mesma resposta e mesmas linhas, ajuste MQO não robusto).
4. **VIF.** Calcule o VIF da interação com `variance_inflation_factor`, como na célula 118.
5. **Interpretação.** Calcule o efeito de +1 cômodo para combinações de `RM` (6, 7 e 8) e `LSTAT` nos quartis 25%, 50% e 75% de `df_t`:
   $100 \cdot \big(e^{\beta_{RM} + 2\beta_{RM^2}(RM - \overline{RM}) + \beta_{int}\,(\log LSTAT - \overline{\log LSTAT})} - 1\big)$.
   É a mesma fórmula da Seção 16, com o termo da interação. Mostre como tabela. Se possível, um gráfico com uma curva por quartil de `LSTAT`, salvo em `results/figures/`.
6. **Validação cruzada.** Repita a célula 126 com as mesmas partes (`KFold(10, shuffle=True, random_state=42)` em `df_t`), com o modelo final e o modelo com a interação, ambos com todas as linhas no treino e `prever_log`.
7. **Resíduos.** Rode `resumir_residuos` no novo modelo e compare RESET e Breusch-Pagan com o modelo final.

## Critério de pronto

- Mantenha a interação no modelo final **só se** o Wald com HC3 der p < 0,05 **e** o RMSE da validação cruzada for menor que 4,00. Se só uma das condições valer, registre e não mude o modelo final.
- Tabela de efeitos (passo 5) e tabela de validação cruzada (passo 6).
- Se a interação entrar no modelo, refaça as tabelas da Parte 8 que dependem da fórmula, numa nova parte do notebook, e atualize o `README.md` da raiz.

Esta tarefa pode ser feita junto com a [Tarefa 05](05-indicadora-zn.md), na mesma parte do notebook. Nesse caso, teste também as duas mudanças juntas.

## Documentação a atualizar

- Novo `docs/pressupostos/NN-interacoes.md` (o mesmo arquivo da Tarefa 05, se feitas juntas).
- `07-pendencias.md`: linha "Interações".

## Referências

- Aiken, L. S.; West, S. G. (1991). *Multiple Regression: Testing and Interpreting Interactions*. Sage.
- [`TERMOS_NAO_LINEARES.md`](../../TERMOS_NAO_LINEARES.md), sobre termos quadráticos centralizados.
