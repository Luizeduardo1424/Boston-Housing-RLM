# Tarefa 02: verificar a correlação entre cidades vizinhas

## Contexto

As casas do Boston Housing são setores censitários de cidades da região de Boston. Setores próximos tendem a ter preços parecidos, então os erros do modelo podem ser correlacionados no espaço. Isso viola a independência dos erros e faz os erros padrão parecerem menores do que são.

O arquivo `data/housing.csv` **não tem coordenadas nem nome da cidade**. Por isso a correlação espacial não foi testada diretamente.

## Estado atual

- Durbin-Watson do modelo final na ordem do arquivo: 1,41. Com os resíduos em ordem aleatória: 2,00 (95%: 1,82 a 2,18). A dependência vem da ordem das linhas, que segue a geografia (célula 122).
- Erros padrão agrupados por cidade aproximada (`cidade`, 78 grupos, célula 122): todos os termos continuam significativos. Isso trata a correlação **dentro** de cada cidade, mas não **entre** cidades vizinhas.
- Registrado como limitação na [Seção 14.1](../pressupostos/06-transformacoes.md) e no `README.md`.

## O que fazer

1. **Encontrar coordenadas.** A versão corrigida do Boston Housing (Gilley e Pace, 1996) tem as colunas `TOWN`, `TRACT`, `LON`, `LAT` e `CMEDV` (`MEDV` corrigido). Fontes:
   - pacote R `spData`, conjunto `boston.c`;
   - o arquivo `boston.c` exportado em CSV em repositórios públicos (procure por "boston corrected LON LAT").
   Salve o arquivo em `data/` e cite a fonte.
2. **Ligar as linhas.** As 506 primeiras linhas de `housing.csv` devem estar na mesma ordem do conjunto original. Confira linha a linha que `CRIM`, `NOX`, `PTRATIO` e `MEDV` coincidem. As linhas 506 a 510 de `housing.csv` são suspeitas e já estão fora de `df_t`. Se a ordem não bater, ligue pelas variáveis (`CRIM`, `NOX`, `TAX`, `PTRATIO`). Registre quantas linhas foram ligadas.
3. **Matriz de vizinhança.** Use `libpysal`: k vizinhos mais próximos (por exemplo k = 6) com `LON` e `LAT`, padronizada por linha. Teste também uma matriz por distância, para ver se a conclusão muda.
4. **I de Moran nos resíduos.** Use `esda.Moran` com os resíduos de `modelo_final` (n = 473) e de `modelo_reduzido` (n = 501). Use 999 permutações.
5. **Se o I de Moran for significativo**, ajuste com `spreg`:
   - modelo de erro espacial (`spreg.ML_Error`);
   - modelo de defasagem espacial (`spreg.ML_Lag`).
   Use os testes LM (`spreg.OLS(..., spat_diag=True)`) para escolher entre os dois. Compare os coeficientes e os erros padrão com o modelo final.
6. **Comparar com os erros agrupados.** Use `TOWN` como grupo verdadeiro em `cov_type="cluster"` e compare com os grupos aproximados de `cidade`.

Novas dependências (`libpysal`, `esda`, `spreg`) entram em `requirements.txt`.

## Critério de pronto

- I de Moran com p-valor para os resíduos do modelo final, **ou** um registro dizendo por que não foi possível (por exemplo, nenhuma fonte com coordenadas que ligue as linhas).
- Se houver correlação espacial: tabela comparando o modelo final com o modelo espacial escolhido.
- Comparação entre os grupos `TOWN` e os grupos aproximados.

## Documentação a atualizar

- Novo `docs/pressupostos/NN-correlacao-espacial.md`.
- `07-pendencias.md`: linha "Independência espacial".
- `README.md` (raiz): "Limitações", segundo item, e a estrutura de `data/` se um arquivo novo for incluído.

## Referências

- Gilley, O. W.; Pace, R. K. (1996). On the Harrison and Rubinfeld data. *Journal of Environmental Economics and Management*, 31(3), 403–405.
- Anselin, L. (1988). *Spatial Econometrics: Methods and Models*. Kluwer.
- Documentação do PySAL: `libpysal.weights.KNN`, `esda.Moran`, `spreg`.
