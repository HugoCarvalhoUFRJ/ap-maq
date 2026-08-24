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

### A notação

**O número de covariáveis é `p`**, em todo o curso — notas, listas, slides,
notebooks e figuras. A migração do `d` terminou em 12/08/2026 e são 629 trocas em
54 arquivos.

Três papéis do `d` **sobreviveram de propósito**, e nenhum deles é dimensão:

- **distância** `d(\X_i,\x)` na aula 04 e `d^2(\x_i,\x_j)` na E1. A migração até
  ajudou aqui: antes `d` era dimensão *e* distância na mesma página da aula 05. (A
  versão ao quadrado saiu da 04 em 24/08/2026, junto com a tabela de núcleos.);
- **índice**: `d_j` é valor singular na E2, `d_1` é documento na E3, `d^k_{\x}` é a
  k-ésima distância na 04;
- **diferencial** `\,d\x`, na aula 08.

Nas **notas da aula 02** vale, além disso, uma convenção de forma que as outras
aulas não seguem:

- **matriz** — maiúscula, sem negrito, em `\mathbb`: `\mathbb{X}` (delineamento),
  `\mathbb{I}` (identidade). É o que os slides já faziam;
- **vetor** — **minúscula**, em negrito: `\x`, `\bm{y}`, `\bbeta`, `\bm{\alpha}`;
- **escalar** — sem negrito: `y_i`, `\beta_j`, `\lambda`, `p`, `n`.

O motivo do arranjo não era estética: a macro `\X` é `\bm{X}`, e a matriz de
delineamento também era escrita `\bm{X}` — vetor e matriz saíam com o mesmo glifo,
lado a lado na mesma equação da §1.1.

**Ela não foi estendida às outras aulas, e não deve ser.** Nas aulas 04, 05 e 08 a
maiúscula distingue **vetor aleatório de realização** — `\E[(\rhat(\X)-r(\X))^2]`
contra `d(\X_i,\x)` —, e "maiúscula só para matriz" apagaria essa distinção, que é
o que sustenta a teoria da aula 05. A macro `\X` do estilo existe para isso, e é
usada em 19 arquivos.

**A indicadora é `\mathbf{1}`, não `\mathbb{1}`.** A fonte blackboard-bold da AMS
(`msbm10`) só tem as maiúsculas A–Z: o dígito `1` não existe nela, e o slot
correspondente guarda o `\nVdash`. Escrever `\mathbb{1}` compila **sem aviso** e
imprime **⊮**, que não denota indicadora nenhuma. A macro `\1` do estilo carregava
esse defeito e foi corrigida em 24/08/2026; a troca atingiu 11 arquivos das aulas
02, 04, 08, 09, 10 e 11.

Duas alternativas foram descartadas por colisão: `\mathbb{I}` é a matriz identidade
na aula 02, e `I(\cdot)` --- que é justamente o que **AME e ISLP usam** --- colidiria
com o `I` do número de funções da base, na §2 da aula 04. O 1 vazado de verdade
(`\mathds{1}` do `dsfont`, `\mathbbm{1}` do `bbm`) exigiria `texlive-fonts-extra`,
que não está na lista de pacotes desta página --- e nenhum dos dois está instalado.

Duas colisões que a convenção cria, ambas correntes na literatura e toleradas:
`p` também aparece como *p*-valor e como densidade `p(\bbeta)`; e `\mathbb` serve
tanto para matriz (`\mathbb{X}`) quanto para conjunto ou operador (`\R`, `\E`).

**No código dos notebooks, a dimensão continua sendo `d`.** Ali o nome `p` já é
probabilidade — o que `predict_proba` devolve, o argumento `p=` do `rng.choice`, o
`gini(p)` da aula 11 —, em 14 dos 26 notebooks que têm uma variável de dimensão.
Renomear exigiria mexer em 116 usos de `p` para abrir espaço, e trocaria uma
colisão por outra. Decisão do Gabriel em 12/08/2026: o markdown diz `p`, a célula
diz `d`. A exceção é a `Aula prática 02`, onde não há probabilidade nenhuma e o
código já usa `p`, igual ao texto.

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

## A aula 04 perdeu Nadaraya--Watson e a regressão polinomial local

Decisão do Gabriel em 24/08/2026. A aula 04 vai de "o que é um método não
paramétrico" a *splines*, KNN e suavizadores lineares --- e para aí. **Não
reintroduza o Nadaraya--Watson nem a regressão local**, nem "para completar" uma
referência do AME que os cite.

O corte não foi só nas notas, porque o assunto estava espalhado:

| onde | o que saiu |
| --- | --- |
| notas, as duas versões | §4 (NW, tabela de núcleos, leitura como MQ ponderado) e §5 (polinomial local, viés de fronteira); 5→3 e 7→4 páginas |
| `Aula prática 04.ipynb` | §5, §6 e §7 --- 26 células; as antigas §8 e §9 viraram §5 e §6 |
| `Lista teorica 04.tex` | os exercícios 2 e 3; sobraram 2 |
| `Lista prática 04.ipynb` | reescrita inteira --- ver adiante |
| `gerar-figuras.py` | `_nucleos`, `_fronteira` e os auxiliares `_nucleo_gauss`, `_nadaraya_watson`, `_linear_local` |
| `recursos/figuras/` | `04-nucleos.pdf` e `04-fronteira.pdf`, apagadas --- a aula 04 tem **uma** figura, `04-knn-k` |

E em sete lugares fora da aula 04, que citavam o método de passagem ou dependiam
dele: a `Lista teorica 05` (o item (d) do Ex. 3 mandava literalmente "ligue este
exercício ao Exercício 3 da Lista Teórica 04"), a `Lista prática 05 - gabarito`, as
duas versões das notas da 05, a `Aula prática 05`, as notas da E2 e a
`Aula prática 03`. O `00 Planejamento.tex` teve a ementa da aula 04 reescrita.

**O deck nunca teve o assunto** --- ele vai de KNN direto para a maldição da
dimensionalidade ---, então lá não havia o que remover. Cuidado com o inverso: um
slide novo sobre `weights='distance'` chegou a apontar para o Nadaraya--Watson como
continuação natural, e teve de ser desfeito.

Ao citar o AME, lembre que **§5.2 se chama literalmente "k Vizinhos Mais Próximos e
Regressão Linear Local"**. As leituras recomendadas passaram a glosar a parte que
interessa ("o KNN sob redundância") em vez de reescrever o título do livro.

**A citação de Von Neumann sobre o elefante saiu junto**, das duas versões das notas
e da `Aula prática 04`. De quebra, as notas do docente chamavam de "Figura
``elefante'' do [AME] (§3.9)" algo que não existe: §3.9 tem a **Figura 3.8**
(relação entre paramétricos penalizados e não paramétricos), e o elefante é a
*epígrafe* do Capítulo 4. Corrigido para `Figura~3.8`.

### A `Lista prática 04` reescrita

Três exercícios, cobrindo o que sobrou (§2, §3 e §4 das notas), todo número medido
na semente 2026:

1. **cada nó compra um grau de liberdade** --- base truncada contra uma cúbica
   *independente* por pedaço: 7 parâmetros contra 16, saltos de $g$, $g'$ e $g''$
   nos nós de $10^{-9}$ contra até $160$, e a irrestrita ajusta **melhor o treino**
   (0,4111 × 0,5444) e é **16× pior contra $r$** (3,5712 × 0,2233);
2. **o $k$ por validação cruzada** --- o único exercício que sobreviveu ao corte,
   sem a comparação com o NW. A CV escolhe $k=5$; contra $r$, $0{,}1236$;
3. **o KNN é um suavizador linear (e o que isso não garante)** --- monta $\bm H$,
   confere $\operatorname{tr}(\bm H)=n/k$, e mede que **o atalho do LOOCV da Aula 03
   não vale para o KNN**: erra 27% em $k=2$, e para lados opostos conforme $k$
   (razão $1{,}274$ em $k=2$, $0{,}989$ em $k=10$), então nem como cota serve. O
   motivo é que tirar $x_i$ muda *quem são* os $k$ vizinhos --- entra o
   $(k{+}1)$-ésimo ---, e não só reescala pesos. É o par prático do exercício
   teórico que sobreviveu na `Lista teorica 04`.

**O script que gera o par enunciado/gabarito não está no repositório**, como o das
outras listas e os `.qmd` dos slides. Se for mexer nos dois `.ipynb`, faça no mesmo
passo e confira que só divergem nas lacunas.

## Figuras (`recursos/figuras/`)

As figuras das notas dos alunos são geradas por `gerar-figuras.py`; nenhuma foi
copiada dos livros. Uma função por figura, registrada com `@figura("nome", "aula")`:

```bash
python3 recursos/figuras/gerar-figuras.py         # todas (~5 min)
python3 recursos/figuras/gerar-figuras.py 03 07   # só as aulas 03 e 07
```

Três coisas a respeitar:

1. **O script confere os números que as legendas afirmam.** Ele imprime linhas
   `[conferência]` com o que foi medido (a decomposição viés--variância fechando na
   precisão de máquina, o ganho do QDA sobre o LDA, o superajuste do boosting...).
   Se você mudar uma simulação, releia a legenda correspondente: vários números
   estão escritos no `.tex`.
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
   link ou índice aponta para o `id` antigo. O menu lateral (`slide-menu`) é montado
   em tempo de execução a partir do DOM, então um slide novo entra nele sozinho.
4. **O slide não rola, e o que passa do fim é cortado em silêncio.** Nos decks os
   slides de tópicos vão até ~450 caracteres de texto visível (o campeão do deck 04
   tem 453); um slide novo com 525 teve o fim invisível, sem aviso nenhum. O escape
   do próprio Quarto é `class="slide level2 scrollable"`, que os decks usam nos
   slides com tabela grande — mas para lista de tópicos, encurtar é melhor que rolar.

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
- **nada de macro do curso no markdown**: `\x`, `\bm`, `\rhat` e `\1` são do
  `estilo-notas.sty`, e o MathJax do Jupyter não as conhece --- use `\mathbf{}` e
  escreva o resto por extenso. É a armadilha do mathtext do matplotlib um andar
  acima, e ela é silenciosa: o `.tex` compila, o notebook renderiza torto;
- commitados **sem outputs** e sem `execution_count`;
- **o notebook explica estatística, não explica as próprias escolhas de estilo** —
  meta-comentário do tipo "seguimos a conduta do [ISLP]" foi explicitamente
  removido pelo Gabriel da versão que ele leu.

**Os blocos `> **Sua vez.**` acabaram nas 14 aulas práticas** (12/08/2026). Eles
eram um enunciado seguido de célula de código vazia, e faziam sentido quando a aula
prática era o único material de exercício. Com uma lista prática por aula, o
laboratório guiado **mostra** em vez de deixar em aberto: cada bloco virou markdown
+ código + leitura do resultado. Não escreva `Sua vez` em notebook novo.

Foram 40 blocos ao todo, e **meça antes de escrever** não é conselho de estilo: em
mais de um terço deles o resultado contrariou o que o enunciado sugeria. A árvore
gananciosa precisa de profundidade 6, não 3, para o `sinal(x1x2x3)`; o desvio-padrão
da CV continuava caindo com $k$ mesmo em $n=200$ (medição removida do material em
19/08/2026 — ver adiante); ficar com as 5 colunas mais correlacionadas piora o KNN
*e* a Ridge; o t-SNE com `init="pca"` é reprodutível; e
acrescentar comprimento e dígitos ao filtro de spam melhora a AUC e **piora** a AP.
Um bloco precisou de repetições e erro-padrão para não afirmar bobagem.

### As medições dos 40 blocos, e o que elas cobraram do resto do material

Em 17/08/2026 as 40 medições foram conferidas contra as notas (as duas versões), as
listas teóricas e seus gabaritos, as listas práticas e os 11 decks. **Toda medição
nova é uma afirmação nova sobre o curso, e ela precisa passar por aí** — o notebook
corrigido ao lado de uma nota que diz outra coisa é pior que os dois errados juntos.

Três colisões saíram dessa varredura e estão corrigidas:

- a `Lista teorica E2` dizia que o t-SNE "nem sequer é determinado de forma única
  (rodar de novo com outra semente dá outro mapa)". **O `init` padrão do `TSNE`
  virou `"pca"` na versão 1.2 do scikit-learn**, e os trechos de código das notas
  omitem o `init` — então recebem `"pca"` e ficam determinísticos. Só com
  `init="random"` a frase vale, e mesmo aí 92,6% das vizinhanças se preservam. Os
  `lstlisting` passaram a trazer o `init` explícito;
- quatro lugares afirmavam que um modelo com $n$ parâmetros para $n$ pontos
  interpola com resíduo nulo. É verdade em aritmética exata, e a `Lista teorica 03`
  nomeia justamente o caso que a `Aula prática 03` §3 mede — grau 49 em 50 pontos —
  onde o medido é $0{,}1029$: a matriz perde posto numérico e o `lstsq` devolve a
  solução de norma mínima. Só a analogia com o polinômio precisou de ressalva; o RSS
  zero da árvore com uma observação por folha é exato também no computador;
- a caixa da aula 07 dividia os métodos em duas categorias e são **três**: LDA, QDA
  e Bayes ingênuo também são invariantes por reescala, e justamente *porque* estimam
  a covariância.

**O grau 49 da aula 03 não tem um número, tem uma faixa** (medido em 19/08/2026). Os
três valores que o §3 afirmava — erro de treino $0{,}3049$, EQM de teste $25{,}5$ e
mergulho a $-109$ — vieram todos de uma execução coerente, mas em uma instalação que
truncava o posto em $10^{-6}$ relativo. No ambiente atual (scikit-learn 1.5.1, scipy
1.13.1) o `lstsq` trunca na precisão da máquina, enxerga posto 39 em vez de 21, e os
mesmos três números viram $0{,}1029$, $2{,}5\times10^{13}$ e $-1{,}05\times10^{8}$ —
o do teste, doze ordens de grandeza acima. **Não trate nenhum deles como estável**:
variando só o corte de posto de $10^{-6}$ à precisão da máquina, o EQM de teste
percorre de $25$ a $2{,}5\times10^{13}$. O que sobrevive a qualquer corte, e é o que o
texto deve sustentar, são as três leituras: o erro de treino não é zero, é menor que o
do grau 5, e o ajuste é catastrófico fora dos pontos. O notebook, as notas do aluno e
a `Lista teorica 03` já trazem a ressalva.

**A variância da CV contra $k$ saiu do material** (19/08/2026). O deck da aula 03 ---
que é o que os alunos veem --- ensina o argumento clássico: $k$ grande dá dobras
muito correlacionadas e portanto estimativa de variância alta. As notas o
contradiziam com medição (o desvio-padrão caía de $2{,}20$ em $k=2$ a $0{,}13$ na
LOOCV, e continuava caindo com $n=200$), e a `Aula prática 03` media isso numa seção
própria. **Decisão do Gabriel: alinhar ao deck.** Saíram a caixa
`o que a medição mostra` das duas versões das notas, a `emsala` que encenava a
contradição em aula, a seção do notebook e a curva de desvio-padrão da figura
`03-escolha-k` --- que hoje mostra só o viés e o custo. O que ficou é o viés, que
não contradiz nada: $0{,}427$ em $k=2$, $0{,}0064$ em $k=10$. A medição antiga está
no histórico do git, não no material.

E cinco resultados que só existiam no notebook viraram caixa nas notas: a
profundidade que a miopia gananciosa cobra (06), o expoente empírico depender da
janela de $n$ (05), o corte por custo não cortar nada em modelo descalibrado (11), a
silhueta e a compressão discordarem por um fator de dez (E1), e a AP descer enquanto
a AUC sobe (E3).

**Conferido e correto — não reabra:** o `C` da aula 10 (as notas já trazem a
convenção de orçamento do [ISLP] e a inversão do scikit-learn em caixas vizinhas), o
PCA e o KNN na E2 (as notas já dizem que o KNN se adapta sozinho à dimensão
intrínseca) e o Gini contra o erro na 11. Nesses o errado era só o enunciado antigo
do bloco. (O viés de fronteira da 04 também estava conferido, mas o assunto saiu do
curso em 24/08/2026 --- ver a seção da aula 04, adiante.)

As **listas práticas e seus gabaritos** têm outros **44 blocos** `Sua vez`, em 26
notebooks (eram 46 em 28 até a `Lista prática 04` ser reescrita, em 24/08/2026).
Ali eles talvez façam sentido, já que a lista é o material de exercício — não os
converta sem perguntar ao Gabriel.

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
aula 02 o usa na §5.

E pegou uma segunda, em 12/08/2026: o **`QuadraticDiscriminantAnalysis` levanta
`LinAlgError`** em vez de avisar quando a covariância de uma classe fica mal
condicionada, e a `Aula prática 08` morria da §8 em diante — as 30 medidas do
`breast_cancer` são colineares o bastante. A correção é `QDA(reg_param=1e-4)`, um
ridge minúsculo na covariância, e ela **muda o resultado**: o QDA sai de empatado
na frente para terceiro lugar, atrás do LDA. O texto foi reescrito sobre o medido.

Uma varredura dos argumentos de **todas** as chamadas do scikit-learn em **todos**
os notebooks contra as assinaturas da 1.9 não achou outro caso (10/08/2026) — mas
ela cobre nome de parâmetro, não exceção nova nem mudança de comportamento padrão,
que é justamente a classe destas duas. Rodar é a única varredura que pega.
O `requirements.txt` registra as duas.

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
exercícios, nenhum marcado como opcional; a 04 é a exceção, com 2 desde
24/08/2026) e `Lista prática NN.ipynb` (lacunas marcadas por `...`), cada uma com
seu `- gabarito`. O gabarito teórico é o
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
  verificação — o vazamento por padronização é numericamente irrelevante perto do
  vazamento por seleção de variáveis, e o atalho do LOOCV da Aula~03 **não vale para
  o KNN**, apesar de ele ser um suavizador linear com $h_{ii}$ bem definido (erra 27%
  em $k=2$; ver a `Lista prática 04`). Quando a medição contrariar o texto,
  **registre o que foi medido** em vez de repetir a previsão.
  Com uma ressalva, registrada na seção das 40 medições: quando o medido contradiz
  o **deck** — que é o que os alunos veem —, o que fazer é decisão do Gabriel, não
  consequência automática da medição. Foi assim com a variância da CV na aula 03.

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
6. Em 21/08/2026, dois slides no deck da aula 04. O que "otimizava outros
   hiperparâmetros" exibia `KNeighborsRegressor(n_neighbors=17, p=1)` como se o `p`
   de Minkowski fosse um achado: em **uma** covariável ele não muda a ordem dos
   vizinhos, as quatro opções empatam em primeiro lugar e o `p=1` impresso é
   desempate por ordem da grade. Prova disso, a figura do slide era **byte-idêntica**
   à do slide anterior. Saíram o `p` da grade, o `p=1` da saída e a figura repetida
   (169 KB); a grade ficou só com `weights`, que é real. E entrou um slide novo antes
   dele, "KNN - os pesos dos vizinhos", explicando `'uniform'` × `'distance'` ---
   que o deck usava sem nunca definir, aqui ou depois.
7. Em 21/08/2026, o agradecimento a Lucas Galdino passou a dizer "da edição de
   2022/02 **desta** disciplina, **então na UFRJ**". Sem isso, com o rodapé já
   apontando para a UFF, a atribuição ficava ambígua.

## O slide de SVM, o único em Beamer

O fonte chegou em 17/08/2026 e a autoria antiga acabou: **não há mais material do
curso creditando o Prof. Hugo**. O que veio foi o `main.tex` do curso inteiro dele
— 137 frames, 3473 linhas, 50 figuras — em que tudo menos SVM estava dentro de dois
`\begin{comment}`. Daí saíram os 30 frames de SVM e as 10 figuras que eles usam;
mais dois frames escritos aqui, e o deck tem 32.

```
aulas/10-svm/
├── 10 SVM - slide.tex        ← 958 linhas, Beamer tema Madrid
├── 10 SVM - slide.pdf        ← 33 páginas, mesmo caminho de antes
└── slide-figuras/            ← as 10 figuras (1,1 MB), via \graphicspath
```

O `.tex` fica ao lado do `.pdf`, como em todo o resto do repositório; só as figuras
ganharam subpasta, para dez `.pdf` soltos não se confundirem com notas. **Compile de
dentro da pasta da aula**, duas passadas, e apague `.nav` e `.snm` junto com os
outros artefatos (o `.gitignore` já os cobre).

Quatro coisas a saber antes de mexer nele:

1. **Ele não usa o `estilo-notas.sty`.** É Beamer com tema Madrid e o preâmbulo do
   Hugo, com as macros dele (`\V`, `\Vg`, `\RR`, `\PP`, `\ds`, `\Hcal`). Nada disso
   conversa com as notas — não tente unificar;
2. **o rodapé de todas as páginas sai de `\author[...]` e `\title[...]`**, as
   chaves *curtas*. É por isso que trocar a autoria foi uma linha, não trinta e
   uma. O título curto também perdeu o "Apredizagem" (faltava o `n`) do original;
3. **`babel` ficou fora, de propósito**, como no `estilo-notas.sty`: sem o
   `texlive-lang-portuguese` o `babel` falha em silêncio e as dez legendas voltam
   para "Figure". Com `\renewcommand{\figurename}{Figura}` compila igual em qualquer
   máquina;
4. **dois defeitos do original foram corrigidos** e não devem voltar: os ambientes
   `withoutheadline`/`withoutbottomline` fechavam cruzados, e `\set\date{SVM}` usava
   um `\set` inexistente — o LaTeX errava, se recuperava, e o `\date{SVM}` passava
   por sorte. Hoje compila com `-halt-on-error` e zero erro.

As citações `[ITSL]` viraram `[ISLP]` (9 no deck), fechando a troca que os outros
seis decks receberam em 10/08/2026. Os oito números de figura que ele cita (9.1 a
9.12) foram conferidos no `recursos/livros/ISLP.pdf` e estão certos — o capítulo 9
não mudou entre as edições.

**Os dois frames novos são sobre o `C`, e nasceram de uma inconsistência do
original.** O deck apresentava $\sum_i \varepsilon_i \le C$ (o orçamento do
[ISLP]) e, na *mesma* moldura, a forma de Lagrange
$\frac12\|\beta\|^2 + C\sum_i \varepsilon_i$ — que é a do `scikit-learn`, em que
o `C` é o peso da penalidade e portanto tudo se inverte. Mesma letra, papéis
opostos, sem aviso: quem lesse os slides concluiria que $\uparrow C$ dá margem
larga e mais vetores de suporte, e a §8 da `Aula prática 10` mede o contrário
($C=0{,}01 \to 92$ vetores; $C=1000 \to 24$). As notas já traziam a inversão numa
caixa `atencao`; agora o slide também.

**O que ficou de fora:** os outros 107 frames do curso do Hugo e 40 figuras. Estão
só no zip que ele enviou, não no repositório.
