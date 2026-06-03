# 📊 Pipeline de Análise de Vendas — E-commerce

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?logo=powerbi&logoColor=black)

> Pipeline completo de dados simulando o fluxo de um e-commerce real: da geração dos dados até o dashboard analítico.

---

##  Dashboard

![Dashboard de Vendas](powerbi\screenshots\dashboard.jpg)

---

##  Sobre o projeto

Este projeto simula o pipeline de dados de um e-commerce com 2 anos de histórico de vendas. O objetivo é demonstrar a capacidade de estruturar um fluxo completo de dados — desde a geração e limpeza até a modelagem em banco de dados e visualização em dashboard.

O dashboard responde perguntas de negócio como:
- Qual o faturamento mensal e a tendência ao longo do tempo?
- Quais são os 10 produtos que mais geram receita?
- Qual canal de venda (site, app, marketplace, loja física) performa melhor?
- Qual o ticket médio dos pedidos concluídos?

---

## Arquitetura

```
Faker (dados fictícios)
        ↓
  data/raw/*.csv
        ↓
  ETL com Python (Pandas)
        ↓
  SQLite (database.db)
        ↓
  Views SQL analíticas
        ↓
  data/processed/*.csv
        ↓
  Dashboard Power BI
```

---

##  Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python 3.14 | ETL, geração de dados |
| Pandas | Limpeza e transformação |
| Faker | Geração de dados fictícios |
| SQLite | Banco de dados |
| SQL | Modelagem e views analíticas |
| Power BI | Dashboard e visualizações |

---

##  Como rodar

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/sales-pipeline-analysis.git
cd sales-pipeline-analysis
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Gere os dados fictícios**
```bash
python src/generate_data.py
```

**4. Rode o pipeline ETL**
```bash
python src/etl.py
```

Os CSVs processados estarão em `data/processed/` prontos para importar no Power BI.

---

##  Estrutura de pastas

```
sales-pipeline-analysis/
├── data/
│   ├── raw/              # CSVs gerados pelo Faker
│   └── processed/        # Views exportadas para o Power BI
├── notebooks/
│   ├── 01_data_generation.ipynb
│   ├── 02_eda.ipynb
│   └── 03_etl_pipeline.ipynb
├── sql/
│   └── 01_create_views.sql   # Views analíticas
├── src/
│   ├── generate_data.py      # Geração de dados fictícios
│   └── etl.py                # Pipeline ETL
├── powerbi/
│   ├── dashboard_vendas.pbix
│   └── screenshots/
├── requirements.txt
└── README.md
```

---

##  Views SQL criadas

| View | Descrição |
|------|-----------|
| `vw_faturamento_mensal` | Faturamento, pedidos e ticket médio por mês |
| `vw_top_produtos` | Top 10 produtos por receita |
| `vw_vendas_por_regiao` | Faturamento por estado e região |
| `vw_vendas_por_canal` | Comparativo entre canais de venda |

---

##  Contato

Feito por **Filipe Filgueira**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Filipe%20Filgueira-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/filipe-filgueira/)
