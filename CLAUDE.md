# Notas para o Claude Code

Material didático do curso de Aprendizado de Máquina do **Prof. Gabriel Sanfins, na UFF**
(Estatística, Ciências Atuariais, Matemática Aplicada e Engenharia Matemática): notas em
LaTeX, slides, notebooks e dados. **Não é um projeto de software.** A organização está em
`README.md` e `recursos/README.md`; aqui fica o que eles não dizem.

**Este arquivo não é changelog.** Guarda decisões em vigor, convenções, acoplamentos entre
peças e armadilhas. O que foi feito numa sessão vai na mensagem do commit (o `git log` é
detalhado); ao atualizar, substitua o texto em vez de empilhar. A versão longa e datada que
existiu até 07/10/2026 é `git show b291d5a:CLAUDE.md`.

## Regras do jogo

- **Branches.** `refactoring-baby` é o curso do Gabriel e é onde se trabalha; `main` é o do
  Prof. Hugo Tremonte de Carvalho (UFRJ), na estrutura antiga. São paralelas e permanentes:
  não proponha merge, rebase nem "sincronizar", e não trate a diferença como pendência.
- **O repositório não é entregue aos alunos.** Eles recebem só o que o Gabriel escolhe,
  quando escolhe; por isso gabaritos, prova, roteiros de correção e roteiros do docente
  convivem aqui de propósito. O que liberar é decisão dele: informe, não alerte (ex.: o
  gabarito da lista de revisão resolve as três questões da prova). **Mas o remote é
  público** (`HugoCarvalhoUFRJ/ap-maq`, conferido em 08/10/2026): quem tem o endereço lê
  tudo. Mudar a visibilidade é com o dono da conta, e levaria a `main` junto.
- **Os alunos não conhecem os blocos.** Blocos I, II e III são do planejamento e do README.
  No material deles diz-se "regressão" e "classificação" ("Parte I do [AME]" é do livro e
  fica). Do mesmo modo, a prova e o Trabalho Prático 01 não citam aula pelo número.
- **O deck manda.** Os slides são o que os alunos veem. Assunto que não está no deck não
  entra nas notas, no laboratório nem nas listas sem falar com o Gabriel; se entra no deck,
  o resto da aula vai atrás. Foi aplicado, a pedido dele, às aulas 06, 07 e (em parte) 08;
  nas outras não corte por conta própria. Se uma medição contradiz o deck, o que fazer é
  decisão dele.
- **Meça antes de afirmar.** Os números do material foram medidos rodando o código, e várias
  afirmações de livro não se reproduziram. Medição nova é afirmação nova: confira-a contra
  as notas (as duas versões), as listas, os gabaritos e o deck.
- **Leia os livros, não cite de memória.** Estão em `recursos/livros/`: [AME] (Izbicki &
  Mendonça dos Santos) é o esqueleto teórico; [ISLP] (James et al.), intuição e Python.
  `pdftotext -f A -l B recursos/livros/AME.pdf -`; no AME, página do PDF = página do livro
  + 18; no ISLP o offset é instável, localize pelo título da seção.
- **Registro.** Texto novo ou reescrito sai como o de um professor universitário de
  matemática, didático e rigoroso: hipóteses explícitas, cada passo justificado, a leitura
  do resultado depois da conta. Sem aforismos nem frases de efeito, sem caixas "A lição.",
  pouco negrito e pouco travessão. Em exercício, uma pessoa e uma situação em cena, não
  enumeração abstrata. O notebook explica estatística, não as próprias escolhas de estilo.
- **Commits** em português, estilo *conventional commits* (`fix:`, `docs:`, `refactor:`).

## Notas de aula (LaTeX)

Cada aula tem duas notas, para dois públicos (não são rascunho e versão final):
`NN Título.tex` é o **roteiro do docente** (enxuto, com caixas `emsala`) e
`NN Título (alunos).tex` é a **versão do aluno** (leitura autônoma, com figuras; carrega o
estilo com `[aluno]`). Ao mexer em conteúdo, pergunte-se qual das duas o pedido atinge; na
dúvida, as duas. `recursos/latex/estilo-notas.sty` define a notação, os teoremas e as caixas
`emsala`, `ideia`, `atencao`; o `00 Planejamento.tex` tem preâmbulo próprio.

- **Compile de dentro da pasta** (o caminho do estilo é relativo): `pdflatex "NN ....tex"`.
  O planejamento e o Beamer da 09 pedem duas passadas. Pacotes: `texlive-latex-base`,
  `-latex-recommended`, `-latex-extra`, `texlive-fonts-recommended`, `texlive-pictures`,
  `lmodern`. Sem `babel` de propósito (rótulos em português à mão) e `pgfplots` em
  `compat=1.16`: não "modernize" nenhum dos dois.
- **Ao editar um `.tex`, recompile o `.pdf` e versione os dois.** Mas não recompile em massa:
  os PDFs versionados vieram de outro TeX Live, e recompilar sem mudança já gera diff
  (desfaça com `git checkout --`). Para comparar, use `pdftotext` de duas compilações
  **locais**. `pdftotext -layout` acusa diferenças de espaçamento que não existem; para
  conferir texto, compare por multiconjunto de caracteres ou use `-bbox`.
- **Numeração citada de fora:** a Prop. 3.2 das notas do aluno da 03 (atalho do LOOCV) é
  citada pelas da 04; a Prop. 3.1 da 08 (corte ótimo) é citada pela E3. Fórmula nova
  nessas notas entra sem número. Ao procurar remissão num `.tex`, procure também com
  quebra de linha no meio (`Aula` / `prática 11`).

### Notação

- **`p` é o número de covariáveis**, em notas, listas, slides, figuras e no markdown dos
  notebooks. No **código** dos notebooks a dimensão é `d` (lá `p` é probabilidade); as
  exceções são as Aulas práticas 02 e 04 e a Lista prática 06, que usam `p`.
- `d` continua valendo como distância (`d(\X_i,\x)`), índice (`d_j`, o `d` de
  tf-idf$(t,d)$) e diferencial. O grau do *kernel* polinomial é `q` e o número de
  componentes retidos na E2 é `k`. Colisões toleradas: `p` também é *p*-valor, densidade
  `p(\bbeta)` e, na aula 04, o número de nós do *spline* (como no [AME]).
- **Só nas notas da aula 02:** matriz em `\mathbb` (`\mathbb{X}`, `\mathbb{I}`), vetor em
  minúscula negrito, escalar sem negrito. Não estenda: nas outras aulas a maiúscula `\X`
  distingue vetor aleatório de realização.
- **Indicadora é `\mathbf{1}`** (macro `\1`). `\mathbb{1}` compila sem aviso e imprime ⊮, e
  `dsfont`/`bbm` não estão instalados.
- **Lasso no caso ortonormal: limiar $\lambda/2$** (RSS sem $\frac12$; a mesma convenção dá
  $\hat\beta/(1+\lambda)$ no Ridge). No scikit-learn o `Lasso` minimiza
  $\frac1{2n}$RSS $+\,\alpha\|\beta\|_1$: é a nossa convenção com $\lambda=2n\alpha$, e o
  fator até o `alpha` do `Ridge` é $2n$ (é $n$ no `ElasticNet` com `l1_ratio=0`).
- **Matriz de confusão: previsto nas linhas, real nas colunas** (como [AME] e [ISLP]); o
  `confusion_matrix` devolve a transposta, e o material avisa.

## O que cada aula cobre, e o que não volta

A numeração é a de hoje: 10 aulas oficiais (01 a 10) e três extras (E1 a E3). Commits
anteriores a 31/08/2026 usam a antiga, com uma aula 05 a mais.

- **Antiga aula 05** (aspectos teóricos dos não paramétricos: taxas, maldição, esparsidade,
  redundância): saiu inteira e não volta. As menções ao conceito nas aulas 04, 07, 10, E2 e
  E3 ficam de propósito, como vocabulário sem aula dedicada. Ao renumerar qualquer coisa,
  procure `Lista` junto com `Aula`.
- **03.** O material segue o argumento clássico do deck sobre a escolha de $k$ (LOOCV:
  pouco viés, variância alta). A medição que o contradizia saiu; a figura `03-escolha-k`
  mostra só viés e custo.
- **04.** Vai de bases e *splines* a KNN e suavizadores lineares. Não reintroduza
  Nadaraya–Watson, regressão polinomial local nem a citação do elefante de Von Neumann. Não
  desenvolve RKHS: remeta a [AME] §4.6. O título de [AME] §5.2 contém "Regressão Linear
  Local": glose a parte que interessa em vez de reescrever o título.
- **05.** Árvore, poda, agregação, *bagging* e florestas. Não reintroduza *boosting*, OOB nem
  importância de variáveis. Ficam de propósito a correlação $\rho$ e o piso $\rho v$: nas
  notas, na Lista teorica 05 (Ex. 4) e na Lista prática 05 (Ex. 2); se sair, saem os três.
  Outras aulas citam OOB e *boosting* como conceito, sem ponteiro para a 05.
- **06.** O laboratório e a lista prática cobrem só o que o deck cobre: sensibilidade à
  escala, $\mu$ e $\sigma$ aprendidos, o `Pipeline` e `Pipeline` + `GridSearchCV`. Não
  reintroduza neles vazamento por seleção, agrupamento, `ColumnTransformer` nem busca no
  pré-processamento. Os dois vazamentos graves vivem nas notas (texto e Figura 1, que mede
  o da seleção) e no Ex. 1 da Lista teorica 06; nenhum notebook de aula os mede.
- **07.** Notas, laboratório e listas seguem o deck, na ordem dele (Bayes ingênuo, LDA, QDA,
  logística). Fora de propósito: regressão sobre indicadores, a comparação de escala no
  laboratório e o `C` (nenhum material do aluno da 07 o define). Nas notas sem estar no
  deck, de propósito: as caixas "a acurácia engana" e "o preço do ingênuo" (a 08 as cita) e
  a observação do que se transfere da regressão.
- **08.** Laboratório com nove seções, sem $F_1$ e sem a seção de custos (o corte ótimo
  segue no deck e nas notas). A Lista teorica 08 pede só as métricas do deck. O deck e o
  resto da aula ainda não coincidem: ver "Pendências".
- **09.** O deck é o único em Beamer (adiante).
- As notas do aluno da 05 e da 07 não têm "Para praticar"; "Prática em Python" saiu das
  notas 04 a 08.

## Figuras, notebooks e os acoplamentos entre eles

`recursos/figuras/gerar-figuras.py` gera todas as figuras das notas (uma função por figura,
`@figura("nome", "aula")`; `python3 recursos/figuras/gerar-figuras.py 03 06` roda só essas
aulas). Ele imprime linhas `[conferência]` com os números que as legendas afirmam: se mudar
uma simulação, releia a legenda no `.tex`. Nos rótulos do matplotlib não use macro do curso
(`$\x$`), nem `\%`, `\,`, `\emph{}`; vírgula decimal é `{,}` dentro de `$...$`, e
`.replace(".", ",")` só no número.

**Cada laboratório reproduz as simulações da figura da sua aula, com os mesmos parâmetros e
a mesma semente** (população comum: $r(x)=\operatorname{sen}(1{,}5x)+0{,}3x$ em $[-3,3]$,
$\sigma=0{,}7$, $n=50$). Ao mexer num dos dois, confira o outro. Casos que enganam:

- **06:** a figura e as notas dizem $0{,}8466$ e $R^2=+0{,}40$ (este, citado também na
  Lista teorica 06 e nos notebooks da E2); o laboratório roda com semente própria e mede
  $0{,}8342$ contra $0{,}8341$. São duas amostras do mesmo experimento, e a nota do aluno
  diz isso. Não "conserte". A §5 do laboratório reproduz a saída do slide "Um exemplo".
- **05:** a `05-numero-arvores` só tem o painel da floresta, e o Ex. 3 da Lista prática 05 a
  reproduz com a **mesma** semente (12), de propósito.
- **07:** a §6 do laboratório reproduz a `07-lda-qda` até a quarta casa; o caso $p=2$, $n=20$
  é citado pela Lista teorica 07 3(d).
- **08:** a seção de calibração do laboratório reproduz a legenda da Figura 3 das notas; a
  `08-roc-metricas` não é reproduzida (o laboratório usa o `bank_train_redux.csv`).
- As **listas práticas usam semente diferente** da do laboratório (salvo o Ex. 3 da 05): todo
  número de gabarito é medido, não previsto.

### Convenções dos notebooks

Um laboratório guiado por aula (`Aula prática NN.ipynb`), na conduta dos labs do [ISLP] mas
sem o pacote `ISLP`:

- `from matplotlib.pyplot import subplots` e API orientada a objeto, nunca `plt.figure()`;
  `import sklearn.linear_model as skl`, `import sklearn.model_selection as skm`;
  `rng = np.random.default_rng(semente)`; nomes `X_tr`, `X_te`, `y_tr`, `y_te`, `modelo`;
- markdown antes de cada célula dizendo por que aquilo vem agora; nada de macro do curso
  (`\x`, `\bm`, `\rhat`, `\1`), que o MathJax não conhece: use `\mathbf{}`. `R$` vira `R\$`;
- o laboratório **mostra**: não escreva `Sua vez` nele. As listas práticas têm blocos
  `Sua vez`, e ali ficam (não converta sem perguntar);
- tempo de relógio só em ordem de grandeza, com aviso de que varia;
- versionados **sem saída**, sem `execution_count`, com `kernelspec` "Python 3" e
  `language_info.version` 3.12.7.

Cinco notebooks herdados de demonstração (`Exemplo - ...`, `EXTRA K-medias (exemplo)`,
`Comparação entre classificadores paramétricos`) não seguem nada disso e ficam como estão.

**Antes de versionar, rode o notebook inteiro fora do repositório** e confira cada afirmação
do texto contra o que as células imprimem:

```bash
jupyter nbconvert --to notebook --execute "Aula prática 03.ipynb" --output-dir /tmp
```

**Rode com scikit-learn 1.9**, a versão do Gabriel (conda `barennet_env`, na máquina
`/home/exxon-lp-003`; nas outras, um venv com `scikit-learn==1.9.0`). Versões antigas
escondem quebras, e rodar é a única varredura que as pega. O `requirements.txt` lista as que
já apareceram; em resumo:

- `LassoCV`/`ElasticNetCV` perderam `n_alphas` (omita; `Lasso.path` ainda aceita);
- `QuadraticDiscriminantAnalysis()` levanta `LinAlgError` com covariância mal condicionada
  (o `breast_cancer`): use `reg_param=1e-4`, que muda o resultado. Com menos observações que
  covariáveis numa classe nada resolve. Até a 1.5, pelo menos, ele ajusta calado;
- `AdaBoostClassifier` perdeu `algorithm`; com o `SAMME` as probabilidades ficam entre
  $0{,}2$ e $0{,}8$ (pouca confiança, não demais);
- `LogisticRegression(penalty=...)` sai na 1.10: omita, ou use `C=np.inf`;
- o padrão do `n_init` do `KMeans` é `"auto"`: uma rodada com `k-means++`, dez com
  `init="random"`;
- `GroupKFold` reparte grupos de tamanho igual de outro jeito conforme a versão, e
  `GroupKFold(shuffle=True)` exige 1.6 (o TP01 usa);
- os notebooks chamam `warnings.filterwarnings("ignore")`: depreciação só aparece com
  `python -W error::FutureWarning`, fora do notebook.

**Abrir no Jupyter ou na IDE suja o arquivo:** grava saídas e `execution_count`, reordena as
chaves das células e carimba `kernelspec`/`language_info`. Limpe depois da última edição:
`outputs=[]`, `execution_count=None`, chaves na ordem `cell_type, id, metadata, source`
(e depois `execution_count, outputs` nas de código), metadado como acima, e grave com
`json.dumps(nb, ensure_ascii=False, indent=1) + "\n"`. `nb == original` (a igualdade de
dicionários ignora ordem) prova que só a ordem mudou. Se a IDE salvou durante o trabalho,
confira as fontes contra a sua última versão antes de continuar.

## Listas de exercícios

Uma por aula, na pasta da aula: `Lista teorica NN.tex` (quatro exercícios; dois na 04, 06 e
08, três na 07) e `Lista prática NN.ipynb` (lacunas `...`), cada uma com gabarito. Estilo:
`estilo-lista.sty`, que carrega o `estilo-notas`.

- Os `.tex` das listas **não têm acento no nome**: o invólucro do gabarito faz
  `\input{Lista teorica NN.tex}` antes do `\documentclass`, e nome acentuado quebra.
- `\begin{solucao}` e `\end{solucao}` ficam sozinhos na linha (o `comment.sty` é por linha).
- O script que gera o par enunciado/gabarito dos `.ipynb` **não está no repositório**. Mexa
  nos dois no mesmo passo e confira que só divergem nas lacunas e nas células de leitura do
  gabarito ("Deve imprimir..."); a tabela "O que ficou" existe nos dois.

## Avaliações (`avaliacoes/`)

Irmã de `aulas/` e `recursos/`. As Avaliações Presenciais de 2025-02 em
`recursos/avaliacoes/` são herdadas e não se misturam. Estilo: `estilo-avaliacao.sty`, que
**duplica de propósito** ~30 linhas do `estilo-lista.sty` (a pasta está a um nível da raiz,
não a dois); se mexer num, o outro acompanha.

- **Fonte única.** O corpo de cada exercício mora em `exercicios/ex-NN-slug.tex` e entra por
  `\input` na lista de revisão (os onze) e na prova (os três sorteados); nenhum `.tex` de
  topo tem prosa de exercício. A pontuação por item vem de `\pts{}`, que só aparece com
  `\provatrue`. O `NN` do arquivo é o número do exercício na lista, mantido à mão: ao tirar
  ou pôr um, renomeie os seguintes e atualize os `\input` da lista **e** da prova.
- **O sorteio** (semente `20260914`, uma aula por questão, registrado no topo do `.tex`) deu
  os Ex. 5, 7 e 11. Rodou uma vez e vale. São 4,0 pontos por questão, 12,0 no total, 2 horas.
- **A prova não revela a aula de cada questão:** sem marcador no título, sem "Aula NN" no
  enunciado, cabeçalho sem conteúdo. O enunciado entra como está na lista: ao sortear outra
  prova, confira o texto dos sorteados. E as soluções dos Ex. 1, 4 e 8 usam `\ref` com
  rótulos que só existem na lista: sorteados, imprimiriam `??` no gabarito da prova.
- Para conferir lista contra prova, olhe a fonte (os `\input`); `pdftotext` dos dois PDFs
  serializa a matemática em ordens diferentes e acusa diferenças falsas.

### Trabalho Prático 01

`Trabalho pratico 01.tex` é o enunciado; o invólucro `- gabarito.tex` mostra as caixas
`solucao` e `criterio` (é o roteiro de correção); `- modelo.ipynb` é o ponto de partida do
aluno e `- resolucao.ipynb`, a resolução de referência. Cobre as aulas 01 a 10: R1 a R8 no
`concreto.csv` e C1 a C7 no `credito.csv`, 4,5 pontos cada parte e 1,0 de qualidade.

- **Os números das caixas saem do `resolucao.ipynb`**, rodado na 1.9 com as sementes do
  enunciado (uns 4 a 5 minutos). Mexeu em semente, grade ou dado: rode de novo e confira.
- Os dois `.csv` foram convertidos do `.xls` **sem limpeza**: limpar faz parte das tarefas.
  Os notebooks os procuram em `../recursos/dados/` (um nível só).
- O enunciado exige scikit-learn 1.6 ou mais, e a primeira célula do modelo confere.
- A SVM roda numa subamostra de 5000, fixada no enunciado, para caber nos 20 minutos.

## Dados

Os `.csv` ficam numa cópia única em `recursos/dados/` e **nenhum notebook do curso baixa
nada da rede** (nada de URL do GitHub; o herdado `Exemplo - PCA` baixa o MNIST). A célula de
carga procura na pasta do notebook e depois em `../../recursos/dados/`, e falha com mensagem
clara; é byte a byte igual em todos, a menos do nome do arquivo: copie-a de um laboratório.
Quem carrega o quê:

| arquivo | notebooks |
| --- | --- |
| `superconductivity.csv` (23 MB) | aulas 01 a 05 |
| `bank_train_redux.csv` (96 MB) | aula 08 (laboratório e lista) e Aula prática 10 |
| `spam.csv` | aula E3 |

O `bank_train_redux.csv` é um excerto da competição *Santander Customer Transaction
Prediction*: `target` vale 1 para quem fez uma certa transação (**não** é inadimplência) e as
200 covariáveis são anônimas. Está perto do teto de 100 MiB por arquivo do GitHub.

## Vazamento: a hierarquia

O que separa vazamento grave de leve é **se a etapa olha o $Y$**. Grave: selecionar
variáveis, hiperparâmetros ou modelo olhando a resposta (com $y$ de ruído puro fabrica
$R^2=+0{,}40$), e a mesma unidade nos dois lados da divisão ou informação do futuro (aí só
`GroupKFold`). Leve: padronização, imputação pela média, codificação de categóricas,
vetorização de texto e **PCA**, que não veem o $Y$ e não fabricam sinal (a Aula prática E2 e
a Lista prática E2 medem o PCA). A conduta não muda, tudo vai no `Pipeline`; muda onde gastar
vigilância.

## Conferido: não reabra

- O atalho do LOOCV **não vale para o KNN**: com $h_{ii}=1/k$ ele devolve o LOOCV do
  $(k-1)$-NN. Notas da 04, Lista teorica 04 e Lista prática 04 dizem isso.
- O grau 49 da aula 03 não tem um número, tem uma faixa: depende do corte de posto da
  instalação. O texto sustenta só as três leituras.
- O `C` da aula 09: as notas e o Beamer trazem o orçamento do [ISLP] e o inverso do
  scikit-learn, lado a lado.
- O QDA recusa o `breast_cancer` mesmo padronizado (colinearidade). Na implementação do
  scikit-learn só o LDA é invariante à escala: `reg_param` e `var_smoothing` quebram a do
  QDA e a do Bayes ingênuo.
- LDA contra QDA, como as peças da 07 dizem: $n$ contra $p(p+1)/2$ governa o que o QDA tem a
  perder; o que ele tem a ganhar é o quanto a fronteira de Bayes se afasta de uma reta.
  "Em dimensão baixa a escolha não importa" é falso.
- O [AME] omite o $\frac12$ do expoente nas densidades normais da §8.1.4; as notas do aluno
  da 07 avisam. No [ISLP], o aprendizado não supervisionado é o Capítulo 12, e a ROC do
  `Default` está no §4.4.2.

## Pendências que são do Gabriel

- **Aula 08, o escopo.** O deck (18 slides) vai da matriz de confusão à definição da AUC.
  Não tem precisão–revocação, AP, `class_weight`, calibração, Brier nem `scoring`, que as
  notas, o laboratório, as listas e a tarefa C4 do TP01 usam, e para onde as aulas 07, 09,
  10 e E3 apontam. Ou o deck cresce, ou o conteúdo sai e as remissões são redirecionadas.
  Saíram do deck e seguem nas notas a decomposição do risco pelas taxas e a AUC como
  probabilidade (a Observação 3.2 se apoia nelas).
- **$F_1$:** fora do deck e do laboratório da 08; segue nas notas da 08, na Lista prática 08,
  na E3, no planejamento e na tarefa C4(a) do TP01.
- **Aula 08, notação:** o corte é $K$ nas notas, $p_0$ no deck, $t$ no laboratório; os custos
  são $l_0,l_1$ nas notas, $\ell_0,\ell_1$ no deck e $c_{FP},c_{FN}$ no resto.
- **`MatConf.pdf`** (aula 08): nenhum material aponta mais para ele; continua na pasta.
- **Aula 07:** a razão de chances e a penalização saíram do deck e seguem nas notas.
- **"Para praticar"** diz "nesta mesma pasta" e "com gabarito", o que pressupõe o
  repositório; saiu das notas do aluno da 05 e da 07 e segue nas outras.
- **Aula 05:** medido, o *bagging* com árvores podadas tem risco um pouco menor, o contrário
  do "não podar as árvores!" do deck. Não entrou em material nenhum.
- **TP01:** prazo (`\prazo`), valor (`\valortotal`, hoje 10,0) e política sobre assistentes
  de IA (o enunciado não menciona).

## Slides em HTML

São dez `.html` em `aulas/*/` (aulas 01 a 08, 10 e E1; a 09 é Beamer, e E2 e E3 não têm
deck): reveal.js gerado pelo **Quarto 1.4.549**, com tudo embutido (3 a 8 MB cada). **Os
`.qmd` não estão no repositório.** Toda edição é feita direto no HTML e se perde se alguém
recompilar do fonte.

- **CRLF.** Os dez usam CRLF; o resto do repositório usa LF. Edite em modo binário (ou
  `newline=''`) e confira a contagem de CRLF antes e depois.
- O conteúdo começa entre as linhas 1140 e 1220; antes é CSS e JavaScript. Slides são
  `<section>`. Leia por trecho.
- **Ao buscar texto, descarte `<script>` e `<img>`:** a busca crua acha centenas de
  ocorrências falsas em JavaScript minificado e em base64.
- Os `id` das headings são slugs do Quarto (título repetido ganha `-1`, `-2`): mude junto
  com o título, depois de conferir que nada aponta para o antigo. O rodapé gerado pelo
  Quarto (`quarto-auto-generated-content`) mora dentro do último slide: se ele sair, mova-o.
- **O slide não rola e corta em silêncio** o que passa do fim: cerca de 450 caracteres
  visíveis por slide de tópicos. Na largura, o `<ul>` é `inline-block`: uma fórmula em
  *display* mais larga que a coluna arrasta a lista inteira, e a largura que o MathJax dá
  varia de um render para outro; quebre em `aligned`.
- Confira no navegador (Chrome *headless*): zero `MathJax_Error`, nenhum slide passando do
  fim nem da borda.

**Edições diretas já feitas** (o registro completo é
`git log --since=2026-08-01 -- 'aulas/*/*.html'`; quem tiver os `.qmd` precisa replicá-las):

- todos: autoria `Gabriel Sanfins` / `gabrielsanfins@id.uff.br`; `[ITSL]` virou `[ISLP]`;
- 01: regressão e classificação desinvertidas; título sem o "I"; "2 provas e 1 projeto";
  `g: \mathbb{R}^p`; erros de digitação;
- 02: slide vazio removido; argmin do MQO; limiar do lasso $\lambda/2$;
- 03: "Randomizar o conjunto de treinamento"; par regressão/classificação; "$k=1$ é o *data
  splitting*"; as três molduras "Implementando: ..." com o código explicado e
  `random_state=0`; erros de digitação;
- 04: slide novo "KNN - os pesos dos vizinhos"; grade só com `weights`; agradecimento
  datado ("edição de 2022/02 desta disciplina, então na UFRJ");
- 05: floresta como "menos opções: em cada nó, só $m<p$ covariáveis sorteadas"; saíram os
  três slides e o tópico de importância de covariáveis;
- 06: "Prós e contras do `StandardScaler`";
- 07: seção de regressão logística (seis slides); `MultinomialNB`; erros de digitação;
- 08: o slide "Veja `MatConf.pdf`" virou sete (matriz de confusão, doença rara, TPR, FPR,
  por que essas taxas); ROC reescrita; teorema do custo com os custos nomeados; saíram os
  quatro slides finais sobre o que a AUC mede e seus problemas;
- 10: erro de digitação no texto do link do `KNeighborsClassifier`;
- E1: figuras 12.7 a 12.9 do [ISLP]; erro de digitação;
- 06, 07, 08 e 10: o número da aula na capa, depois da renumeração.

## Slide de SVM (Beamer)

`aulas/09-svm/09 SVM - slide.tex` (tema Madrid, 32 frames) com as figuras em
`slide-figuras/`. Veio do `main.tex` do curso do Hugo, do qual só os frames de SVM entraram.

- **Não usa o `estilo-notas.sty`:** preâmbulo e macros do Hugo (`\V`, `\RR`, `\PP`, ...). Não
  tente unificar.
- O rodapé sai das chaves curtas de `\author[...]` e `\title[...]`.
- Sem `babel`, como nas notas (`\figurename` à mão).
- Dois defeitos do original foram corrigidos e não voltam: ambientes
  `withoutheadline`/`withoutbottomline` fechando cruzados, e `\set\date{SVM}`.
- Os dois frames escritos aqui são sobre o `C`: o original usava a mesma letra para o
  orçamento do [ISLP] e para o peso da penalidade do scikit-learn, que se invertem.
