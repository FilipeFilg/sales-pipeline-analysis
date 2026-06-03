import pandas as pd
import sqlite3
import os

# CAMINHOS
RAW_DIR = "data/raw"
DB_PATH = "data/database.db"


# Conexão com o banco
conn = sqlite3.connect(DB_PATH)
print("Conexão com o banco estabelecida!")

# Carregar os CSVs
clientes = pd.read_csv(f"{RAW_DIR}/clientes.csv")
produtos = pd.read_csv(f"{RAW_DIR}/produtos.csv")
pedidos = pd.read_csv(f"{RAW_DIR}/pedidos.csv")
itens = pd.read_csv(f"{RAW_DIR}/itens_pedido.csv")

print(f"Clientes {len(clientes)} linhas")
print(f"Produtos {len(produtos)} linhas")
print(f"Pedidos {len(pedidos)} linhas")
print(f"Itens {len(itens)} linhas")

clientes["data_cadastro"] = pd.to_datetime(clientes["data_cadastro"])
pedidos["data_pedido"] = pd.to_datetime(pedidos["data_pedido"], errors="coerce")

print("Nulos em pedidos: ")
print(pedidos.isnull().sum())

clientes.to_sql("clientes",  conn, if_exists="replace", index=False)
produtos.to_sql("produtos",  conn, if_exists="replace", index=False)
pedidos.to_sql("pedidos",    conn, if_exists="replace", index=False)
itens.to_sql("itens_pedido", conn, if_exists="replace", index=False)

with open("sql/01_create_views.sql", "r", encoding="utf-8") as f:
    sql = f.read()

conn.executescript(sql)
print("Views Criadas!")

resultado = pd.read_sql("Select * FROM vw_faturamento_mensal LIMIT 5", conn)

os.makedirs("data/processed", exist_ok=True)

views = [
    "vw_faturamento_mensal",
    "vw_top_produtos",
    "vw_vendas_por_regiao",
    "vw_vendas_por_canal",
]

for view in views:
    df = pd.read_sql(f"SELECT * FROM {view}", conn)
    df.to_csv(f"data/processed/{view}.csv", index=False, encoding="utf-8")
    print(f"Exportado: {view}.csv")

conn.close()
print("ETL Concluido")