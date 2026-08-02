# Notas para o Claude Code

Material didático do curso de Aprendizado de Máquina da UFRJ (Estatística,
Ciências Atuariais, Matemática Aplicada e Engenharia Matemática). **Não é um
projeto de software**: é um repositório de conteúdo — notas em LaTeX, slides em
HTML, notebooks e dados. Ver `README.md` para a organização geral e `recursos/README.md`
para os materiais transversais.

## Branches

O trabalho está em **`refactoring-baby`**. A `main` ainda tem a estrutura antiga,
com tudo numa única pasta `materiais-didaticos/`. A reorganização em `aulas/` +
`recursos/` só existe na branch de trabalho — vale conferir em qual branch se está
antes de assumir caminhos.

## Notas de aula (LaTeX)

14 dos 15 `.tex` carregam o estilo compartilhado:

```latex
\usepackage{../../recursos/latex/estilo-notas}
```

A exceção é `aulas/00-planejamento/00 Planejamento.tex`, que tem preâmbulo próprio
e completo. O `estilo-notas.sty` define a notação do curso (`\x`, `\X`, `\E`,
`\rhat`, `\risco`, `\Dados`, ...), os ambientes de teorema em português e as três
caixas pedagógicas: `emsala`, `ideia` e `atencao`.

Como o caminho do estilo é relativo, **compile de dentro da pasta da aula**:

```bash
cd aulas/01-introducao
pdflatex "01 Introducao.tex"
```

O `00 Planejamento.tex` precisa de **duas passadas** (usa `longtable` + `hyperref`).

Pacotes necessários (Debian/Ubuntu):

```bash
sudo apt install -y texlive-latex-base texlive-latex-recommended \
  texlive-latex-extra texlive-fonts-recommended texlive-pictures lmodern
```

`texlive-latex-extra` é o que traz `tcolorbox` (as caixas pedagógicas), `enumitem`
e `multirow`.

O estilo **não** carrega `babel`/`portugues` — os rótulos em português são
definidos à mão, conforme comentário no `.sty`. Isso é deliberado; não há
hifenização portuguesa.

**Ao editar um `.tex`, recompile o `.pdf` correspondente** e commite os dois: o
`.gitignore` mantém apenas `.tex` e `.pdf`, descartando `.aux`, `.log`, `.out` etc.

## Slides (HTML) — leia antes de editar

Os 11 arquivos `.html` em `aulas/*/` **não foram escritos à mão**. São
apresentações reveal.js geradas pelo **Quarto 1.4.549** (todas na mesma versão),
com as bibliotecas JavaScript embutidas — daí os 3–8 MB por arquivo.

**Os arquivos-fonte `.qmd` não estão no repositório**, nem em nenhuma branch ou
commit do histórico. Ficaram na máquina de quem produziu o material. Consequência
prática: qualquer edição feita diretamente no HTML **é perdida se alguém
recompilar a apresentação a partir do fonte**. Ao alterar um slide, avise quem
mantém os `.qmd` para replicar a mudança lá.

Três armadilhas ao editar esses HTMLs:

1. **Os 11 HTMLs usam CRLF.** Todo o resto do repositório (`.tex`, `.sty`, `.md`,
   `.ipynb`) usa LF. Ao editar por script, preserve as quebras — abra em modo
   binário, ou use `newline=''` em Python. Uma escrita em modo texto converte as
   ~2.700 linhas para LF e transforma uma mudança de uma linha num diff do arquivo
   inteiro.
2. **O conteúdo legível começa por volta da linha 1140.** Tudo antes é CSS e
   JavaScript minificado. Os slides são elementos `<section>`; ler o arquivo
   inteiro estoura o limite de contexto, então busque por trecho.
3. **Os `id` das headings são slugs gerados pelo Quarto** a partir do texto. Ao
   mudar o texto de um título, atualize o `id` junto — mas verifique antes se algum
   link ou índice aponta para o `id` antigo.

## Notebooks e dados

Os `.csv` ficam em `recursos/dados/`. Os notebooks os carregam com um padrão de
caminho local + fallback para a web:

```python
_local = os.path.join("..", "..", "recursos", "dados", _nome)
_url = "https://raw.githubusercontent.com/HugoCarvalhoUFRJ/ap-maq/refs/heads/main/recursos/dados/" + _nome
_fonte = _local if os.path.exists(_local) else _url
```

**Atenção:** esse fallback está quebrado. A URL aponta para `main`, mas na `main`
os `.csv` ainda estão em `materiais-didaticos/`, não em `recursos/dados/` — ou
seja, retorna 404. O caminho local funciona; o fallback (usado no Google Colab) só
voltará a funcionar quando o refactor chegar à `main`. Ao fundir a branch, revise
essas URLs.

`bank_train_redux.csv` tem ~100 MB e é um excerto reduzido da base do Kaggle, por
limite de espaço do GitHub.

## Convenções

- Mensagens de commit em português, no estilo *conventional commits*
  (`fix:`, `docs:`, `refactor:`).
- Ao mexer em conteúdo pedagógico, confira a coerência com as notas em LaTeX e com
  os dois livros-texto adotados: **[AME]** (Izbicki & Mendonça) é o esqueleto
  teórico, **[ISLP]** (James et al.) fornece intuição e implementação em Python.

## Histórico de correções relevantes

Os slides das aulas 01 e 03 traziam invertidas as definições de regressão e
classificação (diziam "Y qualitativa: problema de regressão"). Foi corrigido nos
HTMLs, mas **o erro persiste nos `.qmd` de origem** e provavelmente está uma única
vez lá, copiado entre as duas apresentações. O correto: $Y$ quantitativa →
regressão; $Y$ qualitativa → classificação.
