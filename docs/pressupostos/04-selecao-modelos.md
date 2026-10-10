## 12. Análise de sensibilidade e seleção de modelos (células 24–33)

Células do notebook [`02-MRLM.ipynb`](../../notebooks/02-MRLM.ipynb).

### 12.1 Sensibilidade sem as linhas suspeitas (célula 25)

O modelo é reajustado sem os índices 506–510 (n = 501). A função `resumir` usa o resíduo **bruto** no Shapiro-Wilk, o interno na faixa 2–3 e o externo em $\lvert t \rvert > 3$. O corte de alavanca usa o mesmo p e o n de cada modelo.

### 12.2 Seleção entre 16 combinações de remoção (células 29–33)

| Aspecto | Detalhe |
|---|---|
| Grupos | S (506–510), O ($\lvert t \rvert > 3$), L ($h > 2p/n$), I (Cook $> 4/n$ ou $\lvert DFFITS \rvert > 2\sqrt{p/n}$), marcados **uma única vez** no modelo completo (sem iterar) |
| Métricas (`avaliar`) | correlação QQ e Shapiro-Wilk com o resíduo **externo**; faixa 2–3 e binomial com o **interno**; Bonferroni (externo); Breusch-Pagan, RESET e Durbin-Watson com o **bruto**; significância pela ANOVA tipo II |
| Nota final | média de três postos com **pesos iguais** (R² ajustado, resíduos, significância). Os pesos e a composição do posto de resíduos são escolhas do trabalho, e não um critério estatístico padrão |
| Limite | candidatos que removem mais de 10% de n saem da escolha (nenhum saiu: máximo de 8,7%) |

Pressupostos e limitações:

- **Inferência após seleção.** As linhas foram removidas **com base nos próprios resíduos** do modelo. Por isso, os p-valores, os erros padrão, o F e o R² dos modelos reduzidos são **otimistas**: não levam em conta que a amostra foi escolhida para se ajustar bem. Isso vale principalmente para os grupos O e I.
- **R² de amostras diferentes.** Retirar linhas com resíduo grande sempre aumenta o R², e os R² de amostras diferentes não são estritamente comparáveis (o notebook já registra esse cuidado).
- **Validade externa.** Com exceção de 506–510, as linhas removidas são regiões reais. O modelo S+I descreve as regiões "típicas" e não deve ser usado para prever as regiões removidas.
- Os testes de cada candidato continuam usando a covariância **não robusta** ([Seção 10.2](03-modelo-completo-residuos.md)).
