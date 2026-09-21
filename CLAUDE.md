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

- **distância** `d(\X_i,\x)` na aula 04 e `d^2(\x_i,\x_j)` na E1. (A
  versão ao quadrado saiu da 04 em 24/08/2026, junto com a tabela de núcleos.);
- **índice**: `d_j` é valor singular na E2, `d_1` é documento na E3, `d^k_{\x}` é a
  k-ésima distância na 04;
- **diferencial** `\,d\x`, na aula 07.

Nas **notas da aula 02** vale, além disso, uma convenção de forma que as outras
aulas não seguem:

- **matriz** — maiúscula, sem negrito, em `\mathbb`: `\mathbb{X}` (delineamento),
  `\mathbb{I}` (identidade). É o que os slides já faziam;
- **vetor** — **minúscula**, em negrito: `\x`, `\bm{y}`, `\bbeta`, `\bm{\alpha}`;
- **escalar** — sem negrito: `y_i`, `\beta_j`, `\lambda`, `p`, `n`.

O motivo do arranjo não era estética: a macro `\X` é `\bm{X}`, e a matriz de
delineamento também era escrita `\bm{X}` — vetor e matriz saíam com o mesmo glifo,
lado a lado na mesma equação da §1.1.

**Ela não foi estendida às outras aulas, e não deve ser.** Nas aulas 04 e 07 a
maiúscula distingue **vetor aleatório de realização** — `\E[(\rhat(\X)-r(\X))^2]`
contra `d(\X_i,\x)` —, e "maiúscula só para matriz" apagaria essa distinção. A macro
`\X` do estilo existe para isso, e é usada em 25 arquivos.

**A indicadora é `\mathbf{1}`, não `\mathbb{1}`.** A fonte blackboard-bold da AMS
(`msbm10`) só tem as maiúsculas A–Z: o dígito `1` não existe nela, e o slot
correspondente guarda o `\nVdash`. Escrever `\mathbb{1}` compila **sem aviso** e
imprime **⊮**, que não denota indicadora nenhuma. A macro `\1` do estilo carregava
esse defeito e foi corrigida em 24/08/2026; a troca atingiu 11 arquivos das aulas
02, 04, 07, 08, 09 e 10.

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
`gini(p)` da aula 10 —, em 14 dos 23 notebooks que têm uma variável de dimensão.
Renomear exigiria mexer em 116 usos de `p` para abrir espaço, e trocaria uma
colisão por outra. Decisão do Gabriel em 12/08/2026: o markdown diz `p`, a célula
diz `d`. As exceções são a `Aula prática 02` e a `Aula prática 04`, onde não há
probabilidade nenhuma e o código já usa `p`, igual ao texto. (A 04 entrou na lista
quando foi reescrita, em 24/08/2026: `experimento_dimensao(p, ks, ...)`,
`size=(n_tr, p)`, `f"p = {p}"`.)

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
dele: as notas da E2 e a `Aula prática 03` --- os outros quatro estavam na antiga
aula 05 de aspectos teóricos, que saiu do curso em 31/08/2026. O `00 Planejamento.tex` teve a ementa da aula 04 reescrita.

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

## A aula 05 saiu do curso, e as seguintes desceram uma posição

Decisão do Gabriel em 31/08/2026. A antiga aula 05 --- *Métodos Não Paramétricos:
Aspectos Teóricos* --- trazia taxas de convergência, maldição da dimensionalidade,
esparsidade e redundância. São conceitos que ele não quer abordar, e a aula saiu
**inteira**: as duas versões das notas, o deck, a `Aula prática 05`, a
`Lista teorica 05`, a `Lista prática 05`, os dois gabaritos, as figuras `05-taxas` e
`05-vizinho-longe` e as duas funções que as geravam.

**As aulas 06 a 11 viraram 05 a 10.** O curso tem hoje **10 aulas oficiais** mais as
três extras; as pastas vão de `00-planejamento` a `10-knn-arvores-classificacao`, e
E1--E3 não mudaram. `Aula 05` significa agora **Árvores de Regressão e Ensembles**.

O caro não foi apagar: foram as **62 referências à aula 05 vindas de outras 12
aulas**. Delas, 33 eram ponteiro puro e saíram sozinhas; 27 tinham a aula 05 como
**sujeito da frase** (``**A seguir.** A Aula 05 explica com teoria...'', ``## 6. E o
KNN? A Aula 05, confirmada'', ``\begin{atencao}[Eis a Aula~05 em ação]''), e nessas
**apagou-se o mínimo, sem escrever nada novo**; e 2 mandavam à `Lista prática 05` a
partir da lista prática da SVM.

**As menções ao conceito ficaram, de propósito.** ``Maldição da dimensionalidade'',
``esparsidade'' e ``redundância'' continuam nomeadas nas aulas 04, 07 e 10 e nas E2 e
E3 --- saiu o ponteiro, não a afirmação. Hoje são vocabulário sem aula dedicada, como
a *descida dupla* na aula 01. **Não as remova** achando que são resíduo, e **não
reintroduza a aula**.

## A aula 05 perdeu boosting, OOB e importância de variáveis

Decisão do Gabriel em 09/09/2026, aplicada em quatro passos numa sessão. A aula 05
--- *Árvores de Regressão e Ensembles* --- vai hoje de árvore a poda, agregação,
*bagging* e florestas aleatórias, e para aí. **Não reintroduza os três**, nem para
"fechar" o Capítulo 8 do [ISLP], que cobre os três.

| onde | o que saiu |
| --- | --- |
| notas, as duas versões | a seção *Boosting* inteira e as subseções *out-of-bag* e *Importância de variáveis*; 258→190 e 431→337 linhas |
| `Aula prática 05` | as seções de *boosting* e de importância, a análise de importância do caso real, e a coluna `R^2 OOB` da escolha de $m$ |
| `Lista prática 05` | o Ex. 4 inteiro e a metade de *boosting* do Ex. 3; 18→13 e 23→16 células |
| `Lista teorica 05` | o item (b) do Ex. 3, que pedia "uma quantidade que o *bagging* fornece de graça" |
| deck | um tópico, no slide "Fechando o *bagging*" |

**O deck quase não tinha o assunto, e isso engana.** Uma busca por `oob` acha 156
ocorrências --- e **todas** estão em JavaScript minificado e em base64 de imagem.
No texto visível, 10.699 caracteres, não há menção nenhuma a OOB, *boosting* ou
XGBoost. Ao auditar um deck, filtre `<script>` e `<img>` antes de contar; a busca
crua mente por duas ordens de grandeza.

**A figura sobreviveu pela metade certa.** A `05-numero-arvores` tinha dois painéis
--- floresta e *boosting* --- e era citada **dentro da seção de Boosting**, então o
corte a levaria inteira. Mas o painel da floresta é o que o Ex. 3 da
`Lista prática 05` reproduz, e esse vínculo é deliberado (ver "Listas de
exercícios"). A geradora foi reduzida a esse painel, a figura regerada, e a citação
**movida para a seção *Florestas aleatórias***, que já afirmava "o risco é robusto
a $B$" sem nada que mostrasse. Os números não se moveram.

**O que ficou, de propósito: a correlação $\rho$ e o piso $\rho\,v$.** Eles saíram
do laboratório --- a §5 dele passou a medir risco contra $B$, direto --- mas
continuam nas notas, numa `observacao` da seção "Por que agregar?", e na
`Lista teorica 05`, cujo Ex. 4 é "o piso da variância". O Ex. 2 da lista prática é
o par medido desse exercício, e por isso ficou também. Se for cortar o $\rho$ um
dia, são os três de uma vez.

## A aula 06 encolheu a lista teórica e trocou de registro

Decisão do Gabriel em 11/09/2026. A `Lista teorica 06` foi de **quatro exercícios
para dois**, e os dois que ficaram foram reescritos num registro mais próximo do
leitor --- com uma pessoa e uma situação em cena, no lugar de uma enumeração
abstrata. A `Aula prática 06` passou pela mesma reescrita.

| onde | o que mudou |
| --- | --- |
| `Lista teorica 06.tex` | saíram os Ex. 2 (``por que um custa 0,40 e o outro custa nada'') e 4 (``a divisão que nenhum pipeline conserta''); 297→199 linhas, 2→1 página de enunciado e 5→3 de gabarito |
| os dois que ficaram | o Ex. 1 virou a revisão do notebook de um colega; o antigo Ex. 3 virou o Ex. 2, e o banco dele ganhou contexto |
| `Aula prática 06.ipynb` | as 31 células de texto reescritas, as 20 de código **intactas**; markdown de 20 para 23 KB |
| `Lista prática 06` (os dois) | quatro ponteiros para os exercícios que saíram, redirecionados |

**Os ponteiros são a parte cara**, como sempre. A lista prática citava o Ex. 2(b),
o Ex. 2(c), o Ex. 3 e o Ex. 4(b) da teórica. Os dois primeiros passaram a apontar
para os itens *leves* do Ex. 1, que é onde o argumento passou a morar; o terceiro
virou Ex. 2 pela renumeração; e o quarto --- a conta de probabilidade do vazamento
por grupo --- ficou sem destino, então a menção saiu e a conta ficou escrita inline
no próprio notebook.

**A tabela ``O que ficou'' existe nos dois `.ipynb` da lista prática.** Ela não é
lacuna, e por isso é fácil corrigir num e esquecer no outro --- foi o que
aconteceu, e o enunciado ficou uma rodada com números que o gabarito já não tinha.
A conferência que pega isso é comparar as duas fontes célula a célula, descartando
as de leitura (as que começam com ``Deve imprimir''), e exigir que **só** difiram
onde há `...`.

### O `GroupKFold` mudou entre versões, e havia número defasado

Achado em 11/09/2026, conferindo o Ex. 3 da `Lista prática 06`. Com grupos de
tamanho igual, o `GroupKFold` atribui grupos a dobras de um jeito na sklearn 1.3 e
de outro na 1.9 --- a 1.9 faz o rodízio limpo, a 1.3 embaralhava. Os dados saem
byte-idênticos; o que muda é a partição, e um $R^2$ perto de zero **troca de
sinal**:

| | KFold | GroupKFold |
| --- | --- | --- |
| o que o gabarito afirmava | $+0{,}6665$ | $+0{,}0341$ |
| sklearn 1.3 (o `python3` do sistema) | $+0{,}6721$ | $+0{,}0372$ |
| sklearn 1.9 (o `barennet_env`) | $+0{,}6697$ | $\mathbf{-0{,}0866}$ |

Corrigido para os valores da 1.9, junto com a narrativa (``o valor honesto é
$-0{,}09$'') e com a afirmação de que as dez dobras mostram ``16 ou 17 pacientes
nos dois lados'' --- uma delas mostra 13. Os Ex. 1, 2 e 4 da mesma lista
reproduzem exatamente, e a `Aula prática 06` §5, que também usa `GroupKFold`,
confere com a 1.9 até a quarta casa. **As outras aulas não foram auditadas.**

### Dois números que o relógio não sustenta

A §8 da `Aula prática 06` afirmava que a busca com `SelectKBest` leva **9,1
segundos** e que a `RandomizedSearchCV` é **45 vezes** mais rápida. Em quatro
rodadas na mesma máquina, a busca variou de $7{,}2$ a $10{,}6$ s e a razão, de
$26\times$ a $48\times$. Viraram ``cerca de dez segundos'' e ``dezenas de vezes'',
com uma linha avisando que tempo de relógio varia. O resto da seção ---
$0{,}8592$, $0{,}8736$, $0{,}8620$, os 1,6% e os 0,3% --- é estável e ficou.

### O `penalty` da `LogisticRegression` foi depreciado

Terceiro caso da família do `n_alphas` e do `QDA`/`LinAlgError`: roda sem erro
hoje e some numa versão futura. O argumento `penalty` foi **depreciado na 1.8 e
sai na 1.10**. Eram quatro ocorrências, todas corrigidas em 11/09/2026:

- `penalty="l2"` é o padrão, então basta **omitir** --- nas duas versões das notas
  da 07, e no gabarito do Ex. 2 da `Lista teorica 06`, que agora explica isso ao
  aluno;
- `penalty=None` vira **`C=np.inf`**, na §7 da `Aula prática 07`. Os coeficientes
  saem bit-idênticos (diferença absoluta máxima $0$), e a leitura da seção ---
  ``$C=1$ encolhe os coeficientes cerca de 10%'' --- continua valendo: $10{,}2\%$.

As três ocorrências da aula 07 saíram em 16/09/2026, junto com a logística, e ela
voltou em 21/09/2026 **sem** o `penalty`: o laboratório usa `C=np.inf` na §7 e as
notas, `C=1.0`. Ver ``A aula 07 segue o deck (e o deck mudou)'', adiante. Sobrou a
ocorrência da `Lista teorica 06`.

**Cuidado ao procurar por este:** os notebooks chamam
`warnings.filterwarnings("ignore")`, então executá-los **não** mostra o aviso. Só
`python -W error::FutureWarning`, fora do notebook, denuncia.

### E depois a `Aula prática 06` encolheu para seguir o deck

Decisão do Gabriel em 14/09/2026, três dias depois da reescrita acima. O
laboratório passou a cobrir **o que o deck cobre, e só isso**: 52 → **23 células**,
de nove seções para cinco. (Toda numeração citada até aqui é a de *antes* deste
corte --- a §5 do `GroupKFold` e a §8 do relógio no laboratório, o Ex. 3 do
`GroupKFold` na lista prática. A correspondência com a de hoje está nas duas
tabelas abaixo.)

| § de hoje | o que faz | de onde veio |
| --- | --- | --- |
| 1 | pacotes | — |
| 2 | quem é sensível à escala | a antiga §2, intacta |
| 3 | $\mu$ e $\sigma$ são aprendidos: o custo de padronizar fora da dobra | a antiga §4, com laço próprio |
| 4 | o `Pipeline` por dentro | a antiga §6 |
| 5 | `Pipeline` $+$ `GridSearchCV` | **nova**, é o slide ``Um exemplo'' |

Saíram a §3 (vazamento por seleção), a §5 (agrupamento e a hierarquia), a §7
(`ColumnTransformer`), a §8 (busca no pré-processamento) e a §9 (o arquivo
quebrado). **Não as reintroduza no laboratório** --- o deck não tem nenhuma delas.

**A `Lista prática 06` foi atrás, no mesmo dia.** Ela espelhava o laboratório
antigo, então foi reescrita para espelhar o novo: 20→**14 células** no enunciado e
25→18 no gabarito, de quatro exercícios para **três**, um por seção do laboratório.

| Ex. de hoje | espelha | mede |
| --- | --- | --- |
| 1 --- quem muda quando a régua muda | §2 | cinco métodos, uma coluna $\times 500$: MQO $0{,}2762$ e árvore $0{,}9384$ nos dois; KNN $0{,}8668 \to 1{,}4527$ |
| 2 --- o custo de padronizar fora da dobra | §3 | $0{,}8594$ contra $0{,}8593$ (o antigo Ex. 2, mantido) |
| 3 --- o `Pipeline` inteiro, e o `GridSearchCV` | §4 e §5 | o scaler bate com o treino e não com o todo; `lasso__alpha` $=0{,}1$, 9 coeficientes de 60 |

Saíram os exercícios de **seleção**, de **agrupamento** e de `ColumnTransformer`.
Com isso, **nenhum notebook do curso mede mais esses dois vazamentos** --- eles
vivem nas notas (texto e Figura~1) e no Ex. 1 da `Lista teorica 06`, onde entram
como caso a classificar. A geradora da figura, essa sim, continua medindo os dois.
As duas versões das notas dizem isso ao aluno com todas as letras, em vez de
mandá-lo a um laboratório que não existe.

**O bloco `Sua vez` foi preservado** (a lista tinha um, no exercício de seleção que
saiu). O novo mede o contraste que o laboratório só afirma em prosa: reescalar a
coluna **relevante** faz o Lasso melhorar $3{,}4\%$; reescalar uma **irrelevante**
faz piorar $3{,}8\%$ --- quem decidiu foi a unidade de medida, não você.

**A armadilha do laço compartilhado.** As antigas §3 e §4 mediam dentro do
**mesmo `for`**, com o mesmo `default_rng(21)` --- que é o que faz o notebook
reproduzir os dois painéis da figura. Tirar a §3 muda o que a §4 sorteia: o
$0{,}8466$ da figura vira $0{,}8436$. Separar os geradores tampouco resolve, porque
aí muda o painel *esquerdo* também ($+0{,}403$ vira $+0{,}446$, $-0{,}693$ vira
$-0{,}740$) --- e o $+0{,}40$ é citado em **sete arquivos**, incluindo as notas da
E2 e este `CLAUDE.md`. Decisão: **a figura e as notas ficam como estão**, e o
laboratório roda com semente própria (`6`), medindo $0{,}8342$ contra $0{,}8341$.
São duas amostras do mesmo experimento, não uma contradição, e a nota do aluno diz
isso com todas as letras.

**A §5 nova reproduz o slide literalmente.** Com `make_regression(n_samples=1000,
n_features=100, n_informative=10, noise=1.0, random_state=0)`, a busca devolve
`Lasso(alpha=0.1)` e `ElasticNet(alpha=0.1, l1_ratio=1)` --- exatamente a saída
impressa no slide ``Um exemplo''. O `l1_ratio=1` colapsa o ElasticNet em Lasso, e os
dois empatam em EQM de CV ($1{,}1293$) e no teste ($1{,}2110$); o teste é pior que a
CV porque o `best_score_` é o melhor de 56 estimativas ruidosas.

## A aula 07 segue o deck (e o deck mudou)

Duas decisões, com cinco dias entre elas, e é preciso ler as duas juntas.

**Em 16/09/2026** o Gabriel decidiu que a aula 07 passaria a cobrir o que o deck
cobre --- no espírito da aula 06 e indo além dela, porque aqui **as notas também**
foram atrás, não só o laboratório e as listas. O deck cobria a formulação com perda
0--1, o classificador de Bayes, o *plug-in*, o Bayes ingênuo (contínuo e discreto,
com as variantes do `scikit-learn`), a normal multivariada, LDA, QDA e a escolha
entre os dois; a regressão logística aparecia nele só como exemplo de *plug-in*, e
por isso saiu de tudo. É o corte que a tabela abaixo registra.

**Em 21/09/2026** ele pediu slides de regressão logística **para o deck** (item 11
do histórico de correções nos HTMLs), e com isso a premissa do corte caiu. A
logística voltou no mesmo dia para as notas, o laboratório, a lista prática e a
figura, alinhada aos slides novos. O que **não** voltou, de propósito: a subseção
``via regressão sobre indicadores'' das notas, que o deck não tem, e a comparação
de escala da antiga §8 do laboratório, que não media nada (adiante) e é assunto da
aula 06.

O princípio continua valendo: **o deck manda**. Se um assunto não estiver nele, não
entre nas notas sem falar com o Gabriel --- e, se ele entrar no deck, o resto da
aula vai atrás.

| onde | o corte de 16/09 | como está hoje |
| --- | --- | --- |
| notas, as duas versões | saíram a seção da logística (MV, separação perfeita, multiclasse), a regressão sobre indicadores e a comparação discriminativo $\times$ generativo; entraram a motivação da perda 0--1, o Bayes ingênuo discreto com as variantes do `scikit-learn`, a densidade normal multivariada, os estimadores de MV, o discriminante do QDA e a conta de parâmetros com $K$ classes | o que entrou ficou; a logística e a comparação voltaram em 21/09. **Só a regressão sobre indicadores continua fora** --- o deck não a tem |
| `Aula prática 07` | saíram a logística das §3, §4 e §8, a §7 inteira (a pegadinha do `C`) e a comparação de escala da §8; 40→34 células | a logística e a §7 voltaram: **37 células**, com o caso real de novo na §8. A comparação de escala continua fora |
| `Lista prática 07` | saiu a logística dos Ex. 2 e 4; entraram o `reg_param` no QDA do Ex. 4 (com lacuna) e um `Sua vez` sobre a covariância comum, no lugar do de AUC, que é aula 08 | a logística voltou aos dois exercícios; o `reg_param` e o `Sua vez` novo ficaram |
| `07-fronteiras` | o painel da logística: 4→3 painéis | de volta a **quatro**, com a legenda de antes |
| fora da aula | saíram os ponteiros à logística ``da aula 07'' na `Lista prática 09`, nas notas da E3 (docente), no planejamento e no `requirements.txt` | os quatro voltaram |

A `Lista teorica 07` não tinha logística e não perdeu exercício, mas foi corrigida
junto. A logística é usada também nas aulas 08, 09, 10, E2 e E3, notas e notebooks;
antes de 21/09/2026 **nenhum deck a desenvolvia**, e ela era usada como ferramenta
já conhecida. Agora o deck da 07 a apresenta.

**O que voltou em 21/09/2026**, alinhado aos slides: a seção das notas (as duas
versões, com o modelo, a interpretação em razão de chances, a MV, a separação
perfeita e o caso multiclasse), a seção ``Discriminativo $\times$ generativo'', o
painel da logística na `07-fronteiras` (de volta a quatro), as §3, §4 e §8 do
laboratório e a §7 inteira (a pegadinha do `C`), os Ex. 2 e 4 da `Lista prática 07`
e os ponteiros do planejamento, da E3 e da `Lista prática 09`. Os números medidos
são os de antes do corte, reconferidos na 1.9: logística $0{,}1230$ de erro na §3,
$+0{,}0032$ na §4, $10{,}2\%$ de encolhimento em $C=1$ na §7 e $0{,}9591$ no teste
da §8.

O que ficou nas notas sem estar no deck, de propósito: a caixa de que a acurácia
engana (a aula 08 abre citando ``o aviso da Aula 07''), a caixa do preço do
``ingênuo'' (a aula 08 cita o motivo do descalibramento) e a observação do que se
transfere da Parte I.

### O que a reescrita derrubou

Tudo medido em 16/09/2026, no `barennet_env`:

- **A `Lista prática 07` quebrava na sklearn 1.9.** O Ex. 4 chamava
  `QuadraticDiscriminantAnalysis()` sem `reg_param` no `breast_cancer`, e os cinco
  ajustes da CV falhavam --- a quebra que o laboratório corrigiu em 12/08, e da qual a
  lista tinha escapado. Com `reg_param=1e-4` o QDA dá $0{,}9508$ (o gabarito dizia
  $0{,}9561$) e segue atrás do LDA. A `Lista prática 10` tinha a mesma chamada, no
  mesmo banco, e foi corrigida em 21/09/2026 (o QDA dela vai de $0{,}9561$ a
  $0{,}9508$ de acurácia, de $0{,}9912$ a $0{,}9894$ de AUC e de $0{,}0398$ a
  $0{,}0434$ de Brier).
- **O QDA da 1.9 recusa classe pequena.** O `fit` compara os autovalores da
  covariância de cada classe com `tol=1e-4` **absoluto** e levanta `LinAlgError`
  quando a classe tem no máximo $p$ observações ou colunas quase colineares. Com
  **menos** observações que covariáveis, nenhum `reg_param` resolve; com
  exatamente $p$, um `reg_param` de $0{,}1$ resolve e um de $10^{-4}$ não. No §6 do
  laboratório e no Ex. 3 da lista, o `try` transforma a recusa em `nan` em $n=20$,
  $p=10$ --- e o gabarito afirmava $0{,}5475$ e ``16 pontos abaixo do LDA'', número da
  sklearn antiga, repetido na tabela da `Lista teorica 07` 3(d). Hoje os três dizem
  que ali o QDA não ajusta, e usam $n=30$ ($+0{,}0392$ para o LDA) para a vantagem.
- **A comparação de escala da antiga §8 do laboratório comparava cada modelo com ele
  mesmo.** Só a logística estava num `Pipeline` com `StandardScaler`; a coluna ``com
  scaler'' de LDA, QDA e Bayes ingênuo era o modelo cru. Medindo de verdade, na mesma
  divisão: o LDA é invariante (o solver `svd` padroniza por dentro), mas o
  `QDA(reg_param=1e-4)` vai de $0{,}9415$ a $0{,}9532$ com o scaler, e o
  `GaussianNB` de $0{,}9240$ a $0{,}9123$ --- o `var_smoothing` é proporcional à maior
  variância, e com `var_smoothing=0` a invariância volta. A caixa das ``três
  categorias'' das notas da aula 06 citava essa medição: a citação saiu e a caixa
  ganhou a ressalva de implementação.
- **Afirmações do laboratório que as próprias células desmentiam:** o Bayes ingênuo
  ``não é o pior da tabela'' (é, com $0{,}1320$, nas sklearn 1.3 e 1.9); a correlação
  ``$-0{,}82$'' (a verdadeira é $-0{,}803$, e a própria célula a imprime; $-0{,}83$ é a
  estimativa do QDA), também no gabarito da lista; ``um centésimo e meio de ponto
  percentual'' para $+0{,}0015$ (são 0,15 p.p.); e o Bayes ingênuo que ``continua onde
  estava'' com covariâncias iguais --- o excesso dele dobra, de $+0{,}0355$ para
  $+0{,}0737$, porque zerar a correlação comum desvia a direção da fronteira em
  $47{,}8$ graus.
- **O caso $p=2$ parecia mudar de uma peça para outra.** O laboratório mede o QDA
  ganhando desde $n=20$; as listas mediam empate. São populações diferentes: a do
  laboratório (e dos Ex. 1--2 da lista) tem correlações $+0{,}75$ e $-0{,}80$ nas
  duas classes; a do Ex. 3 da lista, $-0{,}47$ e $-0{,}45$. A conclusão antiga das
  listas, ``em dimensão baixa a escolha não importa'', era falsa --- o próprio Ex. 2
  mostra o QDA 4 pontos à frente em $p=2$ ---, e a do laboratório, ``é a razão
  $n/p^2$ que governa'', generalizava demais. As peças dizem hoje a mesma coisa:
  $n$ contra $p(p+1)/2$ governa o que o QDA tem a **perder**; o quanto as
  covariâncias diferem, o que ele tem a **ganhar**.
- **No breast_cancer, LDA e QDA empatam dentro do ruído.** O laboratório lia a
  vantagem do LDA no teste ($0{,}0117$, que são **dois** tumores em 171) como ``a conta
  de parâmetros cobrando''; na CV da mesma tabela o QDA fica à frente
  ($0{,}9623$ contra $0{,}9598$). O texto passou a dizer isso.
- **O AME omite o $\tfrac12$ do expoente** nas duas densidades normais da §8.1.4
  (p. 147 e 149 do livro; conferido com `pdftotext -layout`). As notas do aluno
  avisam na leitura recomendada.

## Figuras (`recursos/figuras/`)

As figuras das notas dos alunos são geradas por `gerar-figuras.py`; nenhuma foi
copiada dos livros. Uma função por figura, registrada com `@figura("nome", "aula")`:

```bash
python3 recursos/figuras/gerar-figuras.py         # todas (~5 min)
python3 recursos/figuras/gerar-figuras.py 03 06   # só as aulas 03 e 06
```

Três coisas a respeitar:

1. **O script confere os números que as legendas afirmam.** Ele imprime linhas
   `[conferência]` com o que foi medido (a decomposição viés--variância fechando na
   precisão de máquina, o ganho do QDA sobre o LDA, a floresta estabilizando com
   $B$...). Se você mudar uma simulação, releia a legenda correspondente: vários
   números estão escritos no `.tex`.
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

**Há um laboratório guiado por aula**, `aulas/NN-*/Aula prática NN.ipynb`, das 13
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

**Os blocos `> **Sua vez.**` acabaram nas aulas práticas** (12/08/2026). Eles
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
- a caixa da aula 06 dividia os métodos em duas categorias e são **três**: LDA, QDA
  e Bayes ingênuo também são invariantes por reescala, e justamente *porque* estimam
  a covariância. (Em 16/09/2026 descobriu-se que a medição que sustentava isso, na
  §8 da `Aula prática 07`, comparava cada modelo com ele mesmo. A invariância vale
  para os estimadores de MV; o `var_smoothing` do `GaussianNB` e o `reg_param` do
  QDA a quebram --- ver ``A aula 07 segue o deck (e o deck mudou)''.)

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

**Conferido e correto — não reabra:** o `C` da aula 09 (as notas já trazem a
convenção de orçamento do [ISLP] e a inversão do scikit-learn em caixas vizinhas), o
PCA e o KNN na E2 (as notas já dizem que o KNN se adapta sozinho à dimensão
intrínseca) e o Gini contra o erro na 10. Nesses o errado era só o enunciado antigo
do bloco. (O viés de fronteira da 04 também estava conferido, mas o assunto saiu do
curso em 24/08/2026 --- ver a seção da aula 04, adiante.)

As **listas práticas e seus gabaritos** têm outros **40 blocos** `Sua vez`, em 24
notebooks (eram 46 em 28 até a `Lista prática 04` ser reescrita, em 24/08/2026, e
44 em 26 até a aula 05 sair do curso, em 31/08/2026).
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
condicionada, e a `Aula prática 07` morria da §8 em diante — as 30 medidas do
`breast_cancer` são colineares o bastante. A correção é `QDA(reg_param=1e-4)`, um
ridge minúsculo na covariância, e ela **muda o resultado**: o QDA sai de empatado
na frente para trás do LDA no teste. O texto foi reescrito sobre o medido. (A §8 é
hoje a §7; a `Lista prática 07`, com a mesma chamada, só foi corrigida em
16/09/2026, e a `Lista prática 10` continua sem a correção.)

E uma terceira, em 21/09/2026: o **`AdaBoostClassifier` perdeu o `algorithm`**. O
`SAMME.R` foi depreciado na 1.4 e removido na 1.6, e o `SAMME` que ficou produz
**outras probabilidades**. A acurácia não se mexe; AUC e Brier, sim: no
`breast_cancer` da `Lista prática 10`, $0{,}9935 \to 0{,}9948$ e
$0{,}1480 \to 0{,}1264$. Não levanta erro nenhum — só aparece rodando. (A §7 da
`Aula prática 10`, que também usa AdaBoost, já estava medida numa versão recente e
confere na 1.9 até a quarta casa.)

Uma varredura dos argumentos de **todas** as chamadas do scikit-learn em **todos**
os notebooks contra as assinaturas da 1.9 não achou outro caso (10/08/2026) — mas
ela cobre nome de parâmetro, não exceção nova nem mudança de comportamento padrão,
que é justamente a classe destas duas. Rodar é a única varredura que pega.
O `requirements.txt` registra as duas.

**Armadilha ao abrir um notebook no Jupyter:** salvar grava as saídas e os
`execution_count`, e ainda **reordena as chaves de cada célula** para a ordem
canônica do `nbformat` (`cell_type, execution_count, id, metadata, outputs,
source`). Os notebooks do repositório estão em outra ordem (`cell_type, id,
metadata, source, execution_count, outputs`), então uma abertura sem edição
nenhuma já produz um diff do arquivo inteiro. Antes de commitar, limpe **e
restaure a ordem** --- os treze laboratórios guiados estão uniformes desde
24/08/2026, e vale manter:

```python
import json

ORDEM_COD = ("cell_type", "id", "metadata", "source", "execution_count", "outputs")
ORDEM_MD  = ("cell_type", "id", "metadata", "source")

p = "aulas/01-introducao/Aula prática 01.ipynb"
nb = json.load(open(p, encoding="utf-8"))
novas = []
for c in nb["cells"]:
    if c["cell_type"] == "code":
        c["outputs"], c["execution_count"] = [], None
        chaves = ORDEM_COD
    else:
        chaves = ORDEM_MD
    nova = {k: c[k] for k in chaves if k in c}
    nova.update({k: v for k, v in c.items() if k not in chaves})   # nada se perde
    novas.append(nova)
nb["cells"] = novas
open(p, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
```

A reordenação é semanticamente inócua (o JSON é equivalente), mas desfazê-la é o
que mantém o diff legível. Confira com `nb == original` antes de gravar: a
igualdade de dicionários em Python ignora ordem, então ela prova que só a ordem
mudou.

O Jupyter carimba também `metadata.language_info.version` com a versão do kernel
que rodou. Como os notebooks são commitados **sem saída**, esse campo não
registra nada de real --- é só ruído de diff. O valor da casa é o Python desta
máquina, **3.12.7**, em 39 dos 44 notebooks. As cinco exceções são exatamente os
cinco herdados de demonstração (adiante), e ficam como estão: três em 3.11.7, um
em 3.9.15, e o `Exemplo - PCA`, que é do Colab e cujo `language_info` só traz o
nome da linguagem --- inventar versão ali seria fabricar metadado.

Sobraram cinco notebooks herdados de demonstração (`Exemplo - ...`,
`EXTRA K-medias (exemplo)`, `Comparação entre classificadores paramétricos`). Eles
são curtos, estão em estilo antigo e as notas os citam — mas **não** seguem as
convenções acima. Os quatro `Aula prática` herdados foram aposentados; continuam na
`main` e no histórico.

## Listas de exercícios

Além do laboratório guiado, **cada aula tem uma lista para depois da aula**, na
pasta da própria aula e sempre com gabarito: `Lista teorica NN.tex` (3–4
exercícios, nenhum marcado como opcional; **duas exceções, com 2**: a 04 desde
24/08/2026 e a 06 desde 11/09/2026) e `Lista prática NN.ipynb` (lacunas marcadas
por `...`), cada uma com seu `- gabarito`. O gabarito teórico é o
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
   **Uma exceção, deliberada: o Ex. 3 da `Lista prática 05`**, que usa a semente
   `12` --- a mesma da figura `05-numero-arvores` --- porque o exercício existe
   justamente para o aluno reproduzir os números que a legenda da nota afirma
   ($8{,}0399$ em $B=1$ e $3{,}3510$ em $B=100$), e o gabarito diz isso com todas as
   letras. Os dados saem **byte-idênticos** (conferido). Não "conserte" trocando a
   semente: quebraria o vínculo com a nota, que é o ponto do exercício. (Até
   09/09/2026 a `Aula prática 05` usava essa mesma população, e o número era
   copiável de lá; a seção que a usava saiu com o *boosting*.)
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

## Avaliações (`avaliacoes/`, na raiz)

Criada em 14/09/2026, decisão do Gabriel. É **irmã** de `aulas/` e `recursos/`, e
guarda as avaliações do curso atual. As duas Avaliações Presenciais de 2025-02
continuam em `recursos/avaliacoes/`: são herdadas do Prof. Hugo e não se misturam
com estas.

```
avaliacoes/
├── Lista de revisao 01-06.tex            11 exercícios, Bloco I
├── Lista de revisao 01-06 - gabarito.tex invólucro de 3 linhas
├── Avaliacao teorica 01.tex              3 questões sorteadas
├── Avaliacao teorica 01 - gabarito.tex   invólucro de 3 linhas
└── exercicios/
    └── ex-NN-slug.tex                    o corpo de cada exercício, 11 arquivos
```

**Os 11 exercícios são inéditos**, e não repetem nenhum dos 20 das
`Lista teorica 01`--`06`. O critério que os tornou inéditos por construção: boa
parte deles pede que o aluno **demonstre resultados que as notas enunciam sem
demonstrar** --- o atalho do LOOCV (aula 03), as fórmulas do lasso no caso
ortonormal (aula 02), as duas formas da fórmula de $k$ dobras (aula 03, numa
`atencao`). São 2+3+2+1+2+1 por aula.

**A aula 06 tem só um exercício, de propósito.** Ela não tem teorema, proposição
nem demonstração, e tem uma única equação numerada --- só sustenta questão
conceitual, e os dois ângulos bons já são os dois exercícios da
`Lista teorica 06`.

**Dois exercícios saíram em 16/09/2026**, por decisão do Gabriel: o do viés da
validação cruzada (aula 03) e o dos nós de *splines* (aula 04), que eram os Ex. 8
e 9. A aula 04 também ficou com um exercício só, e os antigos Ex. 10 a 13 viraram
8 a 11, com os arquivos renomeados junto (`ex-13-escala.tex` virou
`ex-11-escala.tex`). **O `NN` no nome dos arquivos de `exercicios/` é o número do
exercício na lista**, e mantê-lo assim é manual: a numeração impressa é automática,
a dos arquivos não. Ao tirar ou pôr um exercício, renomeie os seguintes e atualize
os `\input` da lista **e da prova**.

### O `estilo-avaliacao.sty` duplica o `estilo-lista.sty`, e é de propósito

O `estilo-lista.sty` alcança o `estilo-notas` por
`\RequirePackage[aluno]{../../recursos/latex/estilo-notas}` --- caminho relativo
ao **diretório de compilação**, não ao `.sty`. Funciona porque todo documento do
repositório está exatamente dois níveis abaixo da raiz (`aulas/NN-tema/`). A
pasta `avaliacoes/` está a **um** nível, e ali aquele `../../` sai do
repositório.

Por isso o `estilo-avaliacao.sty` carrega o `estilo-notas` com um `..` só e
**duplica** as ~30 linhas de que precisa: a opção `[gabarito]`, o ambiente
`exercicio` e o ambiente `solucao`. Se um dia mexerem num dos dois arquivos, o
outro precisa acompanhar --- está anotado no cabeçalho do `.sty`.

Ele acrescenta `\cabecalhorevisao`, `\cabecalhoprova` (título e caixa de
instruções, que no gabarito dá lugar a um aviso ao professor), `\questao` (que
incrementa o mesmo contador do `exercicio` e aceita título vazio), a caixa `criterio`, e o par
`\ifprova`/`\pts` com o ambiente `itens` --- estes três explicados adiante.

### O sorteio da prova

Reproduzível, com a semente registrada em comentário no topo do
`Avaliacao teorica 01.tex`:

```python
rng = np.random.default_rng(20260914)                        # a data, aaaammdd
aulas = sorted(rng.choice([1,2,3,4,5,6], size=3, replace=False).tolist())
# -> [2, 3, 6]; depois um exercício dentro de cada aula, na mesma ordem
```

Resultado: Ex. 5 (aula 02, Ridge bayesiana), Ex. 7 (aula 03, as duas formas da
CV) e Ex. 13 (aula 06, sensibilidade à escala; hoje Ex. 11). A restrição de **uma
aula por questão** evita o azar de uma prova inteira sobre o mesmo assunto. **O
sorteio rodou uma vez e vale** --- não foi repetido até dar um resultado bonito.
Ele rodou sobre a lista de 13; refeito com a de 11, a mesma semente sorteia os
mesmos três exercícios (conferido em 16/09/2026).

Pesos: **4,0 por questão**, total 12,0, em 2 horas. A igualdade entre as três não
é simetria decorativa: a Questão 3 pede sete respostas (cinco classificações mais
dois itens discursivos) e a Questão 1 pede três, de modo que pesos iguais já
corrigem um desequilíbrio que a distribuição anterior tinha.

### A prova não diz de que aula vem cada questão

Decisão do Gabriel em 16/09/2026. O sorteio é feito por aula, mas nada que o aluno
lê na prova revela a aula de origem de uma questão:

- **o título da questão não tem marcador.** O `\daaula`, que imprimia ``[Aula 03]''
  à direita do título, saiu das três questões e do estilo;
- **o enunciado não cita aula por número.** O Gabriel reescreveu os Ex. 1 a 5 nessa
  linha (``já mencionamos'', ``as notas da aula de Regressão Linear''), e o Ex. 7,
  sorteado, trocou as duas menções à ``Aula~03'' por ``notas de aula'';
- **o cabeçalho não mostra o conteúdo.** O `\cabecalhoprova` ainda recebe o
  intervalo de aulas e a descrição (2º e 3º argumentos), mas não os imprime.

**A armadilha é o `\input`.** Em 16/09/2026 nenhum enunciado cita aula por
número; sobra só a ``Lista Teórica~01'', citada no Ex. 1, que não está na prova. Mas o enunciado entra na prova exatamente como está na
lista: **ao sortear uma prova nova, confira o texto dos exercícios sorteados**. Nas
soluções a menção é inofensiva, porque só aparece nos gabaritos.

Na mesma revisão o cabeçalho perdeu os campos de nome, matrícula e turma, e a caixa
de instruções ficou com a duração, o valor, ``Justifique todas as respostas'' e a
notação.

### Fonte única: por que a prova e a lista não podem divergir

O corpo de cada exercício --- enunciado, itens e solução --- mora em
`avaliacoes/exercicios/ex-NN-slug.tex`, e **os dois documentos o incluem por
`\input`**. A lista inclui os onze; a prova, os três sorteados. Nenhum dos dois
`.tex` de topo contém prosa de exercício: eles têm só cabeçalho, títulos, `\label`
e (na prova) os critérios de correção.

Isso não é organização, é a garantia pedida: divergir deixou de ser possível,
porque não há duas cópias. Corrigir um exercício é mexer num arquivo só.

A única coisa que difere entre os dois usos é a **pontuação por item**, que a
prova mostra e a lista não. Ela vem do comando `\pts` do estilo:

```latex
\newif\ifprova\provafalse
\newcommand{\pts}[1]{\ifprova\textbf{(#1)}\ \fi}
```

Cada arquivo de exercício escreve `\item \pts{1,0} texto...`; a prova declara
`\provatrue` antes do `\begin{document}` e o marcador aparece, enquanto na lista
ele some. Os itens usam o ambiente `itens` do estilo, para que a formatação seja
idêntica nos dois.

**Ao conferir isso, não compare o `pdftotext` dos dois PDFs.** Documentos com
matemática deslocada serializam somatórios e frações em ordem diferente conforme
a posição na página, e os números de página caem no meio do fluxo --- a
comparação acusa diferenças de poucos caracteres que não existem no conteúdo. A
verificação correta é na fonte: conferir que os `\input` da prova são subconjunto
dos da lista e que nenhum dos dois `.tex` de topo tem `\begin{solucao}`.

### O gabarito da revisão foi reescrito, e cinco respostas mudaram

Pedido do Gabriel em 21/09/2026, com a prova ainda por aplicar e a intenção de
liberar o gabarito da lista aos alunos: as onze soluções foram reescritas no
registro de **um professor de matemática didático** --- hipóteses explícitas, cada
passo justificado, e a leitura do resultado depois de cada conta. Os enunciados
ficaram intactos byte a byte, com três exceções (adiante). O gabarito da lista foi
de 18 para 23 páginas; o da prova, de 5 para 7.

A reescrita derrubou cinco respostas e desfez uma ambiguidade:

| Ex. | o que o gabarito dizia | o que diz hoje |
| --- | --- | --- |
| 8(c) | "os botões correm em sentidos opostos" --- e a frase seguinte dizia que $k$ grande e $\lambda$ grande simplificam os dois | correm no **mesmo** sentido; ao contrário corre o grau do polinômio, ou o número de nós. E $k$ não é "botão contínuo" |
| 10(d) | o preço da floresta é "variância individual maior", e com $m$ pequeno "o produto $\rho v$ volta a subir" | o preço é **viés** --- a condição (i), que é o que o enunciado pergunta, e o que a `Lista teorica 05` 4(d) já dizia |
| 10(a-i) | com viés, "a conclusão deixa de valer" | a comparação com cada $g_b$ sobrevive; o que se perde é o piso, que vira $\Var(Y\mid\x)+b^2$ |
| 4(d) | $2{,}3$ é "uma espécie de média" de $\partial r/\partial x_1$, "podendo não coincidir com a inclinação em ponto nenhum" | com uma covariável é média e coincide em algum ponto; com várias nem média é: $\beta^\ast_1=2/(2+s^2)$ para $r=x_2^2$ e $X_1=X_2^2+\varepsilon$ |
| 8(d) | só aceitava *smoothing splines*, que o deck 04 não tem e as notas citam numa frase | aceita a árvore podada --- o deck 05 a chama de não paramétrica, e o $\alpha\abs{T}$ de "reminiscente do Lasso" |
| 7 | "a fórmula da aula" --- mas o deck 03 define $\frac1k\sum_i\mathrm{EQM}_i$, que é a do **livro** | "a fórmula das notas", também no enunciado do item (a) |

O 10(d) foi medido na população do Ex. 2 da `Lista prática 05`, com as mesmas
sementes (a tabela de lá se reproduz): de $m=p/3$ para $m=0{,}15\,p$ o piso $\rho v$
ainda cai ($0{,}276\to0{,}208$), e quem faz o erro subir é o viés$^2$
($0{,}984\to1{,}144$). Um detalhe para quem for mexer naquela lista: o "$v$" dela
é a variância **entre as árvores de uma mesma floresta**, não a variância total de
uma árvore, e o $\rho$ isolado da fórmula com esse $v$ sai $0{,}147$ no *bagging*,
contra $0{,}127$ do verdadeiro. As conclusões não mudam. E o Ex. 2(c) passou a dizer
por que a barra ingênua da CV não é honesta: na população da Aula 01 (grau 5,
$n=50$, $k=5$, 4000 amostras), CV $\pm2$ EP cobre o risco condicional em 82,8% das
vezes; o teste de $m=50$, em 92,0%.

**As três mudanças de enunciado**: "sem intercepto" no Ex. 3 (a coluna de uns não
cabe numa $\mathbb{X}$ com $\mathbb{X}^\top\mathbb{X}=\mathbb{I}$); "fórmula das
notas" no Ex. 7(a); e o título do Ex. 8 com maiúscula. Na prova que o aluno recebe,
a única diferença de texto é a do Ex. 7(a) --- conferido pelas coordenadas das
palavras no PDF (`pdftotext -bbox`), porque o `pdftotext -layout` acusou mudanças
de espaçamento que não existem: ele estima a largura das colunas pela página
inteira. **Os critérios da prova** ganharam três linhas: no Ex. 5, a ressalva do
intercepto não é exigida; no Ex. 11(a)(i), vale dizer que a predição soma
$\beta_jx_j$, desde que se note que cada parcela é invariante; no 11(c), vale o
argumento de que a comparação usou o mesmo $\lambda$.

**Armadilha nova: `\ref` nas soluções.** Os Ex. 1, 4 e 8 citam outros exercícios
por `\ref{ex:...}`, com os `\label` da `Lista de revisao 01-06.tex`. Esses rótulos
não existem na prova: se um sorteio futuro escolher um desses três, o gabarito da
prova imprime `??`. Os três sorteados hoje (5, 7 e 11) não citam exercício nenhum
por número --- "no caso ortonormal, em que o Lasso tem fórmula fechada", em vez de
"Exercício 3".

**Uma medição que não entrou, e é decisão do Gabriel.** Na mesma população, o
*bagging* com árvores **podadas** fica com risco um pouco **menor**:

| árvores do *bagging* | viés$^2$ | $v$ total | $\rho$ | piso $\rho v$ | EQM |
| --- | --- | --- | --- | --- | --- |
| profundas | 0,876 | 3,746 | 0,127 | 0,477 | 1,373 |
| `ccp_alpha=0.05` | 0,913 | 3,036 | 0,145 | 0,439 | 1,367 |
| `ccp_alpha=0.2` | 1,049 | 1,522 | 0,180 | 0,274 | 1,328 |
| `max_depth=4` | 1,005 | 2,100 | 0,164 | 0,345 | 1,359 |
| `max_depth=2` | 1,141 | 0,986 | 0,211 | 0,208 | 1,352 |

Podar sobe o viés e **a correlação** --- as árvores ficam só com os cortes do topo,
os mais estáveis de uma amostra bootstrap para outra ---, mas derruba o $v$, e a
média não elimina o piso $\rho v$. É o contrário do "não podar as árvores!" do deck
05. O Ex. 10(b) foi escrito **condicionado às hipóteses da proposição**, onde o
argumento vale, e por isso não contradiz o deck. Levar a ressalva ao gabarito, às
notas ou ao deck espera o Gabriel.

E um aviso, registrado para não se perder: **liberar o gabarito da lista antes da
prova entrega a resolução completa das três questões**, porque os Ex. 5, 7 e 11
entram nela literalmente.

### Pendências achadas na mesma revisão

- **O atalho do LOOCV não vale para o KNN, e o material se contradiz.** A
  `Lista prática 04` mede isso (ver a seção da aula 04), mas as notas da aula 04
  --- as duas versões: "basta que $\ell_i(\x)$ não dependa de $\bm{Y}$" --- e a
  `Lista teorica 04` Ex. 2(c) --- "para $k\ge2$ a fórmula funciona normalmente" ---
  afirmam o contrário. A razão é exata: com $k$ vizinhos,
  $(Y_i-\rhat(\X_i))/(1-1/k)=Y_i-(\text{média dos outros } k-1 \text{ vizinhos})$,
  isto é, o "atalho" calcula **o LOOCV do $(k-1)$-NN** (medido: $0{,}900322$ nos
  dois, em $k=2$). No Ex. 6 da revisão, o passo que falha é o (b).
- **O deck 01 ainda tem `g: \mathbb{R}^d \to \mathbb{R}`**, nos slides "A
  importância da perda quadrática" e "Teorema (Teo. 1, Sec. 1.4 [AME])": uma
  dimensão que escapou da migração.
- **Dois erros de digitação nas notas da aula 06 (aluno)**: "píspares" e
  "Inflacção".

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

Por que não só a pasta da aula: `superconductivity.csv` tem 23 MB e era lido por 10
notebooks; uma cópia por pasta custaria ~230 MB. Por que não só `recursos/dados/`:
sem o repositório esse caminho nunca resolve, e o aluno teria de editar a primeira
célula em toda aula. As duas tentativas anteriores foram essas, nessa ordem.

**A migração terminou em 12/08/2026**: os 17 notebooks que carregam `.csv` usam
essa célula, byte a byte igual a menos do nome do arquivo. Nenhum baixa nada da
rede, e nenhuma URL do GitHub sobrou no repositório — antes havia um *fallback*
para `raw.githubusercontent`, que amarrava o material ao nome da branch.

Quem **carrega** o quê, medido em 16/09/2026 por leitura no código, não por
menção ao nome do arquivo — a `Aula prática E2` cita o `superconductivity.csv` só
no texto, e não entra. A tabela anterior, de 12/08/2026, estava na numeração de
antes da saída da aula 05 e ainda contava a `Aula prática 06`, que deixou de ler o
`bank_train_redux.csv` quando encolheu, em 14/09/2026:

| arquivo | tamanho | notebooks |
| --- | --- | --- |
| `superconductivity.csv` | 23 MB | 9 — aulas 01 a 05, incluindo as listas 02 e 05 |
| `bank_train_redux.csv` | 96 MB | 4 — aula 08, incluindo a lista, e a `Aula prática 10` |
| `spam.csv` | 0,5 MB | 3 — aula E3, incluindo a lista |

A `Aula prática 10` é a única que foge do byte a byte: o banco entra ali como
segundo conjunto, depois do `breast_cancer`, com os nomes sufixados (`_nome_b`,
`_caminho_b`) e `nrows=20_000`.

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
  Mede-se: com $y$ de ruído puro, isso fabrica $R^2 = +0{,}40$ (notas da aula 06,
  painel esquerdo da Fig.~1, gerado por `_vazamento()` no `gerar-figuras.py`);
- **grave** — a mesma unidade nos dois lados da divisão, ou informação do futuro.
  Nenhum `Pipeline` protege disso; a ferramenta é `GroupKFold` (notas da aula 06,
  caixa da hierarquia);

**Desde 14/09/2026 nenhum notebook mede os dois graves** --- os exercícios que os
mediam saíram da `Lista prática 06` quando ela foi espelhar o laboratório enxuto.
Eles vivem no texto das notas, na Fig.~1 e no Ex. 1 da `Lista teorica 06`, que pede
para classificá-los. A geradora da figura continua medindo.
- **leve** — padronização, imputação pela média e **PCA**. Nenhuma das três vê o
  $Y$, e portanto nenhuma consegue fabricar sinal a partir de ruído.

O PCA estava classificado como grave nas notas E2 e 06. A `Aula prática E2` (§7)
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
   03, 05, 07 e o EXTRA de k-médias). É o mesmo livro.
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
8. Em 02/09/2026, a definição de florestas aleatórias no slide "Visão de ambos os
   métodos" do deck da aula 05 --- o primeiro em que os dois métodos aparecem lado
   a lado. Ela dizia "crescer a árvore com ``mais cuidado''", e aponta para o lado
   oposto do que o método faz: sortear $m<p$ covariáveis por nó torna **cada árvore
   individualmente pior**, de propósito (o Ex. 2 da `Lista prática 05` mede $v$
   subindo de $3{,}28$ para $3{,}80$ do *bagging* para a floresta --- a medição
   estava na `Aula prática 05` até o corte de 09/09/2026). Além disso "com cuidado"
   lê-se como poda ou critério de parada, e o slide **seguinte** manda "**não**
   podar as árvores!". Virou "Crescer a árvore com **menos opções**: em cada nó, só
   $m<p$ covariáveis sorteadas" --- o mecanismo, sem a motivação, que o deck
   constrói dois slides adiante no "*Bagging* - atenção!". O slide "Florestas
   aleatórias", mais ao fim do mesmo deck, já trazia a definição certa: o defeito
   era só da visão geral.
9. Em 09/09/2026, o slide "Fechando o *bagging*" do deck da aula 05 perdeu o tópico
   "Permite criar uma medida de importância para cada covariável", quando a
   importância de variáveis saiu da aula. Foi a **única linha** que os três
   assuntos cortados ocupavam no deck inteiro.
10. Em 21/09/2026, dois erros de digitação no deck da aula 07: ``Classifidadores
    *plug-in*'' virou ``Classificadores'' --- no título e no `id` do slide, que nada
    mais referenciava --- e ``hiperlanos'' virou ``hiperplanos'', no slide das
    fronteiras do LDA.
11. Em 21/09/2026, o deck da aula 07 ganhou uma seção de **regressão logística**, a
    pedido do Gabriel: oito slides (a ideia, o modelo, o *log-odds* linear, a
    interpretação dos coeficientes, a estimação por MV, a penalização com o `C`
    invertido, o caso multiclasse e um fecho ``generativo ou discriminativo''),
    escritos no padrão dos outros --- `<li class="fragment">`, MathJax, `<code>` com
    link para a documentação do `scikit-learn`, `^T` para transposta como no resto
    deste deck. O deck foi de 43 para 44 slides. Conferido no navegador: zero
    `MathJax_Error`, nenhum slide sem título e nenhum transbordando.

## O slide de SVM, o único em Beamer

O fonte chegou em 17/08/2026 e a autoria antiga acabou: **não há mais material do
curso creditando o Prof. Hugo**. O que veio foi o `main.tex` do curso inteiro dele
— 137 frames, 3473 linhas, 50 figuras — em que tudo menos SVM estava dentro de dois
`\begin{comment}`. Daí saíram os 30 frames de SVM e as 10 figuras que eles usam;
mais dois frames escritos aqui, e o deck tem 32.

```
aulas/09-svm/
├── 09 SVM - slide.tex        ← 958 linhas, Beamer tema Madrid
├── 09 SVM - slide.pdf        ← 33 páginas, mesmo caminho de antes
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
larga e mais vetores de suporte, e a §8 da `Aula prática 09` mede o contrário
($C=0{,}01 \to 92$ vetores; $C=1000 \to 24$). As notas já traziam a inversão numa
caixa `atencao`; agora o slide também.

**O que ficou de fora:** os outros 107 frames do curso do Hugo e 40 figuras. Estão
só no zip que ele enviou, não no repositório.
