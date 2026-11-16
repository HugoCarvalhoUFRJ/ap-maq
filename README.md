# Aprendizado de Máquina

Material didático do curso de Aprendizado de Máquina, ofertado para alunos da
Estatística, Ciências Atuariais, Matemática Aplicada e Engenharia Matemática na UFF,
pelo Prof. Gabriel Sanfins.

## Organização do repositório

O material está organizado **por aula** em `aulas/` (cada pasta reúne o slide, as
notas de aula e os notebooks daquele tópico), por **avaliações** em `avaliacoes/`
e por **recursos transversais** em `recursos/` (livros, dados e estilos usados ao
longo de todo o curso).

```
aulas/
├── 00-planejamento/              Planejamento geral do curso (.tex/.pdf)
├── 01-introducao/                Bloco I — Fundamentos e Regressão
├── 02-regressao-linear/
├── 03-validacao-cruzada/
├── 04-knn/
├── 05-arvores-e-ensembles/
├── 06-pipelines/
├── 07-classificadores-gaussianos/   Bloco II — Classificação
├── 08-metricas-classificacao/
├── 09-svm/
├── 10-knn-arvores-classificacao/
├── E1-k-medias/                  Bloco III — Não supervisionado e aplicações
├── E2-reducao-dimensionalidade/
└── E3-nlp-classificacao/

avaliacoes/                       Avaliações do curso, com gabarito
├── Lista de revisao 01-06.tex    lista de revisão do Bloco I (11 exercícios)
├── Avaliacao teorica 01.tex      a primeira prova, com 3 questões sorteadas dessa lista
├── exercicios/                   o corpo de cada exercício, incluído pela lista e pelas provas
├── Lista de revisao 07-10.tex    lista de revisão do Bloco II (9 exercícios)
├── Avaliacao teorica 02.tex      a segunda prova, com 3 questões sorteadas dessa lista
├── exercicios-07-10/             o corpo de cada exercício, incluído pela lista e pelas provas
├── Verificacao de reposicao.tex  a VR (segunda chamada), com 2 questões sorteadas de cada lista
├── Verificacao suplementar.tex   a VS (prova final), com 2 questões sorteadas de cada lista
└── Trabalho pratico 01.tex       o trabalho prático (aulas 01 a 10), com dois notebooks

recursos/
├── livros/        AME.pdf, ISLP.pdf
├── dados/         conjuntos de dados (.csv) usados nas aulas práticas
├── avaliacoes/    as Avaliações Presenciais de 2025-02, herdadas
├── figuras/       figuras das notas + gerar-figuras.py que as produz
└── latex/         estilo-notas.sty, estilo-lista.sty e estilo-avaliacao.sty

requirements.txt   pacotes necessários para rodar as aulas práticas
```

Cada pasta de aula contém, conforme disponível:
- o **slide**: `.html` gerado pelo Quarto em dez aulas (01 a 08, 10 e E1), e um
  Beamer em `.tex` mais `.pdf` na aula 09, com as figuras dele em `slide-figuras/`;
  as aulas E2 e E3 não têm slide;
- as **notas de aula** em duas versões (`.tex` + `.pdf` compilado);
- a **aula prática** (`Aula prática NN.ipynb`), um laboratório guiado, para
  acompanhar em sala;
- a **lista de exercícios** da aula, em duas partes e com gabarito
  (`Lista teorica NN.tex/.pdf` e `Lista prática NN.ipynb`), para depois da aula;
- eventuais **notebooks de demonstração herdados** (`Exemplo - ...`,
  `EXTRA K-medias (exemplo)` e `Comparação entre classificadores paramétricos`),
  que não seguem as convenções dos laboratórios.

## Aulas práticas

Há um notebook `Aula prática NN.ipynb` para cada uma das 13 aulas. Eles seguem a
conduta dos laboratórios do [ISLP] — narrativa antes de cada bloco de código, API
orientada a objeto do `matplotlib` — mas sem depender do pacote `ISLP`: bastam
`numpy`, `pandas`, `matplotlib`, `scikit-learn`, `scipy` e `statsmodels`.

O laboratório guiado **mostra**, não deixa exercício em aberto: quem propõe
exercício é a lista prática da mesma aula. Onde havia uma pausa `Sua vez` seguida
de célula vazia, hoje há enunciado, código e leitura do resultado — nas treze
aulas. Todo número que o texto afirma foi medido executando a célula.

Quando um notebook **refaz a simulação de uma figura das notas**, usa os mesmos
parâmetros e a mesma semente, de modo que o número que aparece na figura é o número
que a célula imprime. É o caso, por exemplo, da decomposição viés–variância (aula
01), da validação cruzada contra o risco (03), de LDA contra QDA (07), dos *kernels*
(09) e das fronteiras do KNN (10). Nem toda figura tem contrapartida no laboratório:
os das aulas E1 e E2 trabalham com dados próprios, e o da 06 refaz a figura com
outra semente, que dá outra amostra do mesmo experimento. Os notebooks são
versionados sem saída.

### Como rodar

No **Google Colab** não é preciso instalar nenhum pacote: todos já vêm no ambiente
padrão. Os dados, sim, precisam ser enviados — ver a seção seguinte.

**Localmente**, as dependências estão em [`requirements.txt`](requirements.txt):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd aulas/03-validacao-cruzada
jupyter lab "Aula prática 03.ipynb"
```

São seis pacotes (`numpy`, `pandas`, `matplotlib`, `scikit-learn`, `scipy`,
`statsmodels`), mais `pillow` — que o `scikit-learn` **não** instala junto e é
necessário para a compressão de imagem da aula E1.

### De onde vêm os dados

Os `.csv` ficam em [`recursos/dados/`](recursos/dados), em uma cópia única para o
curso todo, e **nenhum notebook baixa dados da internet** (a exceção é a
demonstração herdada `Exemplo - PCA`, que baixa o MNIST). Todos procuram o
arquivo em dois lugares, nesta ordem:

1. a pasta do próprio notebook;
2. `../../recursos/dados/`, que resolve quando o repositório está clonado.

Se não acharem em nenhum dos dois, param com uma mensagem dizendo onde
procuraram. Assim funciona tanto para quem clonou o repositório quanto para quem
recebeu só o `.ipynb` e o `.csv` lado a lado. No Colab, é preciso subir o `.csv`
junto com o notebook.

## Listas de exercícios

Cada aula tem uma lista, na pasta da própria aula, em duas partes:

| Arquivo | O que é |
| --- | --- |
| `Lista teorica NN.tex` / `.pdf` | 2 a 4 exercícios de nível fácil a mediano |
| `Lista teorica NN - gabarito.pdf` | a mesma lista com as soluções |
| `Lista prática NN.ipynb` | notebook com lacunas marcadas por `...` |
| `Lista prática NN - gabarito.ipynb` | as lacunas preenchidas, com o valor esperado de cada saída |

O gabarito teórico **sai do mesmo arquivo-fonte** do enunciado: `Lista teorica
NN - gabarito.tex` apenas liga a opção `[gabarito]` do estilo e inclui o outro.
Isso torna impossível que enunciado e solução divirjam. Para compilar os dois,
de dentro da pasta da aula:

```bash
cd aulas/03-validacao-cruzada
pdflatex "Lista teorica 03.tex"             # enunciado
pdflatex "Lista teorica 03 - gabarito.tex"  # com as soluções
```

A Lista teorica 09 tem referências cruzadas e pede duas passadas, como as notas.

Todo número que aparece nos gabaritos foi **medido**, executando o notebook — e
em vários casos a medição contrariou o que se esperava. Esses casos estão
registrados nos próprios gabaritos, com a explicação.

## Avaliações

Ficam em [`avaliacoes/`](avaliacoes), na raiz — separadas das Avaliações
Presenciais de 2025-02, que são herdadas e continuam em `recursos/avaliacoes/`.

| Arquivo | O que é |
| --- | --- |
| `Lista de revisao 01-06.tex` / `.pdf` | 11 exercícios inéditos de nível intermediário, cobrindo o Bloco I |
| `Lista de revisao 01-06 - gabarito.pdf` | a mesma lista com as soluções |
| `Avaliacao teorica 01.tex` / `.pdf` | a primeira prova: 3 questões **sorteadas** da lista de revisão 01-06, 12,0 pontos, 2 horas |
| `Avaliacao teorica 01 - gabarito.pdf` | as soluções, com critério de correção por questão |
| `Lista de revisao 07-10.tex` / `.pdf` | 9 exercícios inéditos de nível intermediário, dois de cada uma das aulas 07, 08 e 09 e três da aula 10, cobrindo o Bloco II (classificação) |
| `Lista de revisao 07-10 - gabarito.pdf` | a mesma lista com as soluções |
| `Avaliacao teorica 02.tex` / `.pdf` | a segunda prova: 3 questões **sorteadas** da lista de revisão 07-10, 12,0 pontos, 2 horas |
| `Avaliacao teorica 02 - gabarito.pdf` | as soluções, com critério de correção por questão |
| `Verificacao de reposicao.tex` / `.pdf` | a Verificação de Reposição (VR), a prova de segunda chamada: 4 questões **sorteadas**, 2 de cada lista de revisão, 12,0 pontos, 2 horas |
| `Verificacao de reposicao - gabarito.pdf` | as soluções, com critério de correção por questão |
| `Verificacao suplementar.tex` / `.pdf` | a Verificação Suplementar (VS), a prova final, nos mesmos moldes e sem questão em comum com a VR |
| `Verificacao suplementar - gabarito.pdf` | as soluções, com critério de correção por questão |
| `Trabalho pratico 01.tex` / `.pdf` | o trabalho prático: 15 tarefas sobre as aulas 01 a 10, em dois conjuntos de dados reais, um de regressão e um de classificação, com entrega em notebook |
| `Trabalho pratico 01 - gabarito.pdf` | o roteiro de correção: o esperado em cada tarefa e a distribuição dos pontos |
| `Trabalho pratico 01 - modelo.ipynb` | o ponto de partida do aluno: carrega os dados e tem uma seção por tarefa |
| `Trabalho pratico 01 - resolucao.ipynb` | a resolução de referência, de onde saem os números do roteiro |

As listas de revisão não repetem nenhum dos exercícios das listas de cada aula: boa
parte delas pede que o aluno **demonstre** resultados que as notas usaram sem
demonstrar. Na primeira, o atalho do LOOCV, as fórmulas do lasso no caso
ortonormal e as duas formas da fórmula de $k$ dobras; na segunda, que a margem
máxima depende só dos vetores de suporte, que o *kernel* radial é um *kernel* em
qualquer dimensão e o preço do Bayes ingênuo com covariáveis redundantes.

As questões das quatro provas foram sorteadas com semente registrada no cabeçalho do
`.tex`, com a restrição de que, dentro de cada lista, cada uma venha de uma aula
diferente. A VR e a VS foram sorteadas juntas, sem os exercícios que já tinham caído
na primeira e na segunda prova, e não têm exercício em comum. Como nas listas, o
gabarito sai do mesmo arquivo-fonte do enunciado.

**A prova e a lista compartilham os exercícios, literalmente.** O corpo de cada
um — enunciado, itens e solução — mora em `avaliacoes/exercicios/` (lista 01-06)
ou em `avaliacoes/exercicios-07-10/` (lista 07-10), e os documentos o incluem por
`\input`: a lista 01-06 inclui os onze e a primeira prova, os três sorteados dela; a
lista 07-10, os seus nove, e a segunda prova, os três sorteados dela; a VR e a VS,
dois de cada pasta. Não há duas cópias, então não há como divergirem; corrigir um
exercício é mexer num arquivo só. A única diferença entre os usos é a
pontuação por item, que a prova mostra e a lista não — ela vem de um comando do
estilo, que some quando o documento não é uma prova. Na VR e na VS, cujas questões
valem 3,0 e não 4,0, a prova declara os valores de cada item, que substituem os
escritos no arquivo do exercício.

Para compilar, de dentro de `avaliacoes/`:

```bash
cd avaliacoes
pdflatex "Lista de revisao 01-06.tex"
pdflatex "Lista de revisao 01-06 - gabarito.tex"
pdflatex "Lista de revisao 07-10.tex"
pdflatex "Lista de revisao 07-10 - gabarito.tex"
```

O gabarito da lista 01-06 tem referências cruzadas e pede duas passadas.

## Notas de aula (LaTeX)

Cada aula tem **duas versões** das notas, lado a lado na mesma pasta:

| Arquivo | Para quem | O que é |
| --- | --- | --- |
| `NN Título.tex` | docente | roteiro de sala: enxuto, com caixas *Em sala* que trazem as perguntas a fazer à turma e o fio condutor do discurso |
| `NN Título (alunos).tex` | estudantes | texto autossuficiente para leitura fora da sala: sem instruções de palco, em tratamento direto ao leitor, com exemplos resolvidos e figuras |

As duas compartilham um único arquivo de estilo,
`recursos/latex/estilo-notas.sty`; a versão do aluno o carrega com a opção
`[aluno]`, que habilita `tikz`/`pgfplots` e ajusta o cabeçalho. Cada `.tex` o
referencia por caminho relativo, de modo que basta compilar com `pdflatex` de
dentro da própria pasta da aula (duas passadas, por causa das referências
cruzadas e das figuras):

```bash
cd aulas/01-introducao
pdflatex "01 Introducao.tex"            # versão do docente
pdflatex "01 Introducao (alunos).tex"   # versão dos alunos
```

## Figuras

As figuras das notas dos alunos ficam em `recursos/figuras/` e são geradas por
script — nenhuma foi copiada de livro. Para refazer todas (ou só as de algumas
aulas):

```bash
python3 recursos/figuras/gerar-figuras.py         # todas
python3 recursos/figuras/gerar-figuras.py 01 02   # só as aulas 01 e 02
```

O script imprime, ao gerar, conferências dos números que aparecem nas legendas
(por exemplo, que a decomposição viés–variância fecha na precisão de máquina).
Quando um notebook refaz uma dessas simulações, usa as mesmas constantes, de modo
que o aluno reencontra na prática os números da figura.

## Livros adotados

- **[ISLP]** Gareth James, Daniela Witten, Trevor Hastie, Rob Tibshirani & Jonathan
  Taylor — *An Introduction to Statistical Learning, with Applications in Python*
  ([on-line](https://www.statlearning.com/)).
- **[AME]** Rafael Izbicki & Tiago Mendonça dos Santos — *Aprendizado de Máquina:
  Uma Abordagem Estatística* ([on-line](https://rafaelizbicki.com/ame/)).

## Conjuntos de dados

Em `recursos/dados/`. Os arquivos `superconductivity.csv` e `bank_train_redux.csv`
são usados nas aulas práticas e provêm, respectivamente, de
[superconductivity](https://archive.ics.uci.edu/dataset/464/superconductivty+data) e
[bank_train_redux](https://www.kaggle.com/competitions/santander-customer-transaction-prediction/)
(este último é um excerto da base do Kaggle, por motivos de espaço no GitHub).
O `spam.csv`, da aula E3, é a
[SMS Spam Collection](https://doi.org/10.24432/C5CC84) (Almeida & Hidalgo, 2011),
também do UCI e sob CC BY 4.0, num `.csv` de colunas `v1` (o rótulo) e `v2` (a
mensagem) com 5 572 das 5 574 mensagens originais.
Os arquivos `concreto.csv` e `credito.csv`, do Trabalho Prático 01, vêm do
*UCI Machine Learning Repository*, sob a licença CC BY 4.0:
[Concrete Compressive Strength](https://doi.org/10.24432/C5PK67) e
[Default of Credit Card Clients](https://doi.org/10.24432/C55S3H).
