"""Funções de gráfico (Plotly) usadas pelos notebooks 01-AED e 02-MRLM.

Gráficos interativos: passe o mouse sobre um ponto para ver a linha do arquivo, a cidade
e os valores da observação; clique na legenda para esconder ou mostrar uma série.

Chame configurar(df, pasta_figuras) antes de usar as funções: texto_hover e os gráficos
da AED leem o conjunto de dados, e mostrar_e_salvar grava as figuras nessa pasta.
"""
import math
import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from scipy import stats
from scipy.stats import gaussian_kde
from statsmodels.nonparametric.smoothers_lowess import lowess

COR_PONTO = "#2a78d6"
COR_CURVA = "#eb6834"
COR_DESTAQUE = "#4a3aa7"
COR_REFERENCIA = "#898781"
COR_ALERTA = "#fab219"
COR_CRITICO = "#d03b3b"
COR_ENVELOPE = "rgba(137, 135, 129, 0.25)"
ESCALA_DIVERGENTE = [[0, "#184f95"], [0.25, "#6da7ec"], [0.5, "#f0efec"], [0.75, "#ec835a"], [1, "#a32a2a"]]

pio.templates["boston"] = go.layout.Template(layout=dict(
    colorway=["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"],
    font=dict(family="system-ui, -apple-system, Segoe UI, sans-serif", color="#0b0b0b"),
    paper_bgcolor="#fcfcfb",
    plot_bgcolor="#fcfcfb",
    hovermode="closest",
    hoverlabel=dict(bgcolor="#ffffff", font_size=12),
))
pio.templates.default = "plotly_white+boston"

CONTEXTO_HOVER = {"MEDV": "{:.1f}", "CRIM": "{:.3f}", "RM": "{:.2f}", "LSTAT": "{:.2f}", "RAD": "{}"}

# Estado definido por configurar()
df = None
cidades = None
output_fig_dir = None


def configurar(dados, pasta_figuras, arquivo_cidades="../data/boston_corrected.csv"):
    # Conjunto de dados mostrado no texto ao passar o mouse e pasta onde as figuras são salvas
    global df, cidades, output_fig_dir
    df = dados
    # Cidade de cada linha (versão corrigida do Boston Housing, mesma ordem de linhas de housing.csv)
    cidades = pd.read_csv(arquivo_cidades, usecols=["TOWN"])["TOWN"]
    output_fig_dir = pasta_figuras
    os.makedirs(output_fig_dir, exist_ok=True)


def texto_hover(indices, extras=None):
    # Um texto por observação: linha, cidade, os valores do gráfico (extras) e as principais variáveis
    indices = list(indices)
    extras = {nome: np.asarray(valores) for nome, valores in ({} if extras is None else extras).items()}
    contexto = df.loc[indices, list(CONTEXTO_HOVER)]
    textos = []
    for k, indice in enumerate(indices):
        partes = [f"<b>Linha {indice}</b> ({cidades.get(indice, 'sem cidade')})"]
        partes += [f"{nome}: {valores[k]:.3f}" for nome, valores in extras.items()]
        partes += [f"{coluna}: {formato.format(contexto.iloc[k][coluna])}" for coluna, formato in CONTEXTO_HOVER.items()]
        textos.append("<br>".join(partes))
    return textos


def pontos(x, y, indices, extras=None, nome="Observações", cor=COR_PONTO, tamanho=7, **kwargs):
    return go.Scatter(
        x=np.asarray(x), y=np.asarray(y), mode="markers", name=nome,
        marker=dict(color=cor, size=tamanho, opacity=0.65, line=dict(width=0.5, color="#fcfcfb")),
        hovertext=texto_hover(indices, extras), hovertemplate="%{hovertext}<extra></extra>", **kwargs,
    )


def curva_lowess(x, y, nome="LOWESS"):
    # Mesmo ajuste do sns.regplot(lowess=True): statsmodels lowess com frac = 2/3
    suave = lowess(np.asarray(y, dtype=float), np.asarray(x, dtype=float), frac=2 / 3)
    return go.Scatter(x=suave[:, 0], y=suave[:, 1], mode="lines", name=nome, line=dict(color=COR_CURVA, width=2.5),
                      hovertemplate=f"{nome}<br>x = %{{x:.3f}}<br>y = %{{y:.3f}}<extra></extra>")


def linha_ref(fig, valor, inicio, fim, nome, cor=COR_REFERENCIA, vertical=False, traco="dash", row=None, col=None):
    # Linha de referência como série (aparece na legenda e mostra o valor ao passar o mouse)
    ao_longo = np.linspace(inicio, fim, 60)
    constante = np.full_like(ao_longo, valor)
    x, y = (constante, ao_longo) if vertical else (ao_longo, constante)
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=nome, line=dict(color=cor, width=1.5, dash=traco),
                             hovertemplate=f"{nome}: {valor:.4g}<extra></extra>"), row=row, col=col)


def faixa(valores, margem=0.03):
    valores = np.asarray(valores, dtype=float)
    minimo, maximo = np.nanmin(valores), np.nanmax(valores)
    folga = (maximo - minimo) * margem
    return minimo - folga, maximo + folga


def envelope_qq(n_m, rng):
    # Quantis teóricos e envelope 95% de 100 amostras N(0, 1) ordenadas
    q = stats.norm.ppf((np.arange(1, n_m + 1) - 0.375) / (n_m + 0.25))
    sim = np.sort(rng.standard_normal((100, n_m)), axis=1)
    return q, np.percentile(sim, 2.5, axis=0), np.percentile(sim, 97.5, axis=0)


def tracos_qq(residuos, indices, q, inf, sup, nome_residuo="Res. studentizado"):
    # Gráfico QQ: envelope, pontos dentro e fora dele e reta y = x. Devolve as séries e o nº fora do envelope.
    ordem = np.argsort(np.asarray(residuos), kind="stable")
    rs = np.asarray(residuos)[ordem]
    idx = np.asarray(indices)[ordem]
    fora = (rs < inf) | (rs > sup)
    tracos = [
        go.Scatter(x=q, y=sup, mode="lines", name="Envelope 95%", line=dict(width=0, color=COR_REFERENCIA), showlegend=False,
                   hovertemplate="Envelope 95% (limite superior): %{y:.3f}<extra></extra>"),
        go.Scatter(x=q, y=inf, mode="lines", name="Envelope 95%", line=dict(width=0, color=COR_REFERENCIA),
                   fill="tonexty", fillcolor=COR_ENVELOPE,
                   hovertemplate="Envelope 95% (limite inferior): %{y:.3f}<extra></extra>"),
        go.Scatter(x=q, y=q, mode="lines", name="Reta y = x", line=dict(color=COR_CRITICO, width=1.5),
                   hovertemplate="Reta y = x: %{y:.3f}<extra></extra>"),
    ]
    for nome, mascara, cor in [("Dentro do envelope", ~fora, COR_PONTO), ("Fora do envelope", fora, COR_CRITICO)]:
        if mascara.any():
            tracos.append(pontos(q[mascara], rs[mascara], idx[mascara], nome=nome, cor=cor, tamanho=6,
                                 extras={"Quantil teórico": q[mascara], nome_residuo: rs[mascara]}))
    return tracos, int(fora.sum())


def legenda_unica(fig):
    # Séries de mesmo nome em painéis diferentes viram um grupo: um item na legenda liga e desliga todas
    vistos = set()
    for traco in fig.data:
        if traco.name is None:
            continue
        traco.legendgroup = traco.name
        traco.showlegend = traco.name not in vistos and traco.showlegend is not False
        if traco.showlegend:
            vistos.add(traco.name)


def mostrar_e_salvar(fig, nome=None, titulo=None, altura=500, largura=None):
    legenda_unica(fig)
    fig.update_layout(title=titulo, height=altura, width=largura, margin=dict(t=90 if titulo else 60))
    if nome:
        fig.write_html(f"{output_fig_dir}/{nome}.html", include_plotlyjs="cdn")
    fig.show()


def gerar_subplot_hist(variaveis: list[str], size: tuple[int, int], name: str):

    n_cols = 4
    n_rows = math.ceil(len(variaveis)/n_cols)

    titulos = [
        f"{v}<br><sup>Assimetria: {df[v].skew():.2f} | Curtose: {df[v].kurt():.2f}</sup>"
        for v in variaveis
    ]
    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=titulos, vertical_spacing=0.12)

    for k, variavel in enumerate(variaveis):
        linha, coluna = k // n_cols + 1, k % n_cols + 1
        valores = df[variavel].dropna().to_numpy()
        # Mesmas classes do sns.histplot (regra "auto" do numpy) e a densidade (KDE) na escala da frequência
        bordas = np.histogram_bin_edges(valores, bins="auto")
        largura_classe = bordas[1] - bordas[0]
        fig.add_trace(go.Histogram(
            x=valores, name="Frequência", marker=dict(color=COR_PONTO, line=dict(width=1, color="#fcfcfb")),
            xbins=dict(start=bordas[0], end=bordas[-1], size=largura_classe),
            hovertemplate=f"{variavel}: %{{x}}<br>Frequência: %{{y}}<extra></extra>",
        ), row=linha, col=coluna)
        grade = np.linspace(valores.min(), valores.max(), 200)
        fig.add_trace(go.Scatter(
            x=grade, y=gaussian_kde(valores)(grade) * len(valores) * largura_classe, mode="lines", name="KDE",
            line=dict(color=COR_CURVA, width=2),
            hovertemplate=f"KDE<br>{variavel} = %{{x:.3f}}<br>frequência esperada = %{{y:.1f}}<extra></extra>",
        ), row=linha, col=coluna)

    fig.update_yaxes(title_text="Frequência", col=1)
    mostrar_e_salvar(fig, name, altura=size[1] * 75)

def gerar_subplot_regplot(variaveis: list[str], y: str, size: tuple[int, int], name: str):

    n_cols = 4
    n_rows = math.ceil(len(variaveis)/n_cols)

    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=[f"{y} x {v}" for v in variaveis],
                        vertical_spacing=0.08)

    for k, variavel in enumerate(variaveis):
        linha, coluna = k // n_cols + 1, k % n_cols + 1
        dados = df[[variavel, y]].dropna()
        fig.add_trace(pontos(dados[variavel], dados[y], dados.index, tamanho=5,
                             extras={variavel: dados[variavel], y: dados[y]}), row=linha, col=coluna)
        fig.add_trace(curva_lowess(dados[variavel], dados[y]), row=linha, col=coluna)

    mostrar_e_salvar(fig, name, altura=size[1] * 85)

def grafico_categoria(variavel: str, name: str):
    # Boxplot de MEDV por nível (com todos os pontos) e contagem de observações por nível
    niveis = [str(c) for c in df[variavel].cat.categories]
    fig = make_subplots(rows=1, cols=2, subplot_titles=[f"MEDV por {variavel}", f"Frequência de {variavel}"])
    fig.add_trace(go.Box(
        x=df[variavel].astype(str), y=df["MEDV"], name="MEDV", boxpoints="all", jitter=0.4, pointpos=0,
        marker=dict(color=COR_PONTO, size=4, opacity=0.5), line=dict(color=COR_PONTO), fillcolor="rgba(42, 120, 214, 0.15)",
        hovertext=texto_hover(df.index), hoveron="boxes+points",
    ), row=1, col=1)
    contagem = df[variavel].astype(str).value_counts().reindex(niveis)
    fig.add_trace(go.Bar(x=niveis, y=contagem.values, name="Frequência", marker=dict(color=COR_PONTO),
                         hovertemplate=f"{variavel} = %{{x}}<br>Frequência: %{{y}}<extra></extra>"), row=1, col=2)
    fig.update_xaxes(title_text=variavel, type="category", categoryorder="array", categoryarray=niveis)
    fig.update_yaxes(title_text="MEDV", row=1, col=1)
    fig.update_yaxes(title_text="Frequência", row=1, col=2)
    fig.update_layout(showlegend=False)
    mostrar_e_salvar(fig, name, altura=450)

def heatmap_correlacao(matriz: pd.DataFrame, titulo: str, name: str):
    fig = go.Figure(go.Heatmap(
        z=matriz.values, x=list(matriz.columns), y=list(matriz.index), zmin=-1, zmax=1, zmid=0,
        colorscale=ESCALA_DIVERGENTE, text=matriz.round(2).values, texttemplate="%{text:.2f}",
        xgap=1, ygap=1, colorbar=dict(title="ρ"),
        hovertemplate="%{y} x %{x}<br>correlação = %{z:.3f}<extra></extra>",
    ))
    fig.update_yaxes(autorange="reversed", scaleanchor="x")
    mostrar_e_salvar(fig, name, titulo=titulo, altura=750, largura=850)

def medidas_diagnostico(m):
    # Valores mostrados ao passar o mouse sobre cada ponto dos gráficos de diagnóstico
    infl = m.get_influence()
    return {"Ajustado": m.fittedvalues, "Resíduo": m.resid, "Res. studentizado": infl.resid_studentized_external,
            "Alavanca": infl.hat_matrix_diag, "Cook": infl.cooks_distance[0]}

def graficos_diagnostico(m, dados, titulo, nome_arquivo):
    # Gráfico QQ com envelope, resíduos x ajustados, escala-locação e distância de Cook de um ajuste MQO
    infl = m.get_influence()
    n_m = int(m.nobs)
    indices = m.fittedvalues.index
    medidas = medidas_diagnostico(m)
    q, inf, sup = envelope_qq(n_m, np.random.default_rng(42))
    tracos, fora = tracos_qq(infl.resid_studentized_external, indices, q, inf, sup)
    rotulo_x = f"Valor ajustado ({m.model.endog_names})"
    raiz = np.sqrt(np.abs(infl.resid_studentized_internal))
    cook = infl.cooks_distance[0]

    fig = make_subplots(rows=2, cols=2, vertical_spacing=0.12, subplot_titles=[
        f"Gráfico QQ | fora do envelope: {fora} de {n_m}", "Resíduos x valores ajustados",
        "Escala-locação", "Distância de Cook"])
    for traco in tracos:
        fig.add_trace(traco, row=1, col=1)

    fig.add_trace(pontos(m.fittedvalues, m.resid, indices, medidas), row=1, col=2)
    fig.add_trace(curva_lowess(m.fittedvalues, m.resid), row=1, col=2)
    linha_ref(fig, 0, *faixa(m.fittedvalues), "Resíduo zero", cor="#0b0b0b", traco="solid", row=1, col=2)

    fig.add_trace(pontos(m.fittedvalues, raiz, indices, {**medidas, "√|res. padronizado|": raiz}), row=2, col=1)
    fig.add_trace(curva_lowess(m.fittedvalues, raiz), row=2, col=1)

    acima = cook > 4 / n_m
    fig.add_trace(go.Bar(x=np.asarray(indices), y=cook, name="Distância de Cook",
                         marker=dict(color=np.where(acima, COR_CRITICO, COR_PONTO)),
                         hovertext=texto_hover(indices, medidas), hovertemplate="%{hovertext}<extra></extra>"),
                  row=2, col=2)
    linha_ref(fig, 4 / n_m, *faixa(indices), "Cook = 4/n", cor=COR_ALERTA, row=2, col=2)

    fig.update_xaxes(title_text="Quantil teórico N(0, 1)", row=1, col=1)
    fig.update_yaxes(title_text="Resíduo studentizado", row=1, col=1)
    fig.update_xaxes(title_text=rotulo_x, row=1, col=2)
    fig.update_yaxes(title_text="Resíduo", row=1, col=2)
    fig.update_xaxes(title_text=rotulo_x, row=2, col=1)
    fig.update_yaxes(title_text="√|resíduo padronizado|", row=2, col=1)
    fig.update_xaxes(title_text="Índice da observação", row=2, col=2)
    fig.update_yaxes(title_text="Distância de Cook", row=2, col=2)
    mostrar_e_salvar(fig, nome_arquivo, titulo=titulo, altura=900)
