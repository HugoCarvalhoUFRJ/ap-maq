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
