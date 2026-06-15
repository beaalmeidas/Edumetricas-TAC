# Edumetricas: Progresso inicial do projeto

**Equipe:** <br />
Beatriz Almeida de Souza Silva <br />
Paula Thifanny Gomes Dias

<br />

## Sumário
- [Edumetricas: Progresso inicial do projeto](#edumetricas-progresso-inicial-do-projeto)
  - [Sumário](#sumário)
  - [Levantamento dos dados necessários](#levantamento-dos-dados-necessários)
  - [Descrição dos dados](#descrição-dos-dados)
    - [1-) Dados internos](#1--dados-internos)
    - [2-) Dados externos](#2--dados-externos)
  - [Fontes](#fontes)

<br />

---

## Levantamento dos dados necessários

A fase inicial e mais importante do desenvolvimento do projeto foi a avaliação dos dados necessários para sua execução.

Nesse processo, foi fundamental identificar e separar dois tipos principais de dados:

* ***Dados internos (da escola em questão):*** informações que devem ser fornecidas pela própria instituição de ensino.
* ***Dados externos (nacionais):*** informações de desempenho escolar do ensino médio a nível nacional e estadual.

Essa etapa foi essencial para garantir que o projeto fosse viável e que as análises propostas pudessem realmente gerar insights relevantes.

O objetivo é pegar os dados próprios da escola, do conjunto de turmas do ensino médio, e gerar um sistema de análise, não só para comparação do grupo com dados de desempenho nacional, mas também para acompanhamento individual do desenvolvimento de cada aluno.

--- 

## Descrição dos dados

### 1-) Dados internos
Tem-se os seguintes datasets [caminho: `(data/internal)`]:
- `alunos.csv`: contém informações identificadoras de cada um, tendo-se os campos: matrícula, nome, série, turma, gênero e data de nascimento.
- `professores.csv`: informações identificadoras do corpo docente.
- `linguagens.csv`
- `matematica.csv`
- `ciencias_humanas.csv`
- `ciencias_natureza.csv`

Os datasets de disciplinas possuem dados por aluno com suas notas, faltas e entregas de atividade por bimestre, possibilitando a análise temporal de seu desenvolvimento.
<br />
As disciplinas também possuem o registro de qual professor ministrou cada semestre, para análise de desempenho docente.

### 2-) Dados externos
Para comparações, foram utilizados os seguintes conjuntos de dados [caminho: `(data/external)`]:
- `br_inep_saeb_brasil.csv`: dados de níveis de aprendizado do SAEB a nível nacional, inclui tanto a esfera privada quanto pública.
- `br_inep_saeb_uf.csv`: dados de níveis de aprendizado do SAEB, organizados por estado e disciplina (Língua Portuguesa e Matemática), inclui tanto a esfera privada quanto pública.
- `enem_2024_amostra.csv`: amostra com os resultados de 10.000 participantes do Enem 2024.

<br />

---

## Fontes

Abaixo estão as fontes utilizadas para obtenção dos dados:

* Desempenho a nível nacional (SAEB) [`br_inep_saeb_brasil.csv`]: https://basedosdados.org/dataset/e083c9a2-1cee-4342-bedc-535cbad6f3cd?table=728178ec-a7b2-42dc-9310-9ae8b67a6687
* Desempenho por estado (SAEB) [`br_inep_saeb_uf.csv`]: https://basedosdados.org/dataset/e083c9a2-1cee-4342-bedc-535cbad6f3cd?table=7a42b71d-7e34-4ba1-8503-86a3dba48a39
* Microdados do ENEM [`enem_2024_amostra.csv`]: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem
