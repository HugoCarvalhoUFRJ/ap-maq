# Aprendizado de Máquina

Material didático do curso de Aprendizado de Máquina, ofertado para alunos da
Estatística, Ciências Atuariais, Matemática Aplicada e Engenharia Matemática na UFF,
pelo Prof. Gabriel Sanfins.

## Organização do repositório

O material está organizado **por aula** em `aulas/` (cada pasta reúne o slide, as
notas de aula e os notebooks daquele tópico) e por **recursos transversais** em
`recursos/` (livros, dados, listas e avaliações usados ao longo de todo o curso).

```
aulas/
├── 00-planejamento/              Planejamento geral do curso (.tex/.pdf)
├── 01-introducao/                Bloco I — Fundamentos e Regressão
├── 02-regressao-linear/
├── 03-validacao-cruzada/
├── 04-knn/
├── 05-knn-teoria/
├── 06-arvores-ensembles/
├── 07-pipelines/
├── 08-classificadores-gaussianos/   Bloco II — Classificação
├── 09-metricas-classificacao/
├── 10-svm/
├── 11-knn-arvores-classificacao/
├── E1-k-medias/                  Bloco III — Não supervisionado e aplicações
├── E2-reducao-dimensionalidade/
└── E3-nlp-classificacao/

recursos/
├── livros/        AME.pdf, ISLP.pdf
├── dados/         conjuntos de dados (.csv) usados nas aulas práticas
├── avaliacoes/    avaliações presenciais (AP1, AP2) com gabarito
├── figuras/       figuras das notas + gerar-figuras.py que as produz
└── latex/         estilo-notas.sty e estilo-lista.sty (estilos compartilhados)

requirements.txt   pacotes necessários para rodar as aulas práticas
```

Cada pasta de aula contém, conforme disponível:
- o **slide**: `.html` gerado pelo Quarto em treze aulas, e um Beamer em `.tex` mais
  `.pdf` na aula 10, com as figuras dele em `slide-figuras/`;
- as **notas de aula** em duas versões (`.tex` + `.pdf` compilado);
- a **aula prática** (`Aula prática NN.ipynb`), um laboratório guiado, para
  acompanhar em sala;
- a **lista de exercícios** da aula, em duas partes e com gabarito
  (`Lista teorica NN.tex/.pdf` e `Lista prática NN.ipynb`), para depois da aula;
- eventuais **notebooks de exemplo** (`Exemplo - ...`), demonstrações curtas.

## Aulas práticas

Há um notebook `Aula prática NN.ipynb` para cada uma das 14 aulas. Eles seguem a
conduta dos laboratórios do [ISLP] — narrativa antes de cada bloco de código, API
orientada a objeto do `matplotlib` — mas sem depender do pacote `ISLP`: bastam
`numpy`, `pandas`, `matplotlib`, `scikit-learn`, `scipy` e `statsmodels`.

O laboratório guiado **mostra**, não deixa exercício em aberto: quem propõe
exercício é a lista prática da mesma aula. Onde havia uma pausa `Sua vez` seguida
de célula vazia, hoje há enunciado, código e leitura do resultado — nas catorze
aulas. Todo número que o texto afirma foi medido executando a célula.

Cada notebook **reproduz as simulações das figuras das notas**, com os mesmos
parâmetros, de modo que o número que aparece na figura é o número que a célula
imprime. São commitados sem saída.

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
curso todo, e **nenhum notebook baixa dados da internet**. Todos procuram o
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
| `Lista teorica NN.tex` / `.pdf` | 3 ou 4 exercícios de nível fácil a mediano |
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

Todo número que aparece nos gabaritos foi **medido**, executando o notebook — e
em vários casos a medição contrariou o que se esperava. Esses casos estão
registrados nos próprios gabaritos, com a explicação.

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
As simulações usam as mesmas constantes dos notebooks das aulas práticas, de
modo que o aluno reencontra na prática os números das figuras.

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
