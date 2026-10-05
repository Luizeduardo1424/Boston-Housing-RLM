# Tarefa 05: testar a indicadora `ZN > 0`

## Contexto

`ZN` é a proporção de terrenos residenciais com lotes grandes. A maioria dos setores tem `ZN = 0`, e os outros têm valores espalhados. Uma variável assim costuma funcionar melhor como indicadora (há ou não há zoneamento para lotes grandes) do que como variável contínua. A Parte 7 sugeriu a indicadora `ZN > 0`, mas ela não foi testada.

Na Parte 8, `ZN` saiu do modelo junto com `INDUS` e `AGE` (Wald conjunto com HC3: χ² = 0,32, p = 0,96). Esse teste usou `ZN` contínua, então não diz nada sobre a indicadora.

## Estado atual

- `formula_final` (célula 116) não tem `ZN`.
- Validação cruzada do modelo final: RMSE 4,00, MAE 2,75, R² 0,79.
- `ZN` faz parte da chave dos grupos `cidade` (célula 122). Isso não muda: os grupos continuam usando `ZN` original.

## O que fazer

1. **Descrever.** Conte quantas linhas de `df_t` e de `df_final` têm `ZN > 0`. Compare a mediana de `MEDV` nos dois grupos (Mann-Whitney, como na Parte 3). Se um dos grupos tiver poucas linhas (menos de 30), registre que o teste tem pouco poder.
2. **Fórmula.** `formula_zn = formula_final + " + C(ZN > 0)"`. O patsy aceita a expressão dentro de `C()`. O coeficiente aparece como `C(ZN > 0)[T.True]`.
3. **Ajuste e teste.** Em `df_final`, com `cov_type="HC3"`. Wald com HC3 para o termo. AIC e BIC com o ajuste MQO não robusto, comparados com o modelo final. Confira, como na Tarefa 04, se as linhas influentes mudam.
4. **Colinearidade.** `ZN > 0` é ligada a `INDUS`, `NOX` e `DIS` (subúrbios com lotes grandes têm pouca indústria). Calcule o VIF da indicadora e veja se os coeficientes de `NOX` e `logDIS` mudam muito.
5. **Efeito.** $100 \cdot (e^{\beta} - 1)$: diferença percentual em `MEDV` entre setores com e sem lotes grandes, com o resto fixo. Use o IC 95% com HC3.
6. **Validação cruzada.** A mesma da célula 126, com as mesmas partes, comparando com o modelo final.

## Critério de pronto

- Mantenha a indicadora **só se** o Wald com HC3 der p < 0,05 **e** o RMSE da validação cruzada for menor que 4,00. Caso contrário, registre o resultado e não mude o modelo final.
- Tabela com o efeito, o IC 95% e o p-valor, e a tabela de validação cruzada.

Esta tarefa pode ser feita junto com a [Tarefa 04](04-interacao-rm-lstat.md), na mesma parte do notebook. Nesse caso, teste também as duas mudanças juntas.

## Documentação a atualizar

- Novo `docs/pressupostos/NN-interacoes.md` (o mesmo arquivo da Tarefa 04, se feitas juntas), ou `NN-indicadora-zn.md`.
- `07-pendencias.md`: linha "Interações".
- `README.md` (raiz), se o modelo final mudar.

## Referências

- Harrison, D.; Rubinfeld, D. L. (1978). Hedonic housing prices and the demand for clean air. *Journal of Environmental Economics and Management*, 5(1), 81–102 (definição de `ZN`).
