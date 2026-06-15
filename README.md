# Edumetricas - Análise de Dados e BI
Conjunto de dashboards desenvolvido como projeto final da disciplina Tópicos Avançados em Computação (semestre 2026.1), com o objetivo de apoiar gestores escolares na análise de desempenho de alunos, turmas e professores, além da tomada de decisões.
<br />
<br />
O sistema compara dados internos da escola com benchmarks nacionais (SAEB e Enem), permitindo avaliar o desempenho da instituição de ensino em comparação com seu estado e país.
<br />
<br />

#### Observações:
- Os dados utilizados são detalhados no [documento de descrição dos datasets](DESCRICAO_DATASETS.md).
<br />
- A regra de negócio também é descrita, no arquivo de [documentação do projeto](docs_edumetricas.pdf).

<br />

---

## Sumário
- [Edumetricas - Análise de Dados e BI](#edumetricas---análise-de-dados-e-bi)
      - [Observações:](#observações)
  - [Sumário](#sumário)
  - [Como rodar](#como-rodar)
    - [Deploy](#deploy)
    - [Executar localmente](#executar-localmente)
  - [Arquitetura do projeto](#arquitetura-do-projeto)
  - [Autores](#autores)

<br />

---

## Como rodar

### Deploy
A aplicação está pública através do Streamlit Community Cloud. <br />
https://edumetricas-tac.streamlit.app/

<br />

### Executar localmente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Edumetricas-TAC.git
cd Edumetricas-TAC

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python -m streamlit run src/ui/app.py
```

<br />

---

## Arquitetura do projeto
```
Edumetricas-TAC/
├── data/                       
│   ├── external/                       // DADOS PUBLICOS NACIONAIS
│   │   ├── br_inep_saeb_brasil.csv
│   │   ├── br_inep_saeb_uf.csv
│   │   └── enem_2024_amostra.csv
│   │
│   └── internal/                       // DADOS PROPRIOS DA ESCOLA
│       ├── output/                       
│       │   └── consolidado.csv         // DATASET GERADO PELA PIPELINE PARA SER CONSUMIDO PELA UI 
│       │
│       ├── alunos.csv
│       ├── ciencias_humanas.csv
│       ├── ciencias_natureza.csv
│       ├── linguagens.csv
│       ├── matematica.csv
│       └── professores.csv
│
├── src/
│   ├── backend/
│   │   ├── exp_dados_enem.ipynb       // SCRIPT PARA AMOSTRAGEM DOS DADOS DO ENEM
│   │   └── pipeline.ipynb             // PIPELINE PRINCIPAL PARA ETL, AGREGACOES, COMPARACOES, ETC  
│   │
│   └── ui/
│       └── app.py                     // PROJETO STREAMLIT
│
├── project-screenshots/               // CAPTURAS DE TELA DO SISTEMA RODANDO
│   └── screen-1.ong
│   └── screen-2.ong
│   └── screen-3.ong
│   └── screen-4.ong
│   └── screen-5.ong
│   └── screen-6.ong
│
├── venv/
├── .gitignore
├── DESCRICAO_DATASETS.md              // DESCRICAO DOS DADOS UTILIZADOS
├── README.md
└── requirements.txt                   // REQUERIMENTOS DO SISTEMA
```

<br />

---

## Autores
Beatriz Almeida de Souza Silva <br />
Paula Thifanny Gomes Dias