# Aprendizado de Máquina

Material didático do curso de Aprendizado de Máquina, ofertado para alunos da
Estatística, Ciências Atuariais, Matemática Aplicada e Engenharia Matemática na UFRJ.

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
├── listas/        listas de exercícios 01–08
├── avaliacoes/    avaliações presenciais (AP1, AP2) com gabarito
└── latex/         estilo-notas.sty (estilo compartilhado das notas de aula)
```

Cada pasta de aula contém, conforme disponível:
- o **slide** (`.html` ou `.pdf`);
- as **notas de aula** (`.tex` + `.pdf` compilado);
- os **notebooks** (`.ipynb`) de prática e exemplos do tópico.

## Notas de aula (LaTeX)

As notas de aula são escritas em LaTeX e compartilham um único arquivo de estilo,
`recursos/latex/estilo-notas.sty`. Cada `.tex` o referencia por caminho relativo, de
modo que basta compilar com `pdflatex` de dentro da própria pasta da aula:

```bash
cd aulas/01-introducao
pdflatex "01 Introducao.tex"
```

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
