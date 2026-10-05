## 15. O que ainda não foi verificado

| Pressuposto ou cuidado | Situação |
|---|---|
| Erros padrão robustos (HC3) | aplicados ao modelo E da Parte 7 ([Seção 14](06-transformacoes.md)) e ao modelo final da Parte 8 ([Seção 16](08-modelo-final.md)). As Partes 5 e 6 continuam com `cov_type='nonrobust'`. Na Parte 9 ([Seção 17](09-heterocedasticidade.md)), a variância foi **modelada** por MQGF (pesos por `logLSTAT`): coeficientes próximos aos do MQO, RMSE de validação cruzada 3,89 (contra 4,00) e cobertura de 95,4% dos intervalos de previsão. Resta heterocedasticidade residual (Breusch-Pagan p ≈ 10⁻⁶) e cobertura de 91% nas casas mais baratas |
| Independência espacial | rejeitada pela ordem do arquivo em todos os modelos (DW entre 0,95 e 1,41). A Parte 8 mostra que a dependência vem da ordem das linhas (DW ≈ 2 com os resíduos em ordem aleatória) e que as conclusões resistem a erros padrão agrupados por cidade aproximada. A correlação **entre** cidades vizinhas não foi verificada: sem coordenadas, não há I de Moran nem modelo espacial. Registrada como **limitação** ([Seção 14.1](06-transformacoes.md)) |
| Censura em 50 | tratada pelo modelo Tobit na Parte 10 ([Seção 18](10-tobit.md)): coeficientes a menos de 0,5 erro padrão HC3 do MQO (o efeito de `RM` no MQO está atenuado em 12% a 14%), mesmas conclusões do modelo final e RMSE de validação cruzada 3,83 (contra 4,00). A remoção das linhas censuradas (Parte 6) muda mais e na direção errada. Restam os pressupostos do Tobit: erros normais e variância constante (rejeitada; o Tobit heterocedástico muda os coeficientes em até 0,87 erro padrão) |
| Modelo final | ajustado na Parte 8 ([Seção 16](08-modelo-final.md)): modelo E sem `ZN`, `INDUS` e `AGE`, sem as 28 linhas influentes, com HC3 |
| Capacidade preditiva | avaliada por validação cruzada com 10 partes na Parte 8 ([Seção 16](08-modelo-final.md)). Não há conjunto de teste separado |
| Interações | não testadas (por exemplo, `RM × logLSTAT`), nem a indicadora `ZN > 0` sugerida na Parte 7 |

As tarefas para fechar estas pendências estão descritas, uma por arquivo, em [`docs/tarefas/`](../tarefas/README.md).
