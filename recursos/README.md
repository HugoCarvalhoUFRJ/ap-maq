# Recursos transversais

Materiais usados ao longo de todo o curso (não pertencem a uma aula específica):

- **`livros/`** — os dois livros-texto adotados:
  - [ISLP] *An Introduction to Statistical Learning, with Applications in Python*
    (James, Witten, Hastie, Tibshirani & Taylor) — [on-line](https://www.statlearning.com/);
  - [AME] *Aprendizado de Máquina: Uma Abordagem Estatística*
    (Izbicki & Mendonça) — [on-line](https://rafaelizbicki.com/ame/).
- **`dados/`** — conjuntos de dados (`.csv`) usados nas aulas práticas.
  Fontes: [superconductivity](https://archive.ics.uci.edu/dataset/464/superconductivty+data)
  e [bank_train_redux](https://www.kaggle.com/competitions/santander-customer-transaction-prediction/)
  (excerto da base do Kaggle, por motivos de espaço no GitHub).
- **`avaliacoes/`** — as **Avaliações Presenciais de 2025-02** (AP1 e AP2) com
  gabarito, herdadas. As avaliações do curso atual **não** ficam aqui: estão em
  `avaliacoes/`, na raiz do repositório. E as **listas de exercícios** também
  não: são uma por aula, e moram na pasta da própria aula, em `aulas/`.
- **`latex/`** — os estilos LaTeX compartilhados: `estilo-notas.sty` (notas de
  aula), `estilo-lista.sty` (listas de exercícios, carrega o anterior) e
  `estilo-avaliacao.sty` (lista de revisão e provas).

  O `estilo-avaliacao.sty` **não** carrega o `estilo-lista.sty`, e duplica
  ~30 linhas dele de propósito: o `estilo-lista.sty` alcança o `estilo-notas` por
  `../../recursos/latex/`, caminho relativo ao diretório de compilação, que só
  resolve para documentos dois níveis abaixo da raiz. A pasta `avaliacoes/` está
  a um nível.

  Ele acrescenta o par `\ifprova`/`\pts`, que é o que permite à lista de revisão e
  à prova **incluírem os mesmos arquivos de exercício** sem que a pontuação por
  item apareça nas duas: `\pts{1,0}` some quando o documento não declara
  `\provatrue`.
