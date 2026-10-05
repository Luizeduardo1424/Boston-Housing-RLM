# Regressão Linear Múltipla — Boston Housing Dataset

## 📌 Sobre o projeto

Este repositório contém o desenvolvimento de um trabalho acadêmico sobre **Regressão Linear Múltipla (RLM)**, utilizando o conjunto de dados **Real Estate Dataset**, disponibilizado no Kaggle.

O objetivo do trabalho é estudar a relação entre diferentes características socioeconômicas e estruturais dos municípios/regiões de Boston e o **valor mediano das residências**, utilizando um modelo de regressão linear múltipla.

> **Dataset:** [Real Estate Dataset — Kaggle](https://www.kaggle.com/datasets/arslanali4343/real-estate-dataset)

O conjunto de dados possui **511 observações e 14 variáveis**, sendo 13 variáveis explicativas e uma variável resposta (`MEDV`).

---

## 🎯 Objetivos

### Objetivo geral

Construir e analisar um modelo de **Regressão Linear Múltipla** capaz de explicar a variação do valor mediano das residências a partir de características relacionadas às regiões analisadas.

### Objetivos específicos

* Realizar uma análise exploratória dos dados;
* Identificar possíveis valores ausentes e inconsistências;
* Analisar a distribuição das variáveis;
* Investigar a relação entre as variáveis explicativas e a variável resposta;
* Construir um modelo de Regressão Linear Múltipla;
* Verificar os pressupostos do modelo;
* Avaliar a significância dos coeficientes;
* Analisar possíveis problemas de multicolinearidade;
* Avaliar a qualidade do ajuste do modelo;
* Interpretar os resultados estatísticos;
* Avaliar a capacidade preditiva do modelo.

---

## 📊 Sobre o Dataset

O dataset utilizado é baseado no conhecido **Boston Housing Dataset**, originalmente relacionado ao estudo de preços de imóveis na região de Boston.

O conjunto possui as seguintes variáveis:

| Variável  | Descrição em inglês                                              | Descrição em português                                                             |
| --------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `CRIM`    | Per capita crime rate by town                                    | Taxa de criminalidade por habitante na região                                      |
| `ZN`      | Proportion of residential land zoned for lots over 25,000 sq.ft. | Proporção de terrenos residenciais destinados a lotes com mais de 25.000 pés²      |
| `INDUS`   | Proportion of non-retail business acres per town                 | Proporção de acres destinados a atividades comerciais não varejistas               |
| `CHAS`    | Charles River dummy variable                                     | Variável indicadora que informa se a região faz limite com o rio Charles           |
| `NOX`     | Nitric oxides concentration                                      | Concentração de óxidos de nitrogênio                                               |
| `RM`      | Average number of rooms per dwelling                             | Número médio de cômodos por residência                                             |
| `AGE`     | Proportion of owner-occupied units built prior to 1940           | Proporção de residências ocupadas pelos proprietários construídas antes de 1940    |
| `DIS`     | Weighted distances to five Boston employment centres             | Distância ponderada até cinco centros de emprego de Boston                         |
| `RAD`     | Index of accessibility to radial highways                        | Índice de acessibilidade às rodovias radiais                                       |
| `TAX`     | Full-value property-tax rate per $10,000                         | Taxa de imposto sobre propriedades por US$ 10.000                                  |
| `PTRATIO` | Pupil-teacher ratio by town                                      | Relação entre número de alunos e professores na região                             |
| `B`       | 1000(Bk - 0.63)²                                                 | Transformação baseada na proporção populacional representada por `Bk`              |
| `LSTAT`   | Percentage of lower status population                            | Percentual da população classificada na categoria socioeconômica inferior          |
| `MEDV`    | Median value of owner-occupied homes in $1000s                   | Valor mediano das residências ocupadas pelos proprietários, em milhares de dólares |

As definições das variáveis são baseadas na documentação do conjunto Boston Housing e em descrições do próprio dataset utilizado no Kaggle.

---

## 🎯 Variável resposta

A variável escolhida como resposta do modelo é:

### `MEDV`

**Median value of owner-occupied homes in $1000s**

Representa o **valor mediano das residências ocupadas pelos proprietários**, expresso em milhares de dólares.

Assim, o objetivo do modelo será explicar/predizer `MEDV` a partir das demais variáveis disponíveis.

De forma geral:

$$
MEDV = \beta_0 + \beta_1CRIM + \beta_2ZN + \beta_3INDUS + \cdots + \beta_{13}LSTAT + \varepsilon
$$

onde:

* $\beta_0$ representa o intercepto;
* $\beta_i$ representa o efeito associado a cada variável explicativa;
* $\varepsilon$ representa o erro aleatório.

---

## 🔎 Variáveis explicativas

As variáveis utilizadas inicialmente como explicativas são:

```text
CRIM
ZN
INDUS
CHAS
NOX
RM
AGE
DIS
RAD
TAX
PTRATIO
B
LSTAT
```

A variável `MEDV` será utilizada como variável dependente.

---

## 🧪 Metodologia

O desenvolvimento do trabalho foi dividido nas seguintes etapas:

### 1. Análise exploratória dos dados

* Importação do dataset;
* Verificação das dimensões;
* Identificação dos tipos das variáveis;
* Estatísticas descritivas;
* Identificação de valores ausentes;
* Análise de possíveis outliers;
* Visualizações gráficas.

### 2. Análise das variáveis

Serão investigadas as relações entre as variáveis explicativas e `MEDV`, utilizando, entre outras ferramentas:

* Histogramas;
* Boxplots;
* Gráficos de dispersão;
* Matriz de correlação;
* Heatmap de correlações.

### 3. Construção do modelo

Será ajustado inicialmente um modelo de **Regressão Linear Múltipla** utilizando `MEDV` como variável resposta.

O modelo geral será:

$$
Y = X\beta + \varepsilon
$$

ou, especificamente:

$$
MEDV = \beta_0 + \beta_1CRIM + \beta_2ZN + \cdots + \beta_{13}LSTAT + \varepsilon
$$

### 4. Testes de hipóteses

Serão analisados os testes relacionados aos parâmetros do modelo, incluindo:

* Testes individuais dos coeficientes;
* Teste global de significância da regressão;
* Intervalos de confiança;
* Testes relacionados aos pressupostos do modelo.

### 5. Verificação dos pressupostos

Serão avaliados os principais pressupostos da Regressão Linear Múltipla:

* **Linearidade**;
* **Independência dos erros**;
* **Homoscedasticidade**;
* **Normalidade dos resíduos**;
* **Ausência de multicolinearidade severa**.

### 6. Avaliação do modelo

Serão utilizados indicadores como:

* $R^2$;
* $R^2$ ajustado;
* Erro padrão residual;
* Soma dos quadrados dos resíduos;
* Estatística F;
* p-valores;
* RMSE, quando aplicável.

### 7. Diagnóstico do modelo

Também serão investigados:

* Resíduos;
* Pontos influentes;
* Observações discrepantes;
* Leverage;
* Distância de Cook;
* Multicolinearidade através do **VIF (Variance Inflation Factor)**.

---

## 🛠️ Tecnologias utilizadas

O projeto será desenvolvido utilizando:

* **Python**
* **Jupyter Notebook**
* **Pandas**
* **NumPy**
* **Matplotlib**
* **Seaborn**
* **SciPy**
* **Statsmodels**
* **Scikit-learn**

---

## 📁 Estrutura do projeto

```text
.
├── data/
│   ├── housing.csv              # dados originais (511 linhas)
│   └── housing_processed.csv    # dados com as colunas em log
│
├── notebooks/
│   └── EDA.ipynb                # análise completa (Partes 1 a 8)
│
├── results/
│   └── figures/                 # gráficos salvos pelo notebook
│
├── docs/
│   ├── pressupostos/            # funções, parâmetros e pressupostos de cada etapa
│   └── tarefas/                 # tarefas pendentes, uma por arquivo
│
├── TERMOS_NAO_LINEARES.md
├── requirements.txt
└── README.md
```

### `data/`

Contém o dataset utilizado no trabalho e a versão com as variáveis transformadas.

### `notebooks/`

Contém o notebook com a análise exploratória, a construção do modelo, o diagnóstico e o modelo final.

### `results/`

Gráficos obtidos durante a análise.

### `docs/pressupostos/`

Descrição de cada etapa da análise estatística do notebook: funções, parâmetros, pressupostos e o que cada resultado permite concluir. Comece pelo [índice](docs/pressupostos/README.md).

### `docs/tarefas/`

O que ainda falta fazer no projeto, uma tarefa por arquivo, com o contexto, os passos e o critério de pronto. Veja o [índice](docs/tarefas/README.md).

---

## 📈 Resultados

Os resultados abaixo são do modelo final (Parte 8 do notebook). Os detalhes estão em [`docs/pressupostos/08-modelo-final.md`](docs/pressupostos/08-modelo-final.md).

### Modelo ajustado

$$
\log(MEDV) = \beta_0 + \beta_1 CRIM + \beta_2 CHAS + \beta_3 NOX + \beta_4 \log DIS + \sum_k \gamma_k RAD_k + \beta_5 PTRATIO + \beta_6 B + \beta_7 \log LSTAT + \beta_8 RM_c + \beta_9 RM_c^2 + \beta_{10} (\log LSTAT_c)^2 + \varepsilon
$$

* `RM_c` e $\log LSTAT_c$ são centralizados na média;
* `TAX` saiu por colinearidade com `RAD`. `ZN`, `INDUS` e `AGE` saíram por não serem significativas (teste de Wald conjunto, p = 0,96);
* o ajuste usa 473 linhas: sem as 5 linhas suspeitas, as 5 com `RM` ausente e as 28 observações influentes;
* os erros padrão são robustos à heterocedasticidade (HC3).

### R²

```text
R² = 0,885 (dados do ajuste)
R² fora da amostra = 0,79 (validação cruzada com 10 partes)
```

### R² ajustado

```text
R² ajustado = 0,881 (modelo linear completo da Parte 5: 0,632)
```

### Teste F

```text
F global (HC3) = 184,1 | p-valor ≈ 1,7 × 10⁻¹⁹⁵
```

### Variáveis estatisticamente significativas

Todos os termos são significativos a 5% com HC3, e também com erros padrão agrupados por cidade. Efeitos sobre `MEDV`, mantidos os demais preditores:

| Variável | Efeito |
| --- | --- |
| `LSTAT` | +1% reduz `MEDV` em cerca de 0,31% |
| `RM` | +1 cômodo: +8% (6 cômodos), +12% (casa média), +24% (7), +42% (8) |
| `NOX` | +0,1 reduz `MEDV` em cerca de 6,4% |
| `CHAS` | margem do rio Charles: +9,6% |
| `CRIM` | +1 ponto reduz `MEDV` em 1,7% |
| `PTRATIO` | +1 aluno por professor reduz `MEDV` em 2,7% |
| `DIS` | +1% reduz `MEDV` em 0,14% |
| `RAD` | níveis 2 a 24 valem de 5% a 18% a mais que o nível 1 |
| `B` | efeito positivo e pequeno |

### Diagnóstico dos resíduos

```text
Linearidade:        aceita (RESET p = 0,94)
Normalidade:        quase normal (correlação QQ 0,993); Shapiro-Wilk ainda rejeita (p = 0,001)
Homocedasticidade:  rejeitada (Breusch-Pagan p ≈ 10⁻¹¹); tratada com erros padrão HC3
Independência:      rejeitada pela ordem do arquivo (DW = 1,41): dependência entre regiões vizinhas
Multicolinearidade: sem problema (maior VIF = 4,8, em NOX), após remover TAX e centralizar os quadrados
```

### Capacidade preditiva

Validação cruzada com 10 partes, erro em mil dólares:

| Modelo | RMSE | MAE | R² fora da amostra |
| --- | --- | --- | --- |
| Linear completo (Parte 5) | 4,80 | 3,39 | 0,71 |
| Modelo final | 4,00 | 2,75 | 0,79 |

### Limitações

* A variância dos erros não é constante. A inferência usa HC3, mas a heterocedasticidade não foi eliminada;
* Há correlação espacial entre regiões vizinhas. O conjunto de dados não tem coordenadas para modelá-la;
* `MEDV` é censurado em 50. A censura foi tratada só em parte (sem modelo Tobit);
* O ajuste remove 28 casas reais influentes. Para previsão, o modelo deve ser ajustado com todas as linhas.

---

## 📚 Referências

* Kaggle. **Real Estate Dataset**. Disponível em: https://www.kaggle.com/datasets/arslanali4343/real-estate-dataset
* Harrison, D.; Rubinfeld, D. L. (1978). *Hedonic prices and the demand for clean air*. Journal of Environmental Economics and Management, 5, 81–102.
* Belsley, D. A.; Kuh, E.; Welsch, R. E. (1980). *Regression Diagnostics: Identifying Influential Data and Sources of Collinearity*. Wiley.
* Montgomery, D.C.; Vining, G.C.; Peck, E.A. *Introduction to Linear Regression Analysis*. New York: John Wiley, 2012

---

## 👥 Autores

**Luiz Eduardo Ferreira Coelho**

**José de Ribamar Ferreira Neto**

---

## 🎓 Contexto acadêmico

Projeto desenvolvido como parte das atividades da disciplina de **Modelagem Estatística**, com foco na aplicação de conceitos de **Regressão Linear Múltipla, Inferência Estatística e Modelagem Estatística**.
