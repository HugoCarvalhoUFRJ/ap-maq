# Notas para o Claude Code

Material didático do curso de Aprendizado de Máquina (Estatística, Ciências
Atuariais, Matemática Aplicada e Engenharia Matemática). Na branch
`refactoring-baby` o curso é o do **Prof. Gabriel Sanfins, na UFF**; a `main`
guarda a versão do Prof. Hugo Tremonte de Carvalho, na UFRJ. **Não é um
projeto de software**: é um repositório de conteúdo — notas em LaTeX, slides em
HTML, notebooks e dados. Ver `README.md` para a organização geral e `recursos/README.md`
para os materiais transversais.

## Branches

As duas branches são materiais **paralelos e permanentes**, de docentes
diferentes — não etapas de um refactor:

- **`main`** — as aulas do **Prof. Hugo Tremonte de Carvalho**, na estrutura
  antiga, com tudo numa única pasta `materiais-didaticos/`;
- **`refactoring-baby`** — as aulas do **Gabriel Sanfins**, com a reorganização em
  `aulas/` + `recursos/` e as modificações dele. É onde o trabalho acontece.

**Não há plano de merge para a `main`**, e a divergência é deliberada. Não proponha
fundir, rebasear ou "sincronizar com a `main`", nem trate as diferenças entre as
duas como pendência. O nome `refactoring-baby` é enganoso: não é uma branch
temporária.

Vale conferir em qual branch se está antes de assumir caminhos.

## Notas de aula (LaTeX)

**Cada aula tem duas versões, e elas não são rascunho e versão final** — são dois
públicos:

- `NN Título.tex` — **roteiro do docente**: enxuto, com caixas `emsala` que trazem
  as perguntas a fazer à turma e o que dizer. Foi o que existia primeiro.
- `NN Título (alunos).tex` — **versão dos estudantes**: leitura autônoma. Sem
  `emsala`, em tratamento direto ao leitor, com exemplos resolvidos, figuras e as
  passagens que o docente preencheria no quadro. Roda de 1,3 a 1,7 vez o tamanho da
  outra.

Ao editar conteúdo pedagógico, pergunte-se qual das duas o pedido atinge — na
dúvida, as duas. As `(alunos)` carregam o estilo com a opção `aluno`:

```latex
\usepackage[aluno]{../../recursos/latex/estilo-notas}   % versão do aluno
\usepackage{../../recursos/latex/estilo-notas}          % roteiro do docente
```

A opção é retrocompatível: sem ela o `.sty` se comporta exatamente como antes
(conferido compilando as notas do docente com o `.sty` antigo e com o novo — PDFs
idênticos). Ela carrega `tikz`/`pgfplots` e troca o cabeçalho para "Notas de Aula
--- versão do aluno".

A exceção é `aulas/00-planejamento/00 Planejamento.tex`, que tem preâmbulo próprio
e completo e não tem versão para alunos. O `estilo-notas.sty` define a notação do
curso (`\x`, `\X`, `\E`, `\rhat`, `\risco`, `\Dados`, ...), os ambientes de teorema
em português e as três caixas pedagógicas: `emsala`, `ideia` e `atencao`.

**`pgfplots` está em `compat=1.16`** porque é a versão do TeX Live desta máquina;
valores mais novos fazem o pacote abortar com "compat=1.18 is unknown".

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

**Armadilha:** os `.pdf` commitados foram gerados com uma
versão de TeX Live diferente da local. Recompilar qualquer nota — mesmo sem tocar
no `.tex` — produz um PDF com quebras de linha ligeiramente diferentes e, portanto,
um diff. Consequência prática: **não recompile em massa para "conferir"**. Se
precisar (por exemplo, para testar uma mudança no `.sty`), restaure depois com
`git checkout --` os PDFs que você não pretendia alterar. Para comparar duas
compilações, compare o texto extraído (`pdftotext`) de duas compilações **locais**,
nunca uma local contra o PDF commitado.

## Figuras (`recursos/figuras/`)

As figuras das notas dos alunos são geradas por `gerar-figuras.py`; nenhuma foi
copiada dos livros. Uma função por figura, registrada com `@figura("nome", "aula")`:

```bash
python3 recursos/figuras/gerar-figuras.py         # todas (~5 min)
python3 recursos/figuras/gerar-figuras.py 03 07   # só as aulas 03 e 07
```

Três coisas a respeitar:

1. **O script confere os números que as legendas afirmam.** Ele imprime linhas
   `[conferência]` com o que foi medido (viés na fronteira, ganho do QDA sobre o
   LDA, superajuste do boosting...). Se você mudar uma simulação, releia a legenda
   correspondente: vários números estão escritos no `.tex`.
2. **Não use as macros do curso nos rótulos do matplotlib.** `$\x$` é `\x` do
   `estilo-notas.sty`, e o mathtext do matplotlib não a conhece — quebra com
   `ParseFatalException`. Pelo mesmo motivo, nada de `\%`, `\,` ou `\emph{}` em
   strings do matplotlib: eles saem impressos literalmente.
3. **Os parâmetros da população sintética são os mesmos dos notebooks das aulas
   práticas** (`r(x)=sin(1.5x)+0.3x`, `σ=0,7`, `n=50`, `B=500`). Mudá-los
   dessincroniza figura e prática.

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

## Notebooks

**Há um laboratório guiado por aula**, `aulas/NN-*/Aula prática NN.ipynb`, das 14
aulas. Eles seguem a conduta pedagógica dos labs do **[ISLP]** mas *não* usam o
pacote `ISLP` (que não está instalado e não é dependência do curso). Convenções, a
respeitar em qualquer notebook novo:

- `from matplotlib.pyplot import subplots` e API orientada a objeto — **nunca**
  `plt.figure()`;
- `import sklearn.linear_model as skl`, `import sklearn.model_selection as skm`
  (o módulo, não função a função);
- `rng = np.random.default_rng(semente)` em toda simulação;
- nomes iguais aos das notas: `X_tr`, `X_te`, `y_tr`, `y_te`, `modelo`;
- markdown antes de cada célula dizendo **por que** aquilo vem agora;
- commitados **sem outputs** e sem `execution_count`;
- **o notebook explica estatística, não explica as próprias escolhas de estilo** —
  meta-comentário do tipo "seguimos a conduta do [ISLP]" foi explicitamente
  removido pelo Gabriel da versão que ele leu.

**Os blocos `> **Sua vez.**` estão sendo aposentados.** Eles eram um enunciado
seguido de célula de código vazia, e faziam sentido quando a aula prática era o
único material de exercício. Com uma lista prática por aula, o laboratório guiado
passa a **mostrar** em vez de deixar em aberto: cada `Sua vez` vira markdown +
código + leitura do resultado. A **aula prática 01 já foi convertida** (06/08/2026,
quatro blocos); as outras 13 ainda têm 29 blocos e serão convertidas quando o
Gabriel pedir. Não escreva `Sua vez` em notebook novo.

Cada notebook reproduz as simulações da figura correspondente em
`recursos/figuras/gerar-figuras.py`, **com os mesmos parâmetros e a mesma semente**,
para que o número que o aluno lê na nota seja o número que ele obtém na célula. Ao
mexer num dos dois, confira o outro.

Antes de commitar um notebook, rode-o inteiro e confira as afirmações do texto
contra o que as células imprimem — mas **num diretório de saída separado**, para
não gravar as saídas no arquivo do repositório:

```bash
cd aulas/03-validacao-cruzada
jupyter nbconvert --to notebook --execute "Aula prática 03.ipynb" --output-dir /tmp
```

**Armadilha ao abrir um notebook no Jupyter:** salvar grava as saídas e os
`execution_count`, e ainda **reordena as chaves de cada célula** para a ordem
canônica do `nbformat` (`cell_type, execution_count, id, metadata, outputs,
source`). Os notebooks gerados por script estão em outra ordem (`cell_type, id,
metadata, source, execution_count, outputs`), então uma abertura sem edição
nenhuma já produz um diff do arquivo inteiro. Antes de commitar, limpe:

```python
import json
p = "aulas/01-introducao/Aula prática 01.ipynb"
nb = json.load(open(p, encoding="utf-8"))
for c in nb["cells"]:
    if c["cell_type"] == "code":
        c["outputs"], c["execution_count"] = [], None
json.dump(nb, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
```

Isso resolve as saídas; a reordenação fica, e é inofensiva (o JSON é
equivalente). Hoje 40 notebooks estão na ordem do script e 2 na do Jupyter.

Sobraram cinco notebooks herdados de demonstração (`Exemplo - ...`,
`EXTRA K-medias (exemplo)`, `Comparação entre classificadores paramétricos`). Eles
são curtos, estão em estilo antigo e as notas os citam — mas **não** seguem as
convenções acima. Os quatro `Aula prática` herdados foram aposentados; continuam na
`main` e no histórico.

## Listas de exercícios

Além do laboratório guiado, **cada aula tem uma lista para depois da aula**, na
pasta da própria aula, em duas partes e sempre com gabarito:

- `Lista teorica NN.tex` → `Lista teorica NN.pdf` (3–4 exercícios, fácil a
  mediano, todos tratados igual — não há exercício marcado como opcional);
- `Lista teorica NN - gabarito.tex` → o **mesmo conteúdo** com as soluções;
- `Lista prática NN.ipynb` (lacunas marcadas por `...`) e
  `Lista prática NN - gabarito.ipynb`.

O estilo é `recursos/latex/estilo-lista.sty`, que **carrega** o
`estilo-notas.sty` em vez de duplicá-lo — por isso mexer nas listas não obriga a
recompilar nenhuma nota. Ele define `\cabecalholista`, o ambiente `exercicio` e o
ambiente `solucao`.

Quatro armadilhas, todas já pagas uma vez:

1. **Os `.tex` das listas não têm acento no nome, de propósito.** O invólucro do
   gabarito é literalmente `\def\gabaritoopt{gabarito}` seguido de
   `\input{Lista teorica NN.tex}`, e esse `\input` é lido **antes** do
   `\documentclass` — quando o kernel do LaTeX já tratou os bytes UTF-8 como
   ativos mas o `fontenc` ainda não os definiu. Um nome acentuado ali quebra a
   compilação com `Undefined control sequence` em `\UseTextAccent`. Os `.ipynb`
   podem ter acento (não passam por `\input`).
2. **`\begin{solucao}` e `\end{solucao}` precisam ficar sozinhos na linha.** Sem
   a opção `[gabarito]`, quem descarta o corpo é o `comment.sty`, que trabalha
   por linha.
3. **As listas práticas usam semente diferente da aula prática correspondente**,
   para o aluno não copiar o número do laboratório. Consequência: todo número do
   gabarito precisa ser **medido**, não previsto.
4. **Enunciado e gabarito são gerados da mesma fonte** (um script com as lacunas
   marcadas). Editar um dos dois `.ipynb` à mão faz os dois divergirem, e o
   script de conferência acusa.

Como compilar, de dentro da pasta da aula:

```bash
cd aulas/03-validacao-cruzada
pdflatex "Lista teorica 03.tex"
pdflatex "Lista teorica 03 - gabarito.tex"
```

**As 8 listas herdadas saíram desta branch** (seguem na `main` e no histórico).
Elas creditavam o docente anterior, não tinham fonte `.tex` em lugar nenhum e
estavam numeradas pela ordem antiga dos slides — o que fazia 8 das 10 citações
`Para praticar` nas notas apontarem para a lista errada. Com uma lista por aula,
a numeração é 1:1 e essa classe de erro deixa de existir.

## Dados

Os `.csv` ficam em `recursos/dados/`. Os notebooks os carregam com um padrão de
caminho local + fallback para a web:

```python
_local = os.path.join("..", "..", "recursos", "dados", _nome)
_url = "https://raw.githubusercontent.com/HugoCarvalhoUFRJ/ap-maq/refs/heads/refactoring-baby/recursos/dados/" + _nome
_fonte = _local if os.path.exists(_local) else _url
```

**A branch na URL importa.** O fallback (usado no Google Colab) tem de apontar para
`refactoring-baby`: na `main` os `.csv` seguem em `materiais-didaticos/`, não em
`recursos/dados/`, e como não há merge planejado isso não vai mudar — apontar para
`main` dá 404 permanente. Consequência: **renomear a branch quebra o fallback de
todos os notebooks**; se isso acontecer, revise as URLs.

`bank_train_redux.csv` tem ~100 MB e é um excerto reduzido da base do Kaggle, por
limite de espaço do GitHub.

## Convenções

- Mensagens de commit em português, no estilo *conventional commits*
  (`fix:`, `docs:`, `refactor:`).
- Ao mexer em conteúdo pedagógico, confira a coerência com as notas em LaTeX e com
  os dois livros-texto adotados: **[AME]** (Izbicki & Mendonça) é o esqueleto
  teórico, **[ISLP]** (James et al.) fornece intuição e implementação em Python.
- **Os dois livros estão em `recursos/livros/`** e devem ser lidos de fato antes de
  escrever conteúdo, não citados de memória. Extraia com
  `pdftotext -f A -l B recursos/livros/AME.pdf -`. O offset do AME é **+18**
  (página do livro $+$ 18 $=$ página do PDF, conferido em dois pontos); o do ISLP é
  instável, então localize a seção pelo título:
  `pdftotext recursos/livros/ISLP.pdf - | grep -n "Bias-Variance"`.
- **Meça antes de afirmar.** Várias afirmações herdadas não sobreviveram à
  verificação — a variância da validação cruzada não cresce com $k$ neste curso, o
  vazamento por padronização é numericamente irrelevante perto do vazamento por
  seleção de variáveis, e o viés de fronteira do Nadaraya--Watson só aparece se você
  medir sobre repetições em vez de uma amostra. Quando a medição contrariar o texto,
  **registre o que foi medido** em vez de repetir a previsão.

## A hierarquia de vazamento, e por que o PCA saiu da categoria grave

A regra que separa vazamento **grave** de **leve** não é "quanto a etapa aprende
dos dados", é **se ela olha o $Y$**:

- **grave** — selecionar variáveis, hiperparâmetros ou o modelo olhando a resposta.
  Mede-se: com $y$ de ruído puro, isso fabrica $R^2 = +0{,}40$ (aula 07 §3);
- **grave** — a mesma unidade nos dois lados da divisão, ou informação do futuro.
  Nenhum `Pipeline` protege disso; a ferramenta é `GroupKFold` (aula 07 §5);
- **leve** — padronização, imputação pela média e **PCA**. Nenhuma das três vê o
  $Y$, e portanto nenhuma consegue fabricar sinal a partir de ruído.

O PCA estava classificado como grave nas notas E2 e 07. A `Aula prática E2` (§7)
mediu em quatro configurações de $(n,d,k)$ com $y$ de ruído puro: **em nenhuma o
$R^2$ foi inflado** — ele piorou, porque componentes calculados sobre o conjunto
todo não são os componentes ótimos de nenhuma dobra de treino. As duas notas foram
corrigidas em 05/08/2026.

A conduta prática não mudou: tudo isso vai para o `Pipeline`, porque corrigir custa
uma linha. O que mudou é onde gastar vigilância.

## Histórico de correções relevantes

Duas edições foram feitas **diretamente nos HTMLs** e portanto se perdem se alguém
recompilar as apresentações a partir dos `.qmd` (que não estão no repositório).
Quem mantiver os `.qmd` precisa replicar as duas:

1. Os slides das aulas 01 e 03 traziam invertidas as definições de regressão e
   classificação (diziam "Y qualitativa: problema de regressão"). O correto: $Y$
   quantitativa → regressão; $Y$ qualitativa → classificação. Provavelmente está
   uma única vez no fonte, copiado entre as duas apresentações.
2. Em 05/08/2026, o bloco de autoria dos 10 slides passou de
   `Hugo Tremonte de Carvalho` / `hugo@dme.ufrj.br` para `Gabriel Sanfins` /
   `gabrielsanfins@id.uff.br`, com os `id` das duas headings atualizados junto
   (`gabriel-sanfins` e `gabrielsanfinsid.uff.br` — o Quarto derruba o `@`).
   Nenhum link apontava para os `id` antigos.

**`aulas/10-svm/10 SVM - slide.pdf` continua creditando "Hugo Carvalho"** em todas
as páginas, e nomeia a UFRJ na capa. É um PDF compilado (aparentemente Beamer) sem
fonte no repositório — não dá para corrigir sem o `.tex` de origem. É o único
material do curso que ainda traz a autoria antiga.
