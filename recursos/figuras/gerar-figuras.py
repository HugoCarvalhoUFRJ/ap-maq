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
    """Por que k=5 ou 10: o viés cai depressa com k, e o custo sobe linearmente."""
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
    print(f"     [conferência] risco verdadeiro = {alvo:.4f}")
    print(f"     [conferência] viés por k: {vieses.round(4)}")

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.0, 2.8))
    rotulos = [str(k) if k < N_TR else f"{N_TR}\n(LOOCV)" for k in ks]
    pos = np.arange(len(ks))

    ax1.plot(pos, np.abs(vieses), "o-", color=AZUL, ms=4)
    ax1.set_xticks(pos); ax1.set_xticklabels(rotulos)
    ax1.set_xlabel("número de dobras $k$")
    ax1.set_ylabel("|viés| da estimativa do risco")
    ax1.set_yscale("log")
    ax1.set_title("viés: desprezível a partir de $k=5$")

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


# =========================================================================== #
# Aula 05 --- Métodos Não Paramétricos: Aspectos Teóricos
# =========================================================================== #

@figura("05-taxas", "05")
def _taxas():
    """A taxa n^{-2/(2+d)} degrada brutalmente com d."""
    n = np.logspace(1, 6, 200)
    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.0, 2.8))

    for d, cor in zip([1, 2, 5, 10, 20], [VERDE, AZUL, "#B8860B", VINHO, "black"]):
        ax1.plot(n, n ** (-2 / (2 + d)), color=cor, label=f"$p={d}$")
    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_xlabel("$n$"); ax1.set_ylabel(r"risco $\propto n^{-2/(2+d)}$")
    ax1.set_title("a taxa achata conforme $p$ cresce")
    ax1.legend(fontsize=7.5)

    # n necessário para um risco alvo fixo
    alvo = 0.05
    dd = np.arange(1, 21)
    preciso = alvo ** (-(2 + dd) / 2)
    print(f"     [conferência] n para risco {alvo}: p=1 -> {preciso[0]:.0f}, "
          f"p=5 -> {preciso[4]:.3g}, p=10 -> {preciso[9]:.3g}, p=20 -> {preciso[19]:.3g}")
    ax2.plot(dd, preciso, "o-", color=VINHO, ms=3)
    ax2.axhline(1e10, color=CINZA, ls=":", lw=1.0)
    ax2.text(1.2, 1.6e10, "$10^{10}$ observações", fontsize=7, color=CINZA)
    ax2.set_yscale("log")
    ax2.set_xlabel("$p$ (dimensão)")
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
          f"p=1 -> {medias[0]:.4f}, p=10 -> {medias[4]:.4f}, p=100 -> {medias[-1]:.4f}")

    fig, ax = subplots(figsize=(5.0, 3.0))
    ax.plot(dims, medias, "o-", color=VINHO, ms=4, label="média")
    ax.fill_between(dims, p05, medias, color=VINHO, alpha=0.15,
                    label="entre o percentil 5 e a média")
    ax.set_xscale("log")
    ax.set_xlabel("$p$ (dimensão), escala logarítmica")
    ax.set_ylabel("distância ao vizinho mais próximo\n(fração do diâmetro do cubo)")
    ax.set_xticks(dims); ax.set_xticklabels(dims)
    ax.set_title(f"$n={n}$ pontos uniformes em $[0,1]^p$")
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
    ax1.set_title(f"$y$ é ruído puro ($n={n}$, $p={d}$)")
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
# Aula 08 --- Classificação e Classificadores Gaussianos
# =========================================================================== #

def _duas_gaussianas(n, rng, sep=2.2):
    """Duas classes gaussianas em R^2 com covariâncias DIFERENTES (favorece QDA)."""
    n0 = n // 2
    S0 = np.array([[1.0, 0.75], [0.75, 1.0]])
    S1 = np.array([[1.6, -0.85], [-0.85, 0.7]])
    X0 = rng.multivariate_normal([0, 0], S0, size=n0)
    X1 = rng.multivariate_normal([sep, sep * 0.35], S1, size=n - n0)
    X = np.vstack([X0, X1])
    y = np.r_[np.zeros(n0), np.ones(n - n0)].astype(int)
    return X, y


def _gaussianas_dim(n, d, rng):
    """O mesmo em R^d. Aqui o QDA estima d(d+1) parâmetros de covariância contra
    d(d+1)/2 do LDA -- é essa conta que faz o LDA ganhar quando n é pequeno."""
    n0 = n // 2
    Q0 = rng_fixa_Q(d, 0)
    Q1 = rng_fixa_Q(d, 1)
    mu = np.zeros(d); mu[:3] = [1.6, 1.0, 0.7]
    X0 = rng.multivariate_normal(np.zeros(d), Q0, size=n0)
    X1 = rng.multivariate_normal(mu, Q1, size=n - n0)
    X = np.vstack([X0, X1])
    y = np.r_[np.zeros(n0), np.ones(n - n0)].astype(int)
    return X, y


_CACHE_Q = {}


def rng_fixa_Q(d, qual):
    """Covariância fixa (mesma em toda chamada) para cada classe."""
    if (d, qual) not in _CACHE_Q:
        g = np.random.default_rng(1000 + qual)
        A = g.normal(size=(d, d))
        _CACHE_Q[(d, qual)] = (A @ A.T) / d + np.eye(d) * 0.5
    return _CACHE_Q[(d, qual)]


@figura("08-fronteiras", "08")
def _fronteiras():
    """Onde cada classificador traça a linha."""
    from sklearn.discriminant_analysis import (LinearDiscriminantAnalysis,
                                               QuadraticDiscriminantAnalysis)
    from sklearn.naive_bayes import GaussianNB

    rng = np.random.default_rng(31)
    X, y = _duas_gaussianas(400, rng)
    modelos = [("Logística", skl.LogisticRegression()),
               ("LDA (covariância comum)", LinearDiscriminantAnalysis()),
               ("QDA (covariância por classe)", QuadraticDiscriminantAnalysis()),
               ("Bayes ingênuo", GaussianNB())]

    xx, yy = np.meshgrid(np.linspace(X[:, 0].min() - .8, X[:, 0].max() + .8, 320),
                         np.linspace(X[:, 1].min() - .8, X[:, 1].max() + .8, 320))
    grade = np.c_[xx.ravel(), yy.ravel()]

    fig, axes = subplots(1, 4, figsize=(7.4, 2.1), sharex=True, sharey=True)
    for ax, (nome, m) in zip(axes, modelos):
        m.fit(X, y)
        Z = m.predict_proba(grade)[:, 1].reshape(xx.shape)
        ax.contourf(xx, yy, Z, levels=[0, 0.5, 1], colors=[AZUL, VINHO], alpha=0.10)
        ax.contour(xx, yy, Z, levels=[0.5], colors="black", linewidths=1.2)
        ax.scatter(X[y == 0, 0], X[y == 0, 1], s=5, color=AZUL, alpha=0.55)
        ax.scatter(X[y == 1, 0], X[y == 1, 1], s=5, color=VINHO, alpha=0.55)
        ax.set_title(nome, fontsize=7.5)
        ax.set_xticks([]); ax.set_yticks([])
        ax.grid(False)
    salvar(fig, "08-fronteiras")


@figura("08-lda-qda", "08")
def _lda_qda():
    """A troca viés-variância entre LDA e QDA, em função de n."""
    from sklearn.discriminant_analysis import (LinearDiscriminantAnalysis,
                                               QuadraticDiscriminantAnalysis)
    d = 10
    ns = np.array([30, 50, 80, 150, 300, 700, 1500, 4000])
    n_rep = 120
    rng = np.random.default_rng(32)
    X_te, y_te = _gaussianas_dim(20000, d, np.random.default_rng(99))

    acc = {"LDA": np.zeros((n_rep, len(ns))), "QDA": np.zeros((n_rep, len(ns)))}
    for b in range(n_rep):
        for j, n in enumerate(ns):
            X, y = _gaussianas_dim(int(n), d, rng)
            for nome, M in [("LDA", LinearDiscriminantAnalysis),
                            ("QDA", QuadraticDiscriminantAnalysis)]:
                try:
                    acc[nome][b, j] = M().fit(X, y).score(X_te, y_te)
                except Exception:
                    acc[nome][b, j] = np.nan

    m_lda = np.nanmean(acc["LDA"], axis=0)
    m_qda = np.nanmean(acc["QDA"], axis=0)
    virada = ns[np.argmax(m_qda > m_lda)] if np.any(m_qda > m_lda) else None
    print(f"     [conferência] acurácia LDA: {m_lda.round(4)}")
    print(f"     [conferência] acurácia QDA: {m_qda.round(4)}")
    print(f"     [conferência] QDA passa a ganhar a partir de n = {virada}")

    fig, ax = subplots(figsize=(5.0, 3.1))
    ax.plot(ns, m_lda, "o-", color=AZUL, ms=4, label="LDA (fronteira linear)")
    ax.plot(ns, m_qda, "s-", color=VINHO, ms=4, label="QDA (fronteira quadrática)")
    if virada is not None:
        ax.axvline(virada, color=CINZA, ls=":", lw=1.0)
        ax.annotate(f"QDA passa a ganhar\nem $n={virada}$", xy=(virada, m_lda.min()),
                    xytext=(virada * 1.5, m_lda.min() + 0.008), fontsize=7.5,
                    arrowprops=dict(arrowstyle="->", lw=0.8, color=CINZA))
    ax.set_xscale("log")
    ax.set_xlabel(f"$n$ (tamanho da amostra de treino), escala logarítmica")
    ax.set_ylabel("acurácia em 20 mil observações novas")
    ax.set_title(f"$p={d}$ covariáveis, covariâncias diferentes por classe")
    ax.set_xticks(ns); ax.set_xticklabels(ns)
    ax.legend(loc="lower right", fontsize=8)
    salvar(fig, "08-lda-qda")


# =========================================================================== #
# Aula 09 --- Métricas para Classificação
# =========================================================================== #

def _cenario_desbalanceado(n, rng, prev=0.08, correlacionado=False):
    """Uma classe rara (8%) com sobreposição realista.

    Com ``correlacionado=True`` as covariáveis são fortemente dependentes entre
    si dentro de cada classe -- o que torna a suposição do Bayes ingênuo
    FALSA, e é o que revela a diferença de calibração.
    """
    y = (rng.uniform(size=n) < prev).astype(int)
    if correlacionado:
        d = 6
        S = np.full((d, d), 0.85) + np.eye(d) * 0.15
        L = np.linalg.cholesky(S)
        X = rng.normal(size=(n, d)) @ L.T
        X[y == 1] += 1.05
    else:
        X = rng.normal(size=(n, 4))
        X[y == 1] += np.array([1.5, 0.9, 0.0, 0.0])
    return X, y


@figura("09-roc-metricas", "09")
def _roc_metricas():
    """ROC, AUC e o efeito do corte sobre as métricas."""
    from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve

    rng = np.random.default_rng(41)
    X, y = _cenario_desbalanceado(4000, rng)
    X_te, y_te = _cenario_desbalanceado(20000, np.random.default_rng(42))
    m = Pipeline([("sc", StandardScaler()),
                  ("lg", skl.LogisticRegression())]).fit(X, y)
    p = m.predict_proba(X_te)[:, 1]

    fpr, tpr, cortes = roc_curve(y_te, p)
    auc = roc_auc_score(y_te, p)
    acuracia_trivial = 1 - y_te.mean()
    print(f"     [conferência] prevalência = {y_te.mean():.3f}; "
          f"acurácia do classificador trivial = {acuracia_trivial:.3f}")
    print(f"     [conferência] AUC = {auc:.3f}; "
          f"acurácia com corte 0,5 = {((p >= 0.5) == y_te).mean():.3f}")

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.2, 3.0))
    ax1.plot(fpr, tpr, color=VINHO, lw=1.6, label=f"logística (AUC $= {auc:.3f}$)")
    ax1.plot([0, 1], [0, 1], color=CINZA, ls="--", lw=1.0,
             label="palpite aleatório (AUC $=0{,}5$)")
    for alvo, marca in [(0.5, "o"), (0.2, "s"), (0.08, "^")]:
        j = int(np.argmin(np.abs(cortes - alvo)))
        ax1.plot(fpr[j], tpr[j], marca, color=AZUL, ms=5.5)
        ax1.annotate(f"corte {alvo:.2f}".replace(".", ","),
                     xy=(fpr[j], tpr[j]), xytext=(9, -9),
                     textcoords="offset points", fontsize=7, color=AZUL)
    ax1.set_xlabel("taxa de falsos positivos  $1-$especificidade")
    ax1.set_ylabel("sensibilidade (recall)")
    ax1.set_title("curva ROC")
    ax1.legend(loc="lower right", fontsize=7.5)

    grade = np.linspace(0.01, 0.95, 200)
    prec, rec, f1 = [], [], []
    for t in grade:
        pred = (p >= t)
        tp = np.sum(pred & (y_te == 1)); fp = np.sum(pred & (y_te == 0))
        fn = np.sum(~pred & (y_te == 1))
        pr = tp / (tp + fp) if tp + fp else np.nan
        rc = tp / (tp + fn) if tp + fn else np.nan
        prec.append(pr); rec.append(rc)
        f1.append(2 * pr * rc / (pr + rc) if pr and rc else np.nan)
    melhor_t = grade[int(np.nanargmax(f1))]
    print(f"     [conferência] F1 máximo no corte {melhor_t:.2f} "
          f"(F1 = {np.nanmax(f1):.3f}), não em 0,50")

    ax2.plot(grade, prec, color=AZUL, label="precisão")
    ax2.plot(grade, rec, color=VINHO, label="sensibilidade")
    ax2.plot(grade, f1, color=VERDE, lw=1.8, label="$F_1$")
    ax2.axvline(0.5, color=CINZA, ls="--", lw=1.0)
    ax2.text(0.52, 0.03, "corte 0,50\n(o padrão)", fontsize=7, color=CINZA)
    ax2.axvline(melhor_t, color=VERDE, ls=":", lw=1.2)
    ax2.text(melhor_t - 0.02, 0.88, f"$F_1$ máx.\nem {melhor_t:.2f}".replace(".", ","),
             fontsize=7, color=VERDE, ha="right")
    ax2.set_xlabel("corte aplicado a $\\widehat{P}(Y=1\\mid x)$")
    ax2.set_ylabel("valor da métrica")
    ax2.set_title("o corte muda tudo")
    ax2.set_ylim(0, 1.02)
    ax2.legend(loc="center right", fontsize=7.5)
    salvar(fig, "09-roc-metricas")


@figura("09-calibracao", "09")
def _calibracao():
    """Classificar bem não é o mesmo que estimar bem probabilidades."""
    from sklearn.calibration import calibration_curve
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import roc_auc_score, brier_score_loss

    rng = np.random.default_rng(43)
    X, y = _cenario_desbalanceado(4000, rng, correlacionado=True)
    X_te, y_te = _cenario_desbalanceado(20000, np.random.default_rng(44),
                                        correlacionado=True)

    modelos = [("regressão logística", Pipeline([("sc", StandardScaler()),
                                                 ("lg", skl.LogisticRegression())]), AZUL),
               ("Bayes ingênuo", GaussianNB(), VINHO)]
    fig, ax = subplots(figsize=(4.6, 3.4))
    ax.plot([0, 1], [0, 1], color=CINZA, ls="--", lw=1.0, label="calibração perfeita")
    for nome, m, cor in modelos:
        m.fit(X, y)
        p = m.predict_proba(X_te)[:, 1]
        obs, prev = calibration_curve(y_te, p, n_bins=10, strategy="quantile")
        auc = roc_auc_score(y_te, p)
        brier = brier_score_loss(y_te, p)
        print(f"     [conferência] {nome}: AUC = {auc:.3f}, Brier = {brier:.4f}")
        ax.plot(prev, obs, "o-", color=cor, ms=4,
                label=f"{nome}\nAUC $={auc:.3f}$, Brier $={brier:.4f}$")
    ax.set_xlabel("probabilidade predita")
    ax.set_ylabel("frequência observada")
    ax.set_title("curva de calibração")
    ax.legend(loc="upper left", fontsize=7)
    salvar(fig, "09-calibracao")


# =========================================================================== #
# Aula 10 --- Máquinas de Vetores de Suporte
# =========================================================================== #

@figura("10-margem", "10")
def _margem():
    """Margem máxima, vetores de suporte e o efeito de C."""
    from sklearn.svm import SVC

    rng = np.random.default_rng(51)
    n = 40
    X = np.vstack([rng.normal([-1.1, -0.6], 0.62, size=(n // 2, 2)),
                   rng.normal([1.3, 1.0], 0.62, size=(n // 2, 2))])
    y = np.r_[-np.ones(n // 2), np.ones(n // 2)]

    xx, yy = np.meshgrid(np.linspace(X[:, 0].min() - .7, X[:, 0].max() + .7, 300),
                         np.linspace(X[:, 1].min() - .7, X[:, 1].max() + .7, 300))
    grade = np.c_[xx.ravel(), yy.ravel()]

    fig, axes = subplots(1, 3, figsize=(7.4, 2.6), sharex=True, sharey=True)
    for ax, C in zip(axes, [100.0, 1.0, 0.05]):
        m = SVC(kernel="linear", C=C).fit(X, y)
        Z = m.decision_function(grade).reshape(xx.shape)
        ax.contour(xx, yy, Z, levels=[-1, 0, 1], colors=["gray", "black", "gray"],
                   linestyles=["--", "-", "--"], linewidths=[0.9, 1.4, 0.9])
        ax.scatter(X[y == -1, 0], X[y == -1, 1], s=16, color=AZUL, zorder=3)
        ax.scatter(X[y == 1, 0], X[y == 1, 1], s=16, color=VINHO, zorder=3)
        sv = m.support_vectors_
        ax.scatter(sv[:, 0], sv[:, 1], s=90, facecolors="none",
                   edgecolors=VERDE, linewidths=1.3, zorder=4)
        larg = 2 / np.linalg.norm(m.coef_)
        ax.set_title(f"$C={C:g}$ — {len(sv)} vetores de suporte\n"
                     f"margem $= {larg:.2f}$", fontsize=7.5)
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        print(f"     [conferência] C={C:g}: {len(sv)} vetores de suporte, "
              f"margem {larg:.3f}")
    salvar(fig, "10-margem")


@figura("10-kernel", "10")
def _kernel():
    """O que o kernel compra: fronteiras que a reta não alcança."""
    from sklearn.svm import SVC
    from sklearn.datasets import make_circles

    X, y = make_circles(n_samples=350, factor=0.42, noise=0.13, random_state=3)
    xx, yy = np.meshgrid(np.linspace(-1.6, 1.6, 320), np.linspace(-1.6, 1.6, 320))
    grade = np.c_[xx.ravel(), yy.ravel()]

    config = [("linear", dict(kernel="linear", C=1.0)),
              ("polinomial, $p=2$", dict(kernel="poly", degree=2, C=1.0, gamma="scale")),
              (r"RBF, $\gamma=0{,}5$", dict(kernel="rbf", gamma=0.5, C=1.0)),
              (r"RBF, $\gamma=50$", dict(kernel="rbf", gamma=50.0, C=1.0))]

    fig, axes = subplots(1, 4, figsize=(7.4, 2.1), sharex=True, sharey=True)
    for ax, (nome, kw) in zip(axes, config):
        m = SVC(**kw).fit(X, y)
        Z = m.decision_function(grade).reshape(xx.shape)
        ax.contourf(xx, yy, Z, levels=[Z.min(), 0, Z.max()],
                    colors=[AZUL, VINHO], alpha=0.10)
        ax.contour(xx, yy, Z, levels=[0], colors="black", linewidths=1.2)
        ax.scatter(X[y == 0, 0], X[y == 0, 1], s=5, color=AZUL, alpha=0.6)
        ax.scatter(X[y == 1, 0], X[y == 1, 1], s=5, color=VINHO, alpha=0.6)
        ax.set_title(f"{nome}\nacurácia (treino) $= {m.score(X, y):.3f}$", fontsize=7.5)
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        print(f"     [conferência] kernel {nome}: acurácia de treino "
              f"{m.score(X, y):.3f}")
    salvar(fig, "10-kernel")


@figura("10-perdas", "10")
def _perdas():
    """hinge, logística e 0-1 como funções da margem y*g(x)."""
    u = np.linspace(-2.5, 3.0, 800)
    fig, ax = subplots(figsize=(4.8, 3.1))
    ax.plot(u, np.where(u < 0, 1.0, 0.0), color=CINZA, lw=1.6,
            label=r"0--1: $\mathbb{1}\{y\,g<0\}$")
    ax.plot(u, np.maximum(0, 1 - u), color=VINHO,
            label=r"hinge: $(1-y\,g)_+$")
    ax.plot(u, np.log2(1 + np.exp(-u)), color=AZUL,
            label=r"logística: $\log_2(1+e^{-y\,g})$")
    ax.axvline(1, color=VERDE, ls=":", lw=1.1)
    ax.axvspan(1, 3.0, color=VERDE, alpha=0.07)
    ax.text(1.55, 1.75, "aqui a hinge é zero:\nnão são vetores de suporte",
            fontsize=7.5, color=VERDE)
    ax.axvline(0, color="black", lw=0.7)
    ax.set_xlabel(r"margem $y\,g(x)$  (positiva $=$ classificou certo)")
    ax.set_ylabel("perda")
    ax.set_ylim(0, 3.0)
    ax.legend(loc="upper right", fontsize=7.5)
    salvar(fig, "10-perdas")


# =========================================================================== #
# Aula 11 --- KNN e Árvores de Classificação
# =========================================================================== #

@figura("11-fronteiras-knn", "11")
def _fronteiras_knn():
    """O k do KNN em classificação: de rendilhado a quase linear."""
    from sklearn.neighbors import KNeighborsClassifier

    rng = np.random.default_rng(61)
    n = 300
    X = np.vstack([rng.normal([-0.9, -0.4], 0.95, size=(n // 2, 2)),
                   rng.normal([1.1, 0.8], 0.95, size=(n // 2, 2))])
    y = np.r_[np.zeros(n // 2), np.ones(n // 2)].astype(int)
    X_te = np.vstack([rng.normal([-0.9, -0.4], 0.95, size=(5000, 2)),
                      rng.normal([1.1, 0.8], 0.95, size=(5000, 2))])
    y_te = np.r_[np.zeros(5000), np.ones(5000)].astype(int)

    xx, yy = np.meshgrid(np.linspace(-4, 4.2, 320), np.linspace(-3.6, 4, 320))
    grade = np.c_[xx.ravel(), yy.ravel()]

    fig, axes = subplots(1, 3, figsize=(7.4, 2.5), sharex=True, sharey=True)
    for ax, k in zip(axes, [1, 15, 120]):
        m = KNeighborsClassifier(n_neighbors=k).fit(X, y)
        Z = m.predict(grade).reshape(xx.shape)
        ax.contourf(xx, yy, Z, levels=[-0.5, 0.5, 1.5], colors=[AZUL, VINHO], alpha=0.11)
        ax.contour(xx, yy, Z, levels=[0.5], colors="black", linewidths=1.0)
        ax.scatter(X[y == 0, 0], X[y == 0, 1], s=6, color=AZUL, alpha=0.65)
        ax.scatter(X[y == 1, 0], X[y == 1, 1], s=6, color=VINHO, alpha=0.65)
        tr = m.score(X, y); te = m.score(X_te, y_te)
        ax.set_title(f"$k={k}$\ntreino ${tr:.3f}$ | teste ${te:.3f}$", fontsize=7.5)
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        print(f"     [conferência] k={k}: acurácia treino {tr:.3f}, teste {te:.3f}")
    salvar(fig, "11-fronteiras-knn")


@figura("11-impureza", "11")
def _impureza():
    """Gini, entropia e erro de classificação como medidas de impureza."""
    p = np.linspace(1e-9, 1 - 1e-9, 800)
    gini = 2 * p * (1 - p)
    entropia = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    erro = np.minimum(p, 1 - p)

    fig, ax = subplots(figsize=(4.8, 3.1))
    ax.plot(p, entropia, color=AZUL, label=r"entropia $-\sum_c p_c\log_2 p_c$")
    ax.plot(p, gini, color=VINHO, label=r"Gini $\;2p(1-p)$")
    ax.plot(p, erro, color=VERDE, label=r"erro de classificação $\min(p,1-p)$")
    ax.axvline(0.5, color=CINZA, ls=":", lw=1.0)
    ax.annotate("nó puro", xy=(0.02, 0.03), xytext=(0.10, 0.30), fontsize=7.5,
                color=CINZA, arrowprops=dict(arrowstyle="->", lw=0.8, color=CINZA))
    ax.annotate("máxima impureza", xy=(0.5, 1.0), xytext=(0.55, 0.72), fontsize=7.5,
                color=CINZA, arrowprops=dict(arrowstyle="->", lw=0.8, color=CINZA))
    ax.set_xlabel(r"$p$ = proporção da classe 1 no nó")
    ax.set_ylabel("impureza")
    ax.set_ylim(0, 1.08)
    ax.legend(loc="lower center", fontsize=7.5)
    salvar(fig, "11-impureza")


# =========================================================================== #
# Aula E1 --- Análise de Agrupamento: k-Médias
# =========================================================================== #

def _nuvens(n, rng):
    centros = np.array([[0, 0], [4.2, 1.0], [1.6, 4.4]])
    y = rng.integers(0, 3, size=n)
    return centros[y] + rng.normal(0, 0.95, size=(n, 2)), y


@figura("E1-lloyd", "E1")
def _lloyd():
    """As iterações do algoritmo de Lloyd, uma a uma."""
    from sklearn.cluster import KMeans

    rng = np.random.default_rng(71)
    X, _ = _nuvens(300, rng)
    # inicialização de propósito ruim, para que haja o que ver nas iterações
    c0 = np.array([[-1.5, -1.2], [-0.9, 0.4], [0.2, -1.8]])

    fig, axes = subplots(1, 4, figsize=(7.4, 2.1), sharex=True, sharey=True)
    cores = [AZUL, VINHO, VERDE]
    centros = c0.copy()
    for passo, ax in enumerate(axes):
        rot = np.argmin(((X[:, None, :] - centros[None, :, :]) ** 2).sum(axis=2),
                        axis=1)
        wcss = sum(((X[rot == k] - centros[k]) ** 2).sum() for k in range(3))
        for k in range(3):
            ax.scatter(X[rot == k, 0], X[rot == k, 1], s=5, color=cores[k], alpha=0.5)
            ax.plot(*centros[k], "X", color=cores[k], ms=9, mec="black", mew=0.8)
        ax.set_title(f"iteração {passo}\nWCSS $= {wcss:.0f}$", fontsize=7.5)
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        print(f"     [conferência] Lloyd, iteração {passo}: WCSS = {wcss:.1f}")
        centros = np.array([X[rot == k].mean(axis=0) if np.any(rot == k)
                            else centros[k] for k in range(3)])
    salvar(fig, "E1-lloyd")


@figura("E1-escolha-K", "E1")
def _escolha_k():
    """Cotovelo e silhueta: duas heurísticas para K."""
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    rng = np.random.default_rng(72)
    X, _ = _nuvens(400, rng)
    Ks = np.arange(1, 11)
    wcss, sil = [], []
    for K in Ks:
        km = KMeans(n_clusters=int(K), n_init=10, random_state=0).fit(X)
        wcss.append(km.inertia_)
        sil.append(silhouette_score(X, km.labels_) if K > 1 else np.nan)
    melhor = Ks[1:][int(np.nanargmax(sil[1:]))]
    print(f"     [conferência] WCSS: {np.round(wcss, 1)}")
    print(f"     [conferência] silhueta máxima em K = {melhor} "
          f"({np.nanmax(sil):.3f}); os dados têm 3 grupos")

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.0, 2.8))
    ax1.plot(Ks, wcss, "o-", color=AZUL, ms=4)
    ax1.plot(3, wcss[2], "o", color=VINHO, ms=9, mfc="none", mew=1.6)
    ax1.annotate("cotovelo", xy=(3, wcss[2]), xytext=(4.4, wcss[2] + 0.30 * wcss[0]),
                 fontsize=8, color=VINHO,
                 arrowprops=dict(arrowstyle="->", lw=0.9, color=VINHO))
    ax1.set_xlabel("$K$"); ax1.set_ylabel("WCSS")
    ax1.set_title("a WCSS nunca sobe --- por isso não\nse pode simplesmente minimizá-la",
                  fontsize=8)
    ax1.set_xticks(Ks)

    ax2.plot(Ks[1:], sil[1:], "s-", color=VINHO, ms=4)
    ax2.axvline(melhor, color=CINZA, ls=":", lw=1.0)
    ax2.set_xlabel("$K$"); ax2.set_ylabel("silhueta média")
    ax2.set_title(f"a silhueta tem máximo (em $K={melhor}$)", fontsize=8)
    ax2.set_xticks(Ks[1:])
    salvar(fig, "E1-escolha-K")


@figura("E1-dendrograma", "E1")
def _dendrograma():
    """Dendrograma e o efeito do linkage."""
    from scipy.cluster.hierarchy import dendrogram, linkage

    rng = np.random.default_rng(73)
    X, _ = _nuvens(40, rng)
    fig, axes = subplots(1, 3, figsize=(7.4, 2.5))
    for ax, met in zip(axes, ["ward", "complete", "single"]):
        Z = linkage(X, method=met)
        dendrogram(Z, ax=ax, color_threshold=0, above_threshold_color=AZUL,
                   no_labels=True)
        ax.set_title(f"linkage {met}", fontsize=8)
        ax.set_ylabel("distância na fusão" if met == "ward" else "")
        ax.grid(False)
    salvar(fig, "E1-dendrograma")


# =========================================================================== #
# Aula E2 --- Redução de Dimensionalidade (PCA e t-SNE)
# =========================================================================== #

@figura("E2-eixos", "E2")
def _eixos():
    """PCA como rotação: os eixos que capturam a variância."""
    rng = np.random.default_rng(81)
    n = 300
    base = rng.normal(size=(n, 2)) * np.array([2.4, 0.55])
    ang = np.deg2rad(32)
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    X = base @ R.T + np.array([1.0, 0.5])
    Xc = X - X.mean(axis=0)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    # Uma direção principal só é definida a menos de sinal; fixamos a convenção
    # de apontar para o lado positivo, senão a seta sai virada para trás.
    Vt *= np.sign(Vt[:, 0])[:, None]
    var = S ** 2 / (n - 1)
    print(f"     [conferência] variância por componente: {var.round(3)}; "
          f"o 1º explica {100*var[0]/var.sum():.1f}%")

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.0, 3.0))
    ax1.scatter(X[:, 0], X[:, 1], s=7, color=CINZA, alpha=0.6)
    m = X.mean(axis=0)
    for j, (cor, rot) in enumerate([(VINHO, "1ª componente"), (AZUL, "2ª componente")]):
        v = Vt[j] * np.sqrt(var[j]) * 2.2
        ax1.annotate("", xy=m + v, xytext=m,
                     arrowprops=dict(arrowstyle="-|>", lw=2.0, color=cor))
        ax1.annotate(rot, xy=m + v * 1.06, fontsize=7.5, color=cor)
    ax1.set_aspect("equal")
    ax1.set_xlabel("$x_1$"); ax1.set_ylabel("$x_2$")
    ax1.set_title("as direções de maior variância", fontsize=8.5)

    Z = Xc @ Vt.T
    ax2.scatter(Z[:, 0], Z[:, 1], s=7, color=CINZA, alpha=0.6)
    ax2.axhline(0, color=AZUL, lw=1.0); ax2.axvline(0, color=VINHO, lw=1.0)
    ax2.set_aspect("equal")
    ax2.set_xlabel("1ª componente"); ax2.set_ylabel("2ª componente")
    ax2.set_title("os mesmos dados, nas novas coordenadas", fontsize=8.5)
    salvar(fig, "E2-eixos")


@figura("E2-compressao", "E2")
def _compressao():
    """Compressão por SVD truncada: quantos componentes bastam."""
    import matplotlib.cbook as cbook
    from matplotlib.image import imread

    with cbook.get_sample_data("grace_hopper.jpg") as f:
        img = imread(f).astype(float).mean(axis=2) / 255.0
    U, S, Vt = np.linalg.svd(img, full_matrices=False)
    total = (S ** 2).sum()
    alvos = [5, 20, 60]

    fig, axes = subplots(1, 4, figsize=(7.4, 2.9))
    axes[0].imshow(img, cmap="gray")
    axes[0].set_title(f"original\n{img.size/1000:.0f} mil números", fontsize=7.5)
    for ax, k in zip(axes[1:], alvos):
        aprox = (U[:, :k] * S[:k]) @ Vt[:k]
        guardado = k * (img.shape[0] + img.shape[1] + 1)
        expl = 100 * (S[:k] ** 2).sum() / total
        ax.imshow(np.clip(aprox, 0, 1), cmap="gray")
        ax.set_title(f"$k={k}$: {100*guardado/img.size:.0f}% dos números\n"
                     f"{expl:.0f}% da variância", fontsize=7.5)
        print(f"     [conferência] k={k}: {100*guardado/img.size:.1f}% do "
              f"armazenamento, {expl:.1f}% da variância")
    for ax in axes:
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    salvar(fig, "E2-compressao")


@figura("E2-variancia", "E2")
def _variancia():
    """Scree plot e variância acumulada, no superconductivity."""
    import pandas as pd
    caminho = os.path.join(RAIZ, "recursos", "dados", "superconductivity.csv")
    X = pd.read_csv(caminho).iloc[:, :-1].to_numpy()
    X = StandardScaler().fit_transform(X)
    var = np.linalg.svd(X, compute_uv=False) ** 2 / (len(X) - 1)
    prop = var / var.sum()
    acum = np.cumsum(prop)
    k90 = int(np.searchsorted(acum, 0.90)) + 1
    print(f"     [conferência] {X.shape[1]} covariáveis; o 1º componente explica "
          f"{100*prop[0]:.1f}%; {k90} componentes chegam a 90%")

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.0, 2.8))
    eixo = np.arange(1, len(prop) + 1)
    ax1.plot(eixo, prop, "o-", color=VINHO, ms=3)
    ax1.set_xlabel("componente"); ax1.set_ylabel("proporção da variância")
    ax1.set_title("scree plot", fontsize=8.5)
    ax1.set_yscale("log")

    ax2.plot(eixo, acum, "o-", color=AZUL, ms=3)
    ax2.axhline(0.90, color=VERDE, ls="--", lw=1.1)
    ax2.axvline(k90, color=CINZA, ls=":", lw=1.0)
    ax2.annotate(f"{k90} componentes\ndos {X.shape[1]} originais", xy=(k90, 0.90),
                 xytext=(k90 + 12, 0.55), fontsize=8,
                 arrowprops=dict(arrowstyle="->", lw=0.9, color=CINZA))
    ax2.set_xlabel("número de componentes")
    ax2.set_ylabel("variância acumulada")
    ax2.set_title("90% da variância", fontsize=8.5)
    ax2.set_ylim(0, 1.03)
    salvar(fig, "E2-variancia")


# =========================================================================== #
# Aula E3 --- NLP + Classificação
# =========================================================================== #

@figura("E3-texto", "E3")
def _texto():
    """A matriz documento-termo é enorme e quase vazia; e o que separa spam."""
    import pandas as pd
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB

    caminho = os.path.join(RAIZ, "recursos", "dados", "spam.csv")
    df = pd.read_csv(caminho, encoding="latin-1").iloc[:, :2]
    df.columns = ["rotulo", "texto"]
    y = (df["rotulo"] == "spam").astype(int).to_numpy()

    vec = CountVectorizer()
    M = vec.fit_transform(df["texto"])
    densidade = M.nnz / (M.shape[0] * M.shape[1])
    print(f"     [conferência] {M.shape[0]} mensagens x {M.shape[1]} palavras; "
          f"{100*y.mean():.1f}% spam; densidade = {100*densidade:.3f}% "
          f"(média de {M.nnz/M.shape[0]:.1f} palavras distintas por mensagem)")

    tf = TfidfVectorizer(min_df=3)
    Xt = tf.fit_transform(df["texto"])
    nb = MultinomialNB().fit(Xt, y)
    peso = nb.feature_log_prob_[1] - nb.feature_log_prob_[0]
    nomes = np.array(tf.get_feature_names_out())
    ordem = np.argsort(peso)
    top_spam, top_ham = ordem[-12:][::-1], ordem[:12]

    fig, (ax1, ax2) = subplots(1, 2, figsize=(7.4, 3.2),
                               gridspec_kw={"width_ratios": [1, 1.25]})
    sub = M[:180, :420].toarray() > 0
    ax1.imshow(sub, cmap="Greys", aspect="auto", interpolation="nearest")
    ax1.set_xlabel(f"palavras (primeiras 420 de {M.shape[1]})")
    ax1.set_ylabel("mensagens (primeiras 180)")
    ax1.set_title("cada ponto é uma palavra presente\ndensidade global: "
                  f"{100*densidade:.2f}%", fontsize=8)
    ax1.grid(False)

    pos = np.arange(12)
    ax2.barh(pos + 0.5, peso[top_spam], height=0.72, color=VINHO, label="indica spam")
    ax2.barh(pos - 12.5, peso[top_ham], height=0.72, color=AZUL, label="indica ham")
    rot = list(nomes[top_spam]) + list(nomes[top_ham])
    ax2.set_yticks(list(pos + 0.5) + list(np.arange(12) - 12.5))
    ax2.set_yticklabels(rot, fontsize=7)
    ax2.axvline(0, color="black", lw=0.8)
    ax2.set_xlabel(r"$\log\widehat{P}(\mathrm{palavra}\mid\mathrm{spam})"
                   r"-\log\widehat{P}(\mathrm{palavra}\mid\mathrm{ham})$")
    ax2.set_title("as palavras mais discriminativas", fontsize=8)
    ax2.legend(loc="lower right", fontsize=7.5)
    salvar(fig, "E3-texto")


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
    ax1.set_xlabel("$p$ (número de covariáveis)")
    ax1.set_ylabel(r"condicionamento de $\bm{X}^\top\bm{X}$".replace(r"\bm", r"\mathbf"))
    ax1.set_title(f"o sistema fica mal-condicionado ($n={n}$)")
    ax1.set_yscale("log")

    ax2.plot(dims, riscos.mean(axis=0), "o-", color=VINHO, ms=3,
             label="risco do MQO")
    ax2.plot(dims, normas.mean(axis=0), "s-", color=AZUL, ms=3,
             label=r"$\|\widehat{\beta}^{\,\mathrm{MQO}}\|_2$")
    ax2.axhline(1.0, color=VERDE, ls="--", lw=1.2,
                label=r"erro irredutível $\sigma^2$")
    ax2.set_xlabel("$p$ (número de covariáveis)")
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
