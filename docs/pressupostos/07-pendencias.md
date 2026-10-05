## 15. O que ainda não foi verificado

| Pressuposto ou cuidado | Situação |
|---|---|
| Erros padrão robustos (HC3) | aplicados **só ao modelo E** da Parte 7 ([Seção 14](06-transformacoes.md)). As Partes 5 e 6 continuam com `cov_type='nonrobust'` |
| Independência espacial | rejeitada pela ordem do arquivo em todos os modelos (DW entre 0,95 e 1,27). Nenhuma transformação nem o HC3 corrigem. Sem coordenadas, não há I de Moran, erros padrão agrupados ou modelo espacial. Registrada como **limitação** ([Seção 14.1](06-transformacoes.md)) |
| Censura em 50 | tratada apenas parcialmente (remoção, para verificação). Sem modelo Tobit |
| Diagnóstico do modelo da Parte 6 | gráfico QQ, Shapiro-Wilk, Breusch-Pagan e Durbin-Watson feitos na Parte 7 (modelos D e E). Ainda faltam as medidas de influência (alavanca, Cook, DFFITS) |
| Modelo final | forma funcional definida na Parte 7 (modelo E com HC3). Falta combinar com a remoção S+I da Parte 5 |
| Capacidade preditiva | não avaliada: não há divisão treino/teste nem validação cruzada |
