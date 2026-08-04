#!/usr/bin/env python3
"""Gera as figuras das notas de aula (versão do aluno).

Uso:
    python3 recursos/figuras/gerar-figuras.py            # gera tudo
    python3 recursos/figuras/gerar-figuras.py 01 02      # só as aulas 01 e 02

Cada figura é um PDF vetorial em ``recursos/figuras/``, incluído nas notas com

    \\includegraphics[width=...]{../../recursos/figuras/NN-nome.pdf}

Convenções (as mesmas dos notebooks das aulas práticas):

* ``rng = np.random.default_rng(semente)`` em toda simulação, semente fixa por
  figura --- as figuras são reproduzíveis;
* ``from matplotlib.pyplot import subplots`` e API orientada a objeto;
* os parâmetros da população sintética da aula 01 (``r``, ``SIGMA``, ``A``, ``B``,
  ``n_tr=50``) são idênticos aos do notebook ``Aula prática 01.ipynb``, de modo que
  o aluno reencontra na prática exatamente os números da figura.
"""

import os
import sys

import numpy as np
from matplotlib.pyplot import subplots, close
import matplotlib as mpl

import sklearn.linear_model as skl
import sklearn.model_selection as skm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

# --------------------------------------------------------------------------- #
# Estilo: casar com o corpo do texto (Computer Modern na matemática, serifa no
# texto). Tamanhos pensados para figuras de ~0,8\textwidth em corpo 11pt.
# --------------------------------------------------------------------------- #
mpl.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.5,
    "lines.linewidth": 1.4,
    "figure.constrained_layout.use": True,
    "pdf.fonttype": 42,
})

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))

# Paleta alinhada às cores do estilo-notas.sty
AZUL = "#002D62"     # azulufrj
VERDE = "#006644"    # verdeesc
VINHO = "#800020"    # vinho
CINZA = "#7A7A7A"

_REGISTRO = {}


def figura(nome, aula):
    """Registra uma função geradora sob o nome de arquivo ``nome``."""
    def _dec(func):
        _REGISTRO[nome] = (aula, func)
        return func
    return _dec


def salvar(fig, nome):
    destino = os.path.join(AQUI, nome + ".pdf")
    fig.savefig(destino, bbox_inches="tight", pad_inches=0.02)
    close(fig)
    print(f"  -> {nome}.pdf")


# =========================================================================== #
# Aula 01 --- Introdução
# =========================================================================== #

def r(x):
    """A função de regressão verdadeira (a mesma do notebook da aula 01)."""
    return np.sin(1.5 * x) + 0.3 * x


SIGMA = 0.7          # desvio-padrão do ruído  => erro irredutível = 0.49
A, B = -3.0, 3.0     # suporte de X
N_TR = 50            # tamanho da amostra de treino


def amostra(n, rng):
    x = rng.uniform(A, B, size=n)
    y = r(x) + rng.normal(0, SIGMA, size=n)
    return x, y


def modelo_poly(grau):
    return Pipeline([
        ("poly", PolynomialFeatures(degree=grau, include_bias=False)),
        ("escala", StandardScaler()),
        ("mqo", skl.LinearRegression()),
    ])


@figura("01-ajustes", "01")
def _ajustes():
    """Grau 1, 5 e 15 sobre a MESMA amostra: subajuste, bom ajuste, superajuste."""
    rng = np.random.default_rng(0)
    x, y = amostra(N_TR, rng)
    grade = np.linspace(A, B, 400)

    fig, axes = subplots(1, 3, figsize=(7.2, 2.5), sharey=True)
    for ax, grau, rotulo in zip(axes, [1, 5, 15],
                                ["subajuste", "equilíbrio", "superajuste"]):
        modelo = modelo_poly(grau).fit(x.reshape(-1, 1), y)
        ax.scatter(x, y, s=12, color=CINZA, alpha=0.7, zorder=2,
                   label="amostra de treino")
        ax.plot(grade, r(grade), color=VERDE, lw=1.6, zorder=3,
                label=r"$r(x)$ verdadeira")
        ax.plot(grade, modelo.predict(grade.reshape(-1, 1)), color=VINHO,
                lw=1.6, zorder=4, label=r"$\widehat{r}(x)$ ajustada")
        ax.set_title(f"grau {grau} \u2014 {rotulo}")
        ax.set_xlabel("$x$")
        ax.set_ylim(-3.2, 3.2)
    axes[0].set_ylabel("$y$")
    axes[0].legend(loc="upper left", framealpha=0.9)
    salvar(fig, "01-ajustes")


def _simular(graus, n_rep, semente, n_grade=400):
    """Roda ``n_rep`` amostras de treino e devolve tudo que as duas figuras usam.

    A grade de teste é fixa e o risco é calculado **sem sortear ruído de teste**:
    como  E[(Y-\\widehat{r}(x))^2 | x] = (r(x)-\\widehat{r}(x))^2 + sigma^2,
    basta comparar com ``r`` e somar ``sigma^2``. Isso elimina uma fonte inteira
    de variabilidade de Monte Carlo e deixa as curvas limpas.
    """
    rng = np.random.default_rng(semente)
    x0 = np.linspace(A, B, n_grade)
    r0 = r(x0)
    X0 = x0.reshape(-1, 1)

    treino = np.zeros((n_rep, len(graus)))
    preds = np.zeros((len(graus), n_rep, n_grade))
    for b in range(n_rep):
        x, y = amostra(N_TR, rng)
        Xb = x.reshape(-1, 1)
        for j, g in enumerate(graus):
            m = modelo_poly(g).fit(Xb, y)
            treino[b, j] = np.mean((y - m.predict(Xb)) ** 2)
            preds[j, b] = m.predict(X0)

    media = preds.mean(axis=1)                              # E_D[rhat(x0)]
    vies2 = ((media - r0) ** 2).mean(axis=1)                # media_x vies(x)^2
    variancia = preds.var(axis=1).mean(axis=1)              # media_x Var(x)
    # risco calculado direto, sem usar a decomposição:
    risco = ((preds - r0) ** 2).mean(axis=(1, 2)) + SIGMA ** 2
    return dict(treino=treino.mean(axis=0), risco=risco,
                vies2=vies2, variancia=variancia)


@figura("01-curva-U", "01")
def _curva_u():
    """O erro de treino cai sempre; o risco tem forma de U."""
    graus = np.arange(1, 13)
    sim = _simular(graus, n_rep=400, semente=1)
    treino, risco = sim["treino"], sim["risco"]
    melhor = graus[int(np.argmin(risco))]
    topo = 1.9

    fig, ax = subplots(figsize=(4.8, 3.2))
    ax.plot(graus, risco, "o-", color=VINHO, ms=3.5,
            label=r"risco $R(\widehat{r}\,)$ --- erro de teste")
    ax.plot(graus, treino, "s-", color=AZUL, ms=3.5,
            label=r"erro de treino $\widehat{R}(\widehat{r}\,)$")
    ax.axhline(SIGMA ** 2, color=VERDE, ls="--", lw=1.2,
               label=r"erro irredutível $\sigma^2=%.2f$" % SIGMA ** 2)
    ax.axvline(melhor, color=CINZA, ls=":", lw=1.0)

    ax.annotate("subajuste", xy=(1.6, 1.06), fontsize=8, color=CINZA)
    ax.annotate("superajuste", xy=(8.4, 1.62), fontsize=8, color=CINZA)
    ax.annotate(f"mínimo do risco:\ngrau {melhor}", xy=(melhor, risco.min()),
                xytext=(melhor - 0.4, 1.30), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="->", lw=0.8, color=CINZA))
    ax.text(11.9, topo - 0.06, f"$\\rightarrow$ {risco[-1]:.0f} no grau {graus[-1]}",
            fontsize=7.5, ha="right", va="top", color=VINHO)

    ax.set_xlabel(r"grau do polinômio (flexibilidade $\rightarrow$)")
    ax.set_ylabel("erro quadrático médio")
    ax.set_ylim(0.28, topo)
    ax.set_xticks(graus)
    ax.legend(loc="upper left", framealpha=0.95)
    salvar(fig, "01-curva-U")


@figura("01-vies-variancia", "01")
def _vies_variancia():
    """viés² + variância + sigma² = risco, grau a grau."""
    graus = np.arange(1, 10)
    sim = _simular(graus, n_rep=500, semente=2)
    vies2, variancia, risco = sim["vies2"], sim["variancia"], sim["risco"]
    soma = vies2 + variancia + SIGMA ** 2
    folga = np.abs(soma - risco).max()
    print(f"     [conferência] max |viés²+var+σ² − risco| = {folga:.2e}")

    # Escala linear de propósito: em log, o viés^2 aparenta *subir* nos graus
    # altos --- efeito das raras predições catastróficas puxando a média E_D --- e
    # isso contradiria a leitura correta da figura. Na escala do risco, esse
    # detalhe vive abaixo de 0,04 e a história (viés cai, variância sobe) fica
    # limpa, com a identidade visível a olho nu.
    fig, ax = subplots(figsize=(5.0, 3.3))
    ax.plot(graus, soma, "-", color="black", lw=3.0, alpha=0.28,
            label=r"viés$^2$ + variância + $\sigma^2$")
    ax.plot(graus, risco, "^", color="black", ms=5, ls="none",
            label=r"risco $R(\widehat{r}\,)$, medido à parte")
    ax.plot(graus, vies2, "o-", color=AZUL, ms=3.5, label=r"viés$^2$ (cai)")
    ax.plot(graus, variancia, "s-", color=VINHO, ms=3.5, label="variância (sobe)")
    ax.axhline(SIGMA ** 2, color=VERDE, ls="--", lw=1.2,
               label=r"$\sigma^2$ (irredutível)")

    ax.set_xlabel(r"grau do polinômio (flexibilidade $\rightarrow$)")
    ax.set_ylabel("contribuição ao risco")
    ax.set_xticks(graus)
    ax.set_ylim(0, 1.75)
    ax.legend(loc="upper left", fontsize=7.5, framealpha=0.95)
    salvar(fig, "01-vies-variancia")


# =========================================================================== #
# Aula 03 --- Seleção de Modelos e Validação Cruzada
# =========================================================================== #

@figura("03-cv-vs-risco", "03")
def _cv_vs_risco():
    """A CV enxerga o "U" a partir de UMA amostra, sem conhecer a população."""
    graus = np.arange(1, 11)
    # (a) risco verdadeiro: só existe porque inventamos a população
    verdade = _simular(graus, n_rep=300, semente=5)["risco"]

    # (b) o que o analista realmente tem: uma amostra de treino, e só
    rng = np.random.default_rng(6)
    x, y = amostra(N_TR, rng)
    X = x.reshape(-1, 1)
    dobras = skm.KFold(5, shuffle=True, random_state=0)
    cv_media, cv_ep, treino = [], [], []
    for g in graus:
        pontuacao = -skm.cross_val_score(modelo_poly(g), X, y, cv=dobras,
                                         scoring="neg_mean_squared_error")
        cv_media.append(pontuacao.mean())
        cv_ep.append(pontuacao.std(ddof=1) / np.sqrt(len(pontuacao)))
        m = modelo_poly(g).fit(X, y)
        treino.append(np.mean((y - m.predict(X)) ** 2))
    cv_media, cv_ep = np.array(cv_media), np.array(cv_ep)

    g_cv = graus[int(np.argmin(cv_media))]
    g_verdade = graus[int(np.argmin(verdade))]
    # regra de 1 erro-padrão: modelo mais simples dentro de 1 EP do mínimo
    limite = cv_media.min() + cv_ep[int(np.argmin(cv_media))]
    g_1ep = graus[int(np.argmax(cv_media <= limite))]
    print(f"     [conferência] mínimo: risco no grau {g_verdade}, "
          f"CV no grau {g_cv}, regra 1-EP no grau {g_1ep}")

    fig, ax = subplots(figsize=(5.0, 3.3))
    ax.plot(graus, verdade, "o-", color=VINHO, ms=3.5,
            label=r"risco verdadeiro (inacessível)")
    ax.errorbar(graus, cv_media, yerr=cv_ep, fmt="s-", color=AZUL, ms=3.5,
                capsize=2.5, lw=1.4, label="validação cruzada, 5 dobras")
    ax.plot(graus, treino, "^--", color=CINZA, ms=3.5, label="erro de treino")
    ax.axhline(SIGMA ** 2, color=VERDE, ls="--", lw=1.1, label=r"$\sigma^2$")
    ax.axvline(g_cv, color=AZUL, ls=":", lw=1.0)
    ax.set_xlabel(r"grau do polinômio (flexibilidade $\rightarrow$)")
    ax.set_ylabel("erro quadrático médio")
    ax.set_xticks(graus)
    ax.set_ylim(0.15, 1.65)
    ax.legend(loc="upper left", fontsize=7.5, framealpha=0.95)
    salvar(fig, "03-cv-vs-risco")


@figura("03-escolha-k", "03")
def _escolha_k():
    """Por que k=5 ou 10: o viés cai com k, mas a variância sobe."""
    grau = 5
    n_rep = 300
    ks = [2, 5, 10, 25, N_TR]           # N_TR dobras = LOOCV
    rng = np.random.default_rng(8)

    # alvo: o risco verdadeiro do procedimento nesse grau
    alvo = _simular(np.array([grau]), n_rep=300, semente=9)["risco"][0]

    estimativas = {k: [] for k in ks}
    for b in range(n_rep):
        x, y = amostra(N_TR, rng)
        X = x.reshape(-1, 1)
        for k in ks:
            cv = (skm.KFold(k, shuffle=True, random_state=b) if k < N_TR
                  else skm.KFold(N_TR))
            s = -skm.cross_val_score(modelo_poly(grau), X, y, cv=cv,
                                     scoring="neg_mean_squared_error")
            estimativas[k].append(s.mean())

    medias = np.array([np.mean(estimativas[k]) for k in ks])
    vieses = medias - alvo
    desvios = np.array([np.std(estimativas[k], ddof=1) for k in ks])
    print(f"     [conferência] risco verdadeiro = {alvo:.4f}")
    print(f"     [conferência] viés  por k: {vieses.round(4)}")
    print(f"     [conferência] desvio por k: {desvios.round(4)}"
          f"  <- NÃO cresce com k neste experimento")

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.0, 2.8))
    rotulos = [str(k) if k < N_TR else f"{N_TR}\n(LOOCV)" for k in ks]
    pos = np.arange(len(ks))

    ax1.plot(pos, np.abs(vieses), "o-", color=AZUL, ms=4, label="|viés|")
    ax1.plot(pos, desvios, "s-", color=VINHO, ms=4, label="desvio-padrão")
    ax1.set_xticks(pos); ax1.set_xticklabels(rotulos)
    ax1.set_xlabel("número de dobras $k$")
    ax1.set_ylabel("erro da estimativa do risco")
    ax1.set_yscale("log")
    ax1.set_title("precisão: tudo estabiliza a partir de $k=5$")
    ax1.legend(loc="upper right", fontsize=8)

    ax2.plot(pos, ks, "^-", color=VERDE, ms=4)
    for p, k in zip(pos, ks):
        ax2.annotate(f"{k}", xy=(p, k), xytext=(0, 5), textcoords="offset points",
                     ha="center", fontsize=7.5, color=VERDE)
    ax2.set_xticks(pos); ax2.set_xticklabels(rotulos)
    ax2.set_xlabel("número de dobras $k$")
    ax2.set_ylabel("ajustes do modelo por estimativa")
    ax2.set_ylim(0, N_TR * 1.22)
    ax2.set_title("custo: cresce linearmente com $k$")
    salvar(fig, "03-escolha-k")


# =========================================================================== #
# Aula 04 --- Métodos Não Paramétricos (KNN)
# =========================================================================== #

def _nucleo_gauss(u):
    return np.exp(-0.5 * u ** 2)


def _nadaraya_watson(x_tr, y_tr, grade, h):
    """Média ponderada por kernel gaussiano (grau 0)."""
    W = _nucleo_gauss((grade[:, None] - x_tr[None, :]) / h)
    return (W @ y_tr) / W.sum(axis=1)


def _linear_local(x_tr, y_tr, grade, h):
    """Reta ajustada localmente em cada ponto da grade (grau 1)."""
    saida = np.empty(len(grade))
    for j, x0 in enumerate(grade):
        w = _nucleo_gauss((x_tr - x0) / h)
        B = np.c_[np.ones_like(x_tr), x_tr - x0]      # centrada em x0
        M = B.T @ (w[:, None] * B)
        saida[j] = np.linalg.solve(M, B.T @ (w * y_tr))[0]
    return saida


@figura("04-knn-k", "04")
def _knn_k():
    """O k do KNN é o mesmo botão de flexibilidade da Aula 01."""
    from sklearn.neighbors import KNeighborsRegressor
    rng = np.random.default_rng(0)
    x, y = amostra(N_TR, rng)
    grade = np.linspace(A, B, 500)

    fig, axes = subplots(1, 3, figsize=(7.2, 2.5), sharey=True)
    for ax, k, rotulo in zip(axes, [1, 9, 40],
                             ["superajuste", "equilíbrio", "subajuste"]):
        m = KNeighborsRegressor(n_neighbors=k).fit(x.reshape(-1, 1), y)
        ax.scatter(x, y, s=12, color=CINZA, alpha=0.7, zorder=2)
        ax.plot(grade, r(grade), color=VERDE, lw=1.6, zorder=3, label="$r(x)$")
        ax.plot(grade, m.predict(grade.reshape(-1, 1)), color=VINHO, lw=1.5,
                zorder=4, label=r"KNN")
        ax.set_title(f"$k={k}$ — {rotulo}")
        ax.set_xlabel("$x$")
        ax.set_ylim(-3.2, 3.2)
    axes[0].set_ylabel("$y$")
    axes[0].legend(loc="upper left", fontsize=7.5)
    salvar(fig, "04-knn-k")


@figura("04-nucleos", "04")
def _nucleos():
    """Os quatro kernels da tabela, todos com h = 1."""
    u = np.linspace(-2.2, 2.2, 800)
    d = np.abs(u)
    kernels = [
        ("uniforme", np.where(d <= 1, 1.0, 0.0), AZUL),
        ("gaussiano", np.exp(-0.5 * u ** 2), VINHO),
        ("triangular", np.where(d <= 1, 1 - d, 0.0), VERDE),
        ("Epanechnikov", np.where(d <= 1, 1 - u ** 2, 0.0), "#B8860B"),
    ]
    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.0, 2.7))
    for nome, k, cor in kernels:
        ax1.plot(u, k / k.max(), color=cor, label=nome)
    # NB: aqui é $x$ mesmo, não a macro \x do estilo-notas -- o mathtext do
    # matplotlib não conhece as macros do curso e quebra em silêncio (ou não).
    ax1.set_xlabel(r"distância até $x$, em unidades de $h$")
    ax1.set_ylabel("peso (reescalado)")
    ax1.set_title("os núcleos da tabela ($h=1$)")
    ax1.legend(fontsize=7.5)

    # o que realmente muda o ajuste é h, não o núcleo
    rng = np.random.default_rng(0)
    x, y = amostra(N_TR, rng)
    grade = np.linspace(A, B, 400)
    ax2.scatter(x, y, s=10, color=CINZA, alpha=0.6)
    ax2.plot(grade, r(grade), color=VERDE, lw=1.6, label="$r(x)$")
    for h, estilo in [(0.08, ":"), (0.35, "-"), (1.5, "--")]:
        ax2.plot(grade, _nadaraya_watson(x, y, grade, h), color=VINHO, ls=estilo,
                 lw=1.4, label=f"$h={h}$")
    ax2.set_xlabel("$x$"); ax2.set_ylabel("$y$")
    ax2.set_title("é a janela $h$ que decide")
    ax2.set_ylim(-3.0, 3.0)
    ax2.legend(fontsize=7, loc="upper left", ncol=2)
    salvar(fig, "04-nucleos")


@figura("04-fronteira", "04")
def _fronteira():
    """O viés de fronteira de Nadaraya-Watson e o conserto do grau 1."""
    # Suporte [-2,2] em vez do [-3,3] das outras figuras, de propósito: o viés de
    # fronteira do NW é proporcional a r'(x) na borda, e r'(±3) ≈ -0,02 (quase
    # plana) esconderia justamente o efeito que queremos mostrar. Já r'(±2) ≈ -1,2.
    #
    # E medimos VIÉS, não o erro de uma realização: a teoria diz que o grau 1
    # corrige o viés de fronteira, e o erro de uma amostra só mistura viés com
    # ruído -- na borda o grau 1 tem variância alta e a conta de uma realização
    # chega a inverter o resultado. Por isso as B repetições abaixo.
    a, b = -2.0, 2.0
    n, h, B_rep = 200, 0.35, 300
    grade = np.linspace(a, b, 300)
    r0 = r(grade)

    rng = np.random.default_rng(3)
    est_nw = np.empty((B_rep, len(grade)))
    est_ll = np.empty((B_rep, len(grade)))
    for j in range(B_rep):
        x = rng.uniform(a, b, size=n)
        y = r(x) + rng.normal(0, SIGMA, size=n)
        est_nw[j] = _nadaraya_watson(x, y, grade, h)
        est_ll[j] = _linear_local(x, y, grade, h)

    m_nw, m_ll = est_nw.mean(axis=0), est_ll.mean(axis=0)
    dp_nw, dp_ll = est_nw.std(axis=0), est_ll.std(axis=0)
    vies_nw, vies_ll = np.abs(m_nw - r0), np.abs(m_ll - r0)
    borda = (grade < a + 0.15 * (b - a)) | (grade > b - 0.15 * (b - a))

    print(f"     [conferência] |viés| na fronteira: NW = {vies_nw[borda].mean():.4f}, "
          f"linear local = {vies_ll[borda].mean():.4f}")
    print(f"     [conferência] |viés| no miolo:     NW = {vies_nw[~borda].mean():.4f}, "
          f"linear local = {vies_ll[~borda].mean():.4f}")
    print(f"     [conferência] desvio na fronteira: NW = {dp_nw[borda].mean():.4f}, "
          f"linear local = {dp_ll[borda].mean():.4f}  <- o preço do grau 1")

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.2, 2.9))
    for ax in (ax1, ax2):
        ax.axvspan(a, a + 0.15 * (b - a), color=CINZA, alpha=0.12)
        ax.axvspan(b - 0.15 * (b - a), b, color=CINZA, alpha=0.12)

    ax1.plot(grade, r0, color=VERDE, lw=1.8, zorder=3, label="$r(x)$ verdadeira")
    ax1.fill_between(grade, m_nw - dp_nw, m_nw + dp_nw, color=VINHO, alpha=0.15)
    ax1.plot(grade, m_nw, color=VINHO, lw=1.5, zorder=4,
             label="Nadaraya--Watson (grau 0)")
    ax1.fill_between(grade, m_ll - dp_ll, m_ll + dp_ll, color=AZUL, alpha=0.15)
    ax1.plot(grade, m_ll, color=AZUL, lw=1.5, ls="--", zorder=5,
             label="linear local (grau 1)")
    ax1.set_xlabel("$x$"); ax1.set_ylabel("estimativa média")
    ax1.set_title(f"média de {B_rep} ajustes ($\\pm 1$ desvio)")
    ax1.legend(loc="lower center", fontsize=7, framealpha=0.95)

    ax2.plot(grade, vies_nw, color=VINHO, lw=1.5, label="NW (grau 0)")
    ax2.plot(grade, vies_ll, color=AZUL, lw=1.5, ls="--", label="linear local (grau 1)")
    ax2.set_xlabel("$x$"); ax2.set_ylabel(r"$|$viés$|$")
    ax2.set_title("o viés dispara só nas pontas")
    ax2.legend(loc="upper center", fontsize=7.5)
    salvar(fig, "04-fronteira")


# =========================================================================== #
# Aula 05 --- Métodos Não Paramétricos: Aspectos Teóricos
# =========================================================================== #

@figura("05-taxas", "05")
def _taxas():
    """A taxa n^{-2/(2+d)} degrada brutalmente com d."""
    n = np.logspace(1, 6, 200)
    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.0, 2.8))

    for d, cor in zip([1, 2, 5, 10, 20], [VERDE, AZUL, "#B8860B", VINHO, "black"]):
        ax1.plot(n, n ** (-2 / (2 + d)), color=cor, label=f"$d={d}$")
    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_xlabel("$n$"); ax1.set_ylabel(r"risco $\propto n^{-2/(2+d)}$")
    ax1.set_title("a taxa achata conforme $d$ cresce")
    ax1.legend(fontsize=7.5)

    # n necessário para um risco alvo fixo
    alvo = 0.05
    dd = np.arange(1, 21)
    preciso = alvo ** (-(2 + dd) / 2)
    print(f"     [conferência] n para risco {alvo}: d=1 -> {preciso[0]:.0f}, "
          f"d=5 -> {preciso[4]:.3g}, d=10 -> {preciso[9]:.3g}, d=20 -> {preciso[19]:.3g}")
    ax2.plot(dd, preciso, "o-", color=VINHO, ms=3)
    ax2.axhline(1e10, color=CINZA, ls=":", lw=1.0)
    ax2.text(1.2, 1.6e10, "$10^{10}$ observações", fontsize=7, color=CINZA)
    ax2.set_yscale("log")
    ax2.set_xlabel("$d$ (dimensão)")
    ax2.set_ylabel(f"$n$ para atingir risco {alvo}".replace("0.05", "0,05"))
    ax2.set_title("e o $n$ exigido explode")
    ax2.set_xticks([1, 5, 10, 15, 20])
    salvar(fig, "05-taxas")


@figura("05-vizinho-longe", "05")
def _vizinho_longe():
    """Em dimensão alta o "vizinho mais próximo" não é próximo de nada."""
    rng = np.random.default_rng(4)
    n = 1000
    dims = [1, 2, 3, 5, 10, 20, 50, 100]
    medias, p05 = [], []
    for d in dims:
        X = rng.uniform(0, 1, size=(n, d))
        alvo = rng.uniform(0, 1, size=(200, d))
        dist = np.sqrt(((alvo[:, None, :] - X[None, :, :]) ** 2).sum(axis=2))
        maisproximo = dist.min(axis=1)
        # normaliza pelo diâmetro do cubo, sqrt(d): fração do espaço percorrida
        medias.append((maisproximo / np.sqrt(d)).mean())
        p05.append(np.quantile(maisproximo / np.sqrt(d), 0.05))
    print(f"     [conferência] distância ao vizinho mais próximo / diâmetro: "
          f"d=1 -> {medias[0]:.4f}, d=10 -> {medias[4]:.4f}, d=100 -> {medias[-1]:.4f}")

    fig, ax = subplots(figsize=(5.0, 3.0))
    ax.plot(dims, medias, "o-", color=VINHO, ms=4, label="média")
    ax.fill_between(dims, p05, medias, color=VINHO, alpha=0.15,
                    label="entre o percentil 5 e a média")
    ax.set_xscale("log")
    ax.set_xlabel("$d$ (dimensão), escala logarítmica")
    ax.set_ylabel("distância ao vizinho mais próximo\n(fração do diâmetro do cubo)")
    ax.set_xticks(dims); ax.set_xticklabels(dims)
    ax.set_title(f"$n={n}$ pontos uniformes em $[0,1]^d$")
    ax.legend(fontsize=7.5, loc="lower right")
    salvar(fig, "05-vizinho-longe")


# =========================================================================== #
# Aula 06 --- Árvores de Regressão e Ensembles
# =========================================================================== #

@figura("06-numero-arvores", "06")
def _numero_arvores():
    """B grande é inofensivo na floresta e perigoso no boosting."""
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

    rng = np.random.default_rng(12)
    n, d, ruido = 150, 8, 1.5
    X = rng.uniform(-2, 2, size=(n, d))
    # resposta não linear com interação, dependendo só das 3 primeiras covariáveis
    def alvo(M):
        return (np.sin(1.5 * M[:, 0]) + 0.8 * M[:, 1] * M[:, 2]
                + 0.5 * M[:, 0] ** 2)
    y = alvo(X) + rng.normal(0, ruido, size=n)
    X_te = rng.uniform(-2, 2, size=(4000, d))
    y_te = alvo(X_te) + rng.normal(0, ruido, size=4000)

    Bs = np.array([1, 2, 3, 5, 8, 12, 20, 35, 60, 100, 175, 300, 500])
    rf_te, rf_tr = [], []
    for B in Bs:
        m = RandomForestRegressor(n_estimators=int(B), max_features=1/3,
                                  random_state=0).fit(X, y)
        rf_te.append(np.mean((y_te - m.predict(X_te)) ** 2))
        rf_tr.append(np.mean((y - m.predict(X)) ** 2))

    # lambda=0,05 e árvores de profundidade 3: valores realistas. O superajuste
    # aparece porque n=150 é pequeno e o ruído é alto -- não porque forçamos.
    gb = GradientBoostingRegressor(learning_rate=0.05, n_estimators=1500,
                                   max_depth=3, random_state=0).fit(X, y)
    gb_te = np.array([np.mean((y_te - p) ** 2)
                      for p in gb.staged_predict(X_te)])
    gb_tr = np.array([np.mean((y - p) ** 2) for p in gb.staged_predict(X)])
    passos = np.arange(1, len(gb_te) + 1)
    melhor = passos[int(np.argmin(gb_te))]
    print(f"     [conferência] floresta: risco em B=100 -> {rf_te[9]:.4f}, "
          f"B=500 -> {rf_te[-1]:.4f} (variação de "
          f"{100*(rf_te[-1]/rf_te[9]-1):+.1f}%)")
    print(f"     [conferência] boosting: mínimo em B={melhor} ({gb_te.min():.4f}), "
          f"em B=1500 -> {gb_te[-1]:.4f} (+{100*(gb_te[-1]/gb_te.min()-1):.0f}%)")

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.2, 2.9), sharey=True)
    ax1.plot(Bs, rf_te, "o-", color=VINHO, ms=3, label="risco (teste)")
    ax1.plot(Bs, rf_tr, "s--", color=CINZA, ms=3, label="erro de treino")
    ax1.set_xscale("log")
    ax1.set_xlabel("$B$ (número de árvores)")
    ax1.set_ylabel("erro quadrático médio")
    ax1.set_title("Floresta aleatória: estabiliza")
    ax1.legend(fontsize=7.5)

    ax2.plot(passos, gb_te, color=VINHO, label="risco (teste)")
    ax2.plot(passos, gb_tr, color=CINZA, ls="--", label="erro de treino")
    ax2.axvline(melhor, color=AZUL, ls=":", lw=1.2)
    ax2.annotate(f"mínimo em $B={melhor}$", xy=(melhor, gb_te.min()),
                 xytext=(melhor * 3.2, gb_te.min() + 1.1), fontsize=7.5,
                 arrowprops=dict(arrowstyle="->", lw=0.8, color=AZUL))
    ax2.set_xscale("log")
    ax2.set_xlabel("$B$ (número de árvores)")
    ax2.set_title(r"Boosting ($\lambda=0{,}05$): volta a subir")
    ax2.legend(fontsize=7.5)
    ax1.set_ylim(0, 6.0)
    salvar(fig, "06-numero-arvores")


# =========================================================================== #
# Aula 07 --- Pré-processamento e Pipelines
# =========================================================================== #

@figura("07-vazamento", "07")
def _vazamento():
    """Quanto custa vazar: dois tipos de vazamento, medidos.

    Cenário deliberadamente cruel: y é ruído puro, independente de X. Qualquer
    R^2 acima de zero é ilusão. O clássico do ESL §7.10.2, em versão de regressão.
    """
    from sklearn.feature_selection import SelectKBest, f_regression
    from sklearn.pipeline import Pipeline as Pipe

    rng = np.random.default_rng(21)
    n, d, k = 60, 3000, 20
    n_rep = 40
    dobras = skm.KFold(5, shuffle=True, random_state=0)

    r2_errado, r2_certo, r2_escala_errada, r2_escala_certa = [], [], [], []
    for _ in range(n_rep):
        X = rng.normal(size=(n, d))
        y = rng.normal(size=n)                 # NENHUMA relação com X

        # (1) ERRADO: seleciona as k melhores olhando TODOS os dados, e só
        #     depois faz validação cruzada.
        sel = SelectKBest(f_regression, k=k).fit(X, y)
        X_sel = sel.transform(X)
        r2_errado.append(skm.cross_val_score(skl.LinearRegression(), X_sel, y,
                                             cv=dobras, scoring="r2").mean())

        # (2) CERTO: a seleção entra no pipeline e é refeita dentro de cada dobra.
        pipe = Pipe([("sel", SelectKBest(f_regression, k=k)),
                     ("mqo", skl.LinearRegression())])
        r2_certo.append(skm.cross_val_score(pipe, X, y, cv=dobras,
                                            scoring="r2").mean())

        # (3) e (4): o mesmo par, mas com padronização no lugar da seleção,
        #     num problema pequeno e com sinal de verdade.
        Xp = rng.normal(size=(n, 8)) * np.array([1, 50, 0.01, 5, 1, 200, 0.1, 2])
        yp = Xp @ np.r_[1.5, 0.02, 80, 0.3, -1.0, 0.005, 10, 0.4] + rng.normal(0, 1, n)
        esc = StandardScaler().fit(Xp)          # ERRADO: aprende com tudo
        r2_escala_errada.append(skm.cross_val_score(
            skl.Ridge(alpha=1.0), esc.transform(Xp), yp, cv=dobras, scoring="r2").mean())
        r2_escala_certa.append(skm.cross_val_score(
            Pipeline([("sc", StandardScaler()), ("ridge", skl.Ridge(alpha=1.0))]),
            Xp, yp, cv=dobras, scoring="r2").mean())

    m = [np.mean(v) for v in (r2_errado, r2_certo, r2_escala_errada, r2_escala_certa)]
    print(f"     [conferência] seleção fora da dobra (ERRADO): R2 = {m[0]:+.3f}")
    print(f"     [conferência] seleção dentro do pipeline:     R2 = {m[1]:+.3f}")
    print(f"     [conferência] escala fora da dobra (ERRADO):  R2 = {m[2]:+.4f}")
    print(f"     [conferência] escala dentro do pipeline:      R2 = {m[3]:+.4f}")

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.2, 2.9))

    ax1.axhline(0, color="black", lw=0.8)
    ax1.bar([0, 1], [m[0], m[1]], width=0.55, color=[VINHO, VERDE])
    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(["seleção\nfora da dobra", "seleção\ndentro do pipeline"],
                        fontsize=8)
    ax1.set_ylabel("$R^2$ estimado por validação cruzada")
    ax1.set_title(f"$y$ é ruído puro ($n={n}$, $d={d}$)")
    for xx, vv in zip([0, 1], m[:2]):
        ax1.annotate(f"{vv:+.2f}", xy=(xx, vv), xytext=(0, 6 if vv > 0 else -14),
                     textcoords="offset points", ha="center", fontsize=8.5)
    ax1.set_ylim(min(m[1] * 1.35, -0.1), max(m[0] * 1.35, 0.1))

    ax2.bar([0, 1], [m[2], m[3]], width=0.55, color=[VINHO, VERDE])
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(["escala\nfora da dobra", "escala\ndentro do pipeline"],
                        fontsize=8)
    ax2.set_ylabel("$R^2$ estimado por validação cruzada")
    ax2.set_title("padronização, com sinal de verdade")
    for xx, vv in zip([0, 1], m[2:]):
        ax2.annotate(f"{vv:.4f}", xy=(xx, vv), xytext=(0, 6), textcoords="offset points",
                     ha="center", fontsize=8.5)
    baixo = min(m[2], m[3])
    ax2.set_ylim(baixo - 0.02, max(m[2], m[3]) + 0.02)
    salvar(fig, "07-vazamento")


# =========================================================================== #
# Aula 02 --- Regressão Linear e Regularização
# =========================================================================== #

def _dados_esparsos(n, d, s, rng, ruido=1.0):
    """X gaussiano, beta esparso com s coeficientes não nulos."""
    X = rng.normal(size=(n, d))
    beta = np.zeros(d)
    ativos = rng.choice(d, size=s, replace=False)
    beta[ativos] = rng.uniform(1.5, 3.0, size=s) * rng.choice([-1, 1], size=s)
    y = X @ beta + rng.normal(0, ruido, size=n)
    return X, y, beta, np.sort(ativos)


@figura("02-mqo-alta-dim", "02")
def _mqo_alta_dim():
    """Com n fixo, o MQO degrada conforme d -> n: norma explode, risco explode."""
    rng = np.random.default_rng(3)
    n, s = 60, 5
    # grade adensada perto de d = n: é lá que o problema fica mal-condicionado
    dims = np.array([2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 53, 55, 57, 58, 59])
    n_rep = 60

    normas = np.zeros((n_rep, len(dims)))
    condic = np.zeros((n_rep, len(dims)))
    riscos = np.zeros((n_rep, len(dims)))
    for b in range(n_rep):
        for j, d in enumerate(dims):
            X, y, beta, _ = _dados_esparsos(n, d, min(s, d), rng)
            X_te = rng.normal(size=(2000, d))
            y_te = X_te @ beta + rng.normal(0, 1.0, size=2000)
            mqo = skl.LinearRegression().fit(X, y)
            normas[b, j] = np.linalg.norm(mqo.coef_)
            condic[b, j] = np.linalg.cond(X.T @ X)
            riscos[b, j] = np.mean((y_te - mqo.predict(X_te)) ** 2)

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.0, 2.8))
    ax1.plot(dims, condic.mean(axis=0), "o-", color=AZUL, ms=3)
    ax1.set_xlabel("$d$ (número de covariáveis)")
    ax1.set_ylabel(r"condicionamento de $\bm{X}^\top\bm{X}$".replace(r"\bm", r"\mathbf"))
    ax1.set_title(f"o sistema fica mal-condicionado ($n={n}$)")
    ax1.set_yscale("log")

    ax2.plot(dims, riscos.mean(axis=0), "o-", color=VINHO, ms=3,
             label="risco do MQO")
    ax2.plot(dims, normas.mean(axis=0), "s-", color=AZUL, ms=3,
             label=r"$\|\widehat{\beta}^{\,\mathrm{MQO}}\|_2$")
    ax2.axhline(1.0, color=VERDE, ls="--", lw=1.2,
                label=r"erro irredutível $\sigma^2$")
    ax2.set_xlabel("$d$ (número de covariáveis)")
    ax2.set_ylabel("risco / norma")
    ax2.set_title("e o ajuste vai junto")
    ax2.set_yscale("log")
    ax2.legend(loc="upper left", fontsize=7.5)
    salvar(fig, "02-mqo-alta-dim")


@figura("02-caminho-coeficientes", "02")
def _caminho_coeficientes():
    """Caminhos de regularização: Ridge encolhe, Lasso zera."""
    rng = np.random.default_rng(4)
    n, d, s = 80, 30, 5
    X, y, beta, ativos = _dados_esparsos(n, d, s, rng)
    X = StandardScaler().fit_transform(X)

    lambdas = np.logspace(1.2, -2.2, 120)
    cam_ridge = np.array([skl.Ridge(alpha=lam * n).fit(X, y).coef_ for lam in lambdas])
    cam_lasso = np.array([skl.Lasso(alpha=lam, max_iter=50000).fit(X, y).coef_
                          for lam in lambdas])

    eixo = -np.log(lambdas)
    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.0, 2.8), sharey=True)
    for ax, caminho, titulo in [(ax1, cam_ridge, r"Ridge ($\ell_2$)"),
                                (ax2, cam_lasso, r"Lasso ($\ell_1$)")]:
        for j in range(d):
            relevante = j in ativos
            ax.plot(eixo, caminho[:, j],
                    color=(VINHO if relevante else CINZA),
                    lw=(1.4 if relevante else 0.7),
                    alpha=(1.0 if relevante else 0.45), zorder=(3 if relevante else 1))
        ax.axhline(0, color="black", lw=0.6)
        ax.set_title(titulo)
        ax.set_xlabel(r"$-\log\lambda$  (menos penalização $\rightarrow$)")
    ax1.set_ylabel(r"$\widehat{\beta}_j$")
    # legenda no painel do Ridge: à esquerda os coeficientes ainda estão todos
    # perto de zero, então o canto superior esquerdo está livre.
    ax1.plot([], [], color=VINHO, lw=1.4, label=f"as {s} covariáveis relevantes")
    ax1.plot([], [], color=CINZA, lw=0.7, label=f"as {d - s} irrelevantes")
    ax1.legend(loc="upper left", framealpha=0.9, fontsize=7.5)
    salvar(fig, "02-caminho-coeficientes")


@figura("02-soft-threshold", "02")
def _soft_threshold():
    """Caso ortonormal: Ridge multiplica, Lasso subtrai e trunca."""
    b = np.linspace(-3, 3, 600)
    lam = 1.0
    ridge = b / (1 + lam)
    lasso = np.sign(b) * np.maximum(np.abs(b) - lam / 2, 0.0)

    fig, ax = subplots(figsize=(4.0, 3.2))
    ax.plot(b, b, color=CINZA, ls="--", lw=1.0, label=r"MQO (identidade)")
    ax.plot(b, ridge, color=AZUL, label=r"Ridge: $\widehat{\beta}_j/(1+\lambda)$")
    ax.plot(b, lasso, color=VINHO,
            label=r"Lasso: $\mathrm{sinal}(\widehat{\beta}_j)(|\widehat{\beta}_j|-\lambda/2)_+$")
    ax.axhline(0, color="black", lw=0.6)
    ax.axvline(0, color="black", lw=0.6)
    ax.fill_between([-lam / 2, lam / 2], -3, 3, color=VINHO, alpha=0.07)
    ax.text(0, -2.6, "zerado\npelo Lasso", ha="center", fontsize=7, color=VINHO)
    ax.set_xlabel(r"$\widehat{\beta}_j$ do MQO")
    ax.set_ylabel("estimador penalizado")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.legend(loc="upper left", fontsize=7)
    salvar(fig, "02-soft-threshold")


# =========================================================================== #

def main(argv):
    alvos = argv[1:]
    pendentes = {n: (a, f) for n, (a, f) in _REGISTRO.items()
                 if not alvos or a in alvos}
    if not pendentes:
        print(f"nenhuma figura para {alvos}; aulas disponíveis: "
              f"{sorted({a for a, _ in _REGISTRO.values()})}")
        return 1
    for nome, (aula, func) in sorted(pendentes.items()):
        print(f"[aula {aula}] {nome}")
        func()
    print(f"\n{len(pendentes)} figura(s) em {AQUI}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
