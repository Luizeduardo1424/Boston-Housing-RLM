# Tarefa 07: o que falta para cumprir os pressupostos da RLM

## Contexto

O `README.md` da raiz define o que o projeto precisa entregar:

- **Pressupostos** (Metodologia, item 5): linearidade, independência dos erros, homocedasticidade, normalidade dos resíduos e ausência de multicolinearidade severa.
- **Diagnóstico** (item 7): resíduos, pontos influentes, observações discrepantes, alavanca, distância de Cook e VIF.
- **Objetivos específicos**: significância dos coeficientes, qualidade do ajuste, interpretação e capacidade preditiva.

As Partes 5 a 13 trataram esses pontos um por vez, e a situação está espalhada em várias seções. A [Seção 15](../pressupostos/07-pendencias.md) lista o que ainda não foi verificado, mas não diz se o projeto já cumpre o que o `README.md` promete. Esta tarefa junta tudo em um quadro e decide o que falta fazer para fechar o projeto.

Esta tarefa é de análise e documentação. Ela só acrescenta células ao notebook se um teste estiver faltando (passo 2).

## Estado atual (resumo, confira os números nas seções citadas)

| Pressuposto | Evidência atual | Onde |
|---|---|---|
| Linearidade e forma funcional | RESET p = 0,94 no modelo final | [Seção 16.1](../pressupostos/08-modelo-final.md) |
| Independência | DW 1,41 pela ordem do arquivo; I de Moran 0,32 (p = 0,001); o modelo de erro espacial (SEM) remove a correlação | [Seção 19](../pressupostos/11-correlacao-espacial.md) |
| Homocedasticidade | Breusch-Pagan p ≈ 10⁻¹¹; HC3 na inferência; MQGF reduz, mas resta BP p ≈ 10⁻⁶ e cobertura de 91% nas casas baratas | [Seção 17](../pressupostos/09-heterocedasticidade.md) |
| Normalidade | correlação QQ 0,993; Shapiro-Wilk p = 0,001; curtose 1,3 | [Seção 16.1](../pressupostos/08-modelo-final.md) |
| Multicolinearidade | VIF máximo 4,8 (`NOX`); `TAX` fora | [Seção 16.1](../pressupostos/08-modelo-final.md), [Tarefa 06](06-colinearidade-nox-dis.md) |
| Influentes | 28 linhas removidas na estimação; a previsão usa todas as linhas | [Seção 16](../pressupostos/08-modelo-final.md) |
| Censura em 50 | Tobit: mesmas conclusões, atenuação de 12% a 14% em `RM` | [Seção 18](../pressupostos/10-tobit.md) |

## O que fazer

1. **Quadro de checagem.** Para cada pressuposto e cada item de diagnóstico do `README.md`, uma linha com: teste usado, valor atual, seção de origem e situação:
   - **cumprido**: o teste não rejeita, ou o desvio é pequeno e justificado;
   - **tratado**: o pressuposto falha, mas há correção (HC3, MQGF, SEM, Tobit) e as conclusões não mudam;
   - **em aberto**: falha sem correção, ou a correção não foi avaliada.
   Inclua dois pressupostos que o `README.md` não cita: exogeneidade (variáveis omitidas) e especificação da resposta (log).
2. **Itens em aberto.** Para cada item "em aberto", descreva o que falta e estime o esforço. Itens conhecidos:
   - heterocedasticidade residual depois do MQGF e cobertura baixa nas casas baratas;
   - SEM não avaliado na validação cruzada; resultado depende da matriz de vizinhança (teste também k = 4 e k = 8);
   - Shapiro-Wilk ainda rejeita: avalie se importa com n = 473 (TCL, tamanho do desvio no QQ) ou se pede bootstrap dos IC;
   - Tobit com variância constante, que é rejeitada;
   - não há conjunto de teste separado, só validação cruzada.
   Se um item puder ser fechado com uma célula curta (por exemplo, bootstrap dos IC do modelo final, ou SEM na validação cruzada), faça isso em uma nova parte do notebook.
3. **Objetivos específicos.** Confira um a um os objetivos do `README.md` (linhas 21 a 33) e indique a célula ou seção que cumpre cada um. Liste os que não estão cumpridos.
4. **Modelo de entrega.** Decida qual modelo é o principal do trabalho (MQO com HC3, MQGF, Tobit ou SEM) e como os outros entram, como análise de robustez. Justifique pela lista de pressupostos e pela validação cruzada. Use também o resultado da [Tarefa 08](08-comparacao-modelos.md), se ela já estiver feita.
5. **Texto final.** Reescreva as seções "Resultados" e "Limitações" do `README.md` da raiz para refletir o quadro.

## Critério de pronto

- Quadro "pressuposto → evidência → situação" completo, sem lacunas.
- Lista curta de pendências que ainda ficam abertas, com a razão de cada uma.
- `README.md` da raiz coerente com o quadro e com a [Seção 15](../pressupostos/07-pendencias.md).

Faça esta tarefa **depois** das Tarefas 06 e 08, porque ela usa os resultados delas.

## Documentação a atualizar

- Novo `docs/pressupostos/NN-checagem-pressupostos.md` com o próximo número livre.
- `07-pendencias.md`: atualize todas as linhas que mudarem.
- `README.md` (raiz): "Resultados" e "Limitações".

## Referências

- Fox, J. (2016). *Applied Regression Analysis and Generalized Linear Models*. 3. ed. Sage (capítulos 11 a 13: diagnóstico).
- Montgomery, D. C.; Peck, E. A.; Vining, G. G. (2012). *Introduction to Linear Regression Analysis*. 5. ed. Wiley (capítulo 4: adequação do modelo).
