# CLAUDE.md

Projeto acadêmico de regressão linear múltipla (Boston Housing). A análise está em dois notebooks: `notebooks/01-AED.ipynb` (análise exploratória, Partes 1 a 4) e `notebooks/02-MRLM.ipynb` (modelo de regressão linear múltipla, Partes 5 a 12). As funções de gráfico ficam em `notebooks/graficos.py`. Língua do projeto: português.

## Documentação da análise estatística

A pasta `docs/pressupostos/` descreve o que foi feito na análise: para cada etapa do notebook, a função usada, os parâmetros aplicados, os pressupostos e o que o resultado permite concluir.

- **Atualizar a cada commit.** Todo commit que muda a análise (notebook, modelo, testes, figuras ou tabelas em `results/`) deve atualizar, no mesmo commit, o arquivo correspondente em `docs/pressupostos/` e o índice em `docs/pressupostos/README.md`. Um commit que não muda a análise não precisa atualizar a documentação.
- **Limite de tamanho.** Cada arquivo da pasta deve ter no máximo ~250 linhas ou ~20 KB. Se um arquivo passar do limite, divida-o por seção em novos arquivos numerados e atualize o índice.
- **Nova parte do notebook = novo arquivo.** Crie `NN-assunto.md` com o próximo número livre, em vez de aumentar um arquivo existente. As pendências ficam em `07-pendencias.md` e as referências em `referencias.md`.
- **Números de seção estáveis.** Não renumere seções existentes. Para citar uma seção de outro arquivo, use um link: `[Seção 11.6](03-modelo-completo-residuos.md)`. Cite os índices das células do notebook (contados a partir de 0).
- **Leitura econômica.** Leia primeiro `docs/pressupostos/README.md` (índice) e depois só o arquivo da seção necessária, não a pasta inteira.

`TERMOS_NAO_LINEARES.md` é um texto explicativo à parte e não segue a regra acima.

## Fluxo de trabalho

- Atualize `main`, crie a branch a partir dela e abra o PR para `main`.
