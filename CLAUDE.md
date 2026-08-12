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
  `aulas/` + `recursos/`. É onde o trabalho acontece, e o nome é enganoso: não é
  uma branch temporária.

**Não há plano de merge**, e a divergência é deliberada. Não proponha fundir,
rebasear ou "sincronizar com a `main`", nem trate as diferenças entre as duas como
pendência.

## Notas de aula (LaTeX)

**Cada aula tem duas versões, e elas não são rascunho e versão final** — são dois
públicos:

- `NN Título.tex` — **roteiro do docente**: enxuto, com caixas `emsala` que trazem
  as perguntas a fazer à turma e o que dizer. Foi o que existia primeiro.
- `NN Título (alunos).tex` — **versão dos estudantes**: leitura autônoma. Sem
  `emsala`, em tratamento direto ao leitor, com exemplos resolvidos, figuras e as
  passagens que o docente preencheria no quadro.

Ao editar conteúdo pedagógico, pergunte-se qual das duas o pedido atinge — na
dúvida, as duas. As `(alunos)` carregam o estilo com a opção `aluno`:

```latex
\usepackage[aluno]{../../recursos/latex/estilo-notas}   % versão do aluno
\usepackage{../../recursos/latex/estilo-notas}          % roteiro do docente
```

A opção carrega `tikz`/`pgfplots` e troca o cabeçalho para "Notas de Aula ---
versão do aluno"; sem ela o `.sty` se comporta como antes.

A exceção é `aulas/00-planejamento/00 Planejamento.tex`, que tem preâmbulo próprio
e completo e não tem versão para alunos. O `estilo-notas.sty` define a notação do
curso (`\x`, `\X`, `\E`, `\rhat`, `\risco`, `\Dados`, ...), os ambientes de teorema
em português e as três caixas pedagógicas: `emsala`, `ideia` e `atencao`.

### A notação da aula 02, que as outras ainda não seguem

Pedido do Gabriel em 10/08/2026, aplicado por ora **só na aula 02** (as duas
versões). Vale para material novo; ao mexer em qualquer outra aula, **veja qual
convenção ela usa antes de escrever**.

- **matriz** — maiúscula, sem negrito, em `\mathbb`: `\mathbb{X}` (delineamento),
  `\mathbb{I}` (identidade). É o que os slides já faziam;
- **vetor** — **minúscula**, em negrito: `\x`, `\bm{y}`, `\bbeta`, `\bm{\alpha}`.
  Maiúscula ficou reservada a matriz, então `\X` e `\bm{Y}` saíram da aula 02 —
  a macro `\X` do estilo continua existindo para as outras 13;
- **escalar** — sem negrito: `y_i`, `\beta_j`, `\lambda`, `p`, `n`.

O número de covariáveis é **`p`**, não `d` — nas notas (as duas) e na `Aula
prática 02`. O resto ainda é `d`, medido em 12/08/2026: 457 ocorrências em 34
arquivos `.tex`, as figuras `05-taxas` e `05-vizinho-longe`, que rotulam `$d$`, e
os notebooks das outras aulas. Dentro da própria aula 02 sobraram a `Lista teorica
02` (quatro `$d>n$`) e a `Lista prática 02`.

O motivo do arranjo não era estética: a macro `\X` é `\bm{X}`, e a matriz de
delineamento também era escrita `\bm{X}` — vetor e matriz saíam com o mesmo glifo,
lado a lado na mesma equação da §1.1.

Duas colisões que a convenção cria, ambas correntes na literatura e toleradas:
`p` também aparece como *p*-valor e como densidade `p(\bbeta)`; e `\mathbb` serve
tanto para matriz (`\mathbb{X}`) quanto para conjunto ou operador (`\R`, `\E`).

**O limiar do lasso no caso ortonormal é $\lambda/2$**, não $\lambda$. Sai de
derivar $\|y-\mathbb{X}\beta\|^2 + \lambda\sum_j|\beta_j|$, sem $\frac12$ no RSS —
a mesma convenção que dá $\hat\beta/(1+\lambda)$ para o Ridge. Notas, slide, lista
teórica, `gerar-figuras.py` e notebook estão todos nela.

**`pgfplots` está em `compat=1.16`** porque é a versão do TeX Live desta máquina;
valores mais novos fazem o pacote abortar com "compat=1.18 is unknown".

Como o caminho do estilo é relativo, **compile de dentro da pasta da aula**:

```bash
cd aulas/01-introducao
pdflatex "01 Introducao.tex"
```

O `00 Planejamento.tex` precisa de **duas passadas** (usa `longtable` + `hyperref`).

Pacotes necessários (Debian/Ubuntu) — o `-extra` é o que traz `tcolorbox`, das
caixas pedagógicas:

```bash
sudo apt install -y texlive-latex-base texlive-latex-recommended \
  texlive-latex-extra texlive-fonts-recommended texlive-pictures lmodern
```

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
código + leitura do resultado. Já foram convertidas a **aula prática 01**
(06/08/2026, quatro blocos) e a **02** (10/08/2026, três); as outras 12 ainda têm
**33 blocos** e serão convertidas quando o Gabriel pedir. Não escreva `Sua vez` em
notebook novo.

Ao converter, **meça antes de escrever**: em três dos sete blocos já convertidos o
resultado contrariou a pergunta do enunciado, e um deles precisou de repetições e
erro-padrão para não afirmar bobagem.

As **listas práticas e seus gabaritos** têm outros **46 blocos** `Sua vez`, em 28
notebooks. Ali eles talvez façam sentido, já que a lista é o material de exercício
— não os converta sem perguntar ao Gabriel.

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

**Rode no ambiente do Gabriel, não no `python3` do sistema.** O interpretador
padrão desta máquina tem scikit-learn 1.3; o dele é o conda `barennet_env`, com
1.9 — e a versão velha esconde quebras que os alunos veriam:

```bash
/home/exxon-lp-003/anaconda3/envs/barennet_env/bin/jupyter nbconvert \
  --to notebook --execute "Aula prática 02.ipynb" --output-dir /tmp
```

Isso já pegou uma quebra real: `LassoCV` e `ElasticNetCV` perderam o parâmetro
`n_alphas` no scikit-learn 1.7, e a aula prática 02 parava no meio. Omitir o
parâmetro usa o padrão de 100 alphas e funciona em qualquer versão. Cuidado para
não "corrigir" demais: o `Lasso.path` é outra função, ainda aceita `n_alphas`, e a
aula 02 o usa na §5. Uma varredura dos argumentos de **todas** as chamadas do
scikit-learn em **todos** os notebooks contra as assinaturas da 1.9 não achou outro
caso (10/08/2026) — mas ela cobre nome de parâmetro, não mudança de comportamento
padrão, que altera número sem levantar erro. O `requirements.txt` registra isso.

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

Isso resolve as saídas; a reordenação fica, e é inofensiva (o JSON é equivalente).

Sobraram cinco notebooks herdados de demonstração (`Exemplo - ...`,
`EXTRA K-medias (exemplo)`, `Comparação entre classificadores paramétricos`). Eles
são curtos, estão em estilo antigo e as notas os citam — mas **não** seguem as
convenções acima. Os quatro `Aula prática` herdados foram aposentados; continuam na
`main` e no histórico.

## Listas de exercícios

Além do laboratório guiado, **cada aula tem uma lista para depois da aula**, na
pasta da própria aula e sempre com gabarito: `Lista teorica NN.tex` (3–4
exercícios, nenhum marcado como opcional) e `Lista prática NN.ipynb` (lacunas
marcadas por `...`), cada uma com seu `- gabarito`. O gabarito teórico é o
**mesmo conteúdo**, com as soluções ligadas por uma opção.

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
   marcadas), **e esse script não está no repositório** — como os `.qmd` dos
   slides, ficou na máquina de quem produziu o material. Mexer nos dois `.ipynb`
   à mão exige fazê-lo no mesmo passo e conferir que só divergem nas lacunas.

Como compilar, de dentro da pasta da aula:

```bash
cd aulas/03-validacao-cruzada
pdflatex "Lista teorica 03.tex"
pdflatex "Lista teorica 03 - gabarito.tex"
```

**As 8 listas herdadas saíram desta branch** (seguem na `main` e no histórico):
creditavam o docente anterior, não tinham fonte `.tex` e estavam numeradas pela
ordem antiga dos slides. Com uma lista por aula, a numeração é 1:1.

## Dados

**Os notebooks não baixam dados da rede, e os `.csv` ficam numa cópia única em
`recursos/dados/`.** A decisão passou por três rodadas e fechou em 10/08/2026:
os alunos recebem o notebook e o `.csv`, e **podem não ter o repositório**. O
padrão para qualquer notebook novo ou revisado é procurar em dois lugares:

```python
import os

_nome = "superconductivity.csv"

# procura em dois lugares, sem baixar nada da internet: a pasta deste
# notebook primeiro ou então ../../recursos/dados/
_lugares = [_nome, os.path.join("..", "..", "recursos", "dados", _nome)]
_caminho = next((c for c in _lugares if os.path.exists(c)), None)

if _caminho is None:
    raise FileNotFoundError(...)     # dizendo onde procurou

df = pd.read_csv(_caminho)
```

A ordem importa: a pasta do notebook vem **primeiro**, então um `.csv` posto ao
lado vence o do repositório. **Nada de URL para o GitHub** — falhar com mensagem
clara é preferível a baixar pelas costas do aluno.

Por que não só a pasta da aula: `superconductivity.csv` tem 23 MB e é lido por 10
notebooks; uma cópia por pasta custaria ~230 MB. Por que não só `recursos/dados/`:
sem o repositório esse caminho nunca resolve, e o aluno teria de editar a primeira
célula em toda aula. As duas tentativas anteriores foram essas, nessa ordem.

**A migração terminou em 12/08/2026**: os 17 notebooks que carregam `.csv` usam
essa célula, byte a byte igual a menos do nome do arquivo. Nenhum baixa nada da
rede, e nenhuma URL do GitHub sobrou no repositório — antes havia um *fallback*
para `raw.githubusercontent`, que amarrava o material ao nome da branch.

Quem **carrega** o quê, medido em 12/08/2026 (a contagem anterior era por menção
ao nome do arquivo, e somava dois notebooks que só o citam no texto — a `E2` e a
`Aula prática 11`):

| arquivo | tamanho | notebooks |
| --- | --- | --- |
| `superconductivity.csv` | 23 MB | 10 — aulas 01 a 06, incluindo as listas 02 e 06 |
| `bank_train_redux.csv` | 96 MB | 4 — aulas 07 e 09, incluindo a lista 09 |
| `spam.csv` | 0,5 MB | 3 — aula E3, incluindo a lista |

`bank_train_redux.csv` é um excerto reduzido da base do Kaggle, por limite de
espaço do GitHub — atenção ao teto de 100 MiB por arquivo se alguma conversão for
duplicá-lo.

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
mediu quatro configurações de $(n,d,k)$ com $y$ de ruído puro e **em nenhuma o
$R^2$ foi inflado** — ele piorou, porque componentes calculados sobre o conjunto
todo não são os ótimos de nenhuma dobra de treino. As duas notas foram corrigidas
em 05/08/2026.

A conduta prática não mudou: tudo isso vai para o `Pipeline`, porque corrigir custa
uma linha. O que mudou é onde gastar vigilância.

## Histórico de correções relevantes

Feitas **diretamente nos HTMLs**, e portanto perdidas se alguém recompilar a partir
dos `.qmd`. Quem mantiver os `.qmd` precisa replicar todas:

1. Os slides das aulas 01 e 03 traziam invertidas as definições de regressão e
   classificação. O correto: $Y$ quantitativa → regressão; $Y$ qualitativa →
   classificação.
2. Em 05/08/2026, a autoria dos 10 slides passou de `Hugo Tremonte de Carvalho` /
   `hugo@dme.ufrj.br` para `Gabriel Sanfins` / `gabrielsanfins@id.uff.br`, com os
   `id` das duas headings atualizados junto (`gabriel-sanfins` e
   `gabrielsanfinsid.uff.br` — o Quarto derruba o `@`).
3. Em 10/08/2026, `[ITSL]` virou `[ISLP]` em **14 citações de seis decks** (01, 02,
   03, 06, 08 e o EXTRA de k-médias). É o mesmo livro.
4. Em 10/08/2026, três correções no deck da aula 02: saiu um slide vazio entre
   "Além da linearidade" e a capa de "Regularização"; o argmin do MQO passou a ser
   repetido no segundo membro, que igualava um argmin a uma norma; e o limiar do
   lasso virou $(|\hat\beta| - \lambda/2)_+$.
5. Em 12/08/2026, as três legendas do deck de k-médias trocaram de número de
   figura: 10.5, 10.6 e 10.7 viraram **12.7, 12.8 e 12.9**. No ISLP o capítulo de
   não supervisionado é o 12; o 10 é *Deep Learning*. Os capítulos 2 a 9 não
   mudaram entre as edições, então as outras sete citações do curso (2.2, 2.9,
   4.6, 4.9, 5.5, 6.7 e 8.3) seguem válidas.

**Falta o fonte do `aulas/10-svm/10 SVM - slide.pdf`.** Ele credita "Hugo Carvalho"
nas 31 páginas e nomeia a UFRJ na capa — é o único material do curso que ainda traz
a autoria antiga —, e não dá para corrigir um PDF compilado. O que pedir ao Hugo: o
`.tex` de um Beamer de 31 slides, título "SVM", compilado com pdfTeX 1.40.21.
Quando chegar: trocar autoria e instituição, recompilar, commitar `.tex` e `.pdf`
juntos.
