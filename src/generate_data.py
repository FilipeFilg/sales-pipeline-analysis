"""
generate_data.py
================
Geração de dados fictícios de vendas para o projeto de portfólio.
Gera 4 arquivos CSV: clientes, produtos, pedidos e itens_pedido.

Dependências:
    pip install faker pandas

Uso:
    python generate_data.py
"""

import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import os

#  Configurações 
fake = Faker("pt_BR")
random.seed(42)
Faker.seed(42)

NUM_CLIENTES  = 500
NUM_PRODUTOS  = 80
NUM_PEDIDOS   = 3000

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

#  Dados de referência 
CATEGORIAS = {
    "Eletrônicos":    (150.0,  4500.0),
    "Vestuário":      (29.90,  399.90),
    "Casa & Jardim":  (19.90,  899.90),
    "Esportes":       (39.90,  1299.90),
    "Beleza":         (12.90,  299.90),
    "Livros":         (19.90,  149.90),
    "Brinquedos":     (24.90,  599.90),
    "Alimentos":      (8.90,   129.90),
}

STATUS_PEDIDO = ["concluído", "enviado", "processando", "cancelado"]
STATUS_PESO   = [0.60,        0.20,      0.12,          0.08]

FORMAS_PAGAMENTO = ["cartão crédito", "cartão débito", "pix", "boleto"]
PAGAMENTO_PESO   = [0.45,             0.20,            0.25,  0.10]

REGIOES = {
    "SP": "Sudeste", "RJ": "Sudeste", "MG": "Sudeste", "ES": "Sudeste",
    "RS": "Sul",     "SC": "Sul",     "PR": "Sul",
    "BA": "Nordeste","PE": "Nordeste","CE": "Nordeste","MA": "Nordeste",
    "AM": "Norte",   "PA": "Norte",   "RO": "Norte",
    "GO": "Centro-Oeste","MT":"Centro-Oeste","MS":"Centro-Oeste","DF":"Centro-Oeste",
}

# 1. Clientes 
def gerar_clientes(n: int) -> pd.DataFrame:
    registros = []
    for i in range(1, n + 1):
        estado = random.choice(list(REGIOES.keys()))
        registros.append({
            "cliente_id":    i,
            "nome":          fake.name(),
            "email":         fake.email(),
            "telefone":      fake.phone_number(),
            "cidade":        fake.city(),
            "estado":        estado,
            "regiao":        REGIOES[estado],
            "data_cadastro": fake.date_between(start_date="-4y", end_date="today").strftime("%Y-%m-%d"),
            "genero":        random.choice(["M", "F", "Outro"]),
            "idade":         random.randint(18, 75),
        })
    return pd.DataFrame(registros)


#  2. Produtos
NOMES_PRODUTO = [
    "Pro", "Ultra", "Max", "Elite", "Basic", "Smart", "Eco", "Plus",
    "Mini", "Grande", "Premium", "Lite", "Turbo", "Neo", "Air",
]

def gerar_nome_produto(categoria: str) -> str:
    adjetivo = random.choice(NOMES_PRODUTO)
    sufixo   = fake.word().capitalize()
    return f"{adjetivo} {sufixo} {categoria.split()[0]}"

def gerar_produtos(n: int) -> pd.DataFrame:
    registros = []
    for i in range(1, n + 1):
        categoria         = random.choice(list(CATEGORIAS.keys()))
        preco_min, preco_max = CATEGORIAS[categoria]
        preco_custo       = round(random.uniform(preco_min * 0.4, preco_max * 0.5), 2)
        preco_venda       = round(preco_custo * random.uniform(1.4, 2.8), 2)
        registros.append({
            "produto_id":     i,
            "nome":           gerar_nome_produto(categoria),
            "categoria":      categoria,
            "preco_custo":    preco_custo,
            "preco_venda":    preco_venda,
            "margem_pct":     round((preco_venda - preco_custo) / preco_venda * 100, 1),
            "estoque":        random.randint(0, 500),
            "ativo":          random.choices([True, False], weights=[0.90, 0.10])[0],
            "fornecedor":     fake.company(),
        })
    return pd.DataFrame(registros)


# 3. Pedidos
def gerar_pedidos(n: int, clientes: pd.DataFrame) -> pd.DataFrame:
    data_inicio = datetime.now() - timedelta(days=365 * 2)
    registros   = []
    for i in range(1, n + 1):
        data_pedido = fake.date_time_between(start_date=data_inicio, end_date="now")
        status      = random.choices(STATUS_PEDIDO, STATUS_PESO)[0]

        # data de entrega só existe se não estiver processando/cancelado
        if status == "concluído":
            data_entrega = (data_pedido + timedelta(days=random.randint(1, 15))).strftime("%Y-%m-%d")
        elif status == "enviado":
            data_entrega = None
        else:
            data_entrega = None

        registros.append({
            "pedido_id":       i,
            "cliente_id":      random.choice(clientes["cliente_id"].tolist()),
            "data_pedido":     data_pedido.strftime("%Y-%m-%d"),
            "hora_pedido":     data_pedido.strftime("%H:%M:%S"),
            "status":          status,
            "forma_pagamento": random.choices(FORMAS_PAGAMENTO, PAGAMENTO_PESO)[0],
            "frete":           round(random.uniform(0, 49.90), 2),
            "desconto_pct":    random.choices([0, 5, 10, 15, 20], weights=[0.5, 0.2, 0.15, 0.1, 0.05])[0],
            "data_entrega":    data_entrega,
            "canal_venda":     random.choice(["site", "app", "marketplace", "loja física"]),
        })
    return pd.DataFrame(registros)


#  4. Itens do pedido 
def gerar_itens(pedidos: pd.DataFrame, produtos: pd.DataFrame) -> pd.DataFrame:
    registros = []
    item_id   = 1
    for _, pedido in pedidos.iterrows():
        n_itens = random.choices([1, 2, 3, 4, 5], weights=[0.45, 0.30, 0.15, 0.07, 0.03])[0]
        produtos_escolhidos = produtos.sample(n_itens)
        for _, prod in produtos_escolhidos.iterrows():
            quantidade  = random.randint(1, 5)
            preco_unit  = prod["preco_venda"]
            subtotal    = round(quantidade * preco_unit, 2)
            registros.append({
                "item_id":    item_id,
                "pedido_id":  pedido["pedido_id"],
                "produto_id": prod["produto_id"],
                "quantidade": quantidade,
                "preco_unit": preco_unit,
                "subtotal":   subtotal,
            })
            item_id += 1
    return pd.DataFrame(registros)


#  5. Calcular valor_total nos pedidos 
def adicionar_totais(pedidos: pd.DataFrame, itens: pd.DataFrame) -> pd.DataFrame:
    totais = itens.groupby("pedido_id")["subtotal"].sum().reset_index()
    totais.rename(columns={"subtotal": "subtotal_produtos"}, inplace=True)
    pedidos = pedidos.merge(totais, on="pedido_id", how="left")
    pedidos["desconto_valor"] = round(
        pedidos["subtotal_produtos"] * pedidos["desconto_pct"] / 100, 2
    )
    pedidos["valor_total"] = round(
        pedidos["subtotal_produtos"] - pedidos["desconto_valor"] + pedidos["frete"], 2
    )
    return pedidos


#  Main
if __name__ == "__main__":
    print("Gerando dados fictícios de vendas...\n")

    print(f"  [1/4] Clientes ({NUM_CLIENTES})")
    clientes = gerar_clientes(NUM_CLIENTES)
    clientes.to_csv(f"{OUTPUT_DIR}/clientes.csv", index=False, encoding="utf-8")

    print(f"  [2/4] Produtos ({NUM_PRODUTOS})")
    produtos = gerar_produtos(NUM_PRODUTOS)
    produtos.to_csv(f"{OUTPUT_DIR}/produtos.csv", index=False, encoding="utf-8")

    print(f"  [3/4] Pedidos ({NUM_PEDIDOS})")
    pedidos = gerar_pedidos(NUM_PEDIDOS, clientes)

    print(f"  [4/4] Itens do pedido")
    itens = gerar_itens(pedidos, produtos)
    pedidos = adicionar_totais(pedidos, itens)

    pedidos.to_csv(f"{OUTPUT_DIR}/pedidos.csv",      index=False, encoding="utf-8")
    itens.to_csv(  f"{OUTPUT_DIR}/itens_pedido.csv", index=False, encoding="utf-8")

    # ── Resumo─
    print("\n✓ Arquivos salvos em data/raw/\n")
    print("─" * 40)
    print(f"  clientes.csv      → {len(clientes):>6} linhas")
    print(f"  produtos.csv      → {len(produtos):>6} linhas")
    print(f"  pedidos.csv       → {len(pedidos):>6} linhas")
    print(f"  itens_pedido.csv  → {len(itens):>6} linhas")
    print("─" * 40)
    print(f"\n  Faturamento total gerado: R$ {pedidos['valor_total'].sum():,.2f}")
    print(f"  Ticket médio:             R$ {pedidos['valor_total'].mean():,.2f}")
    print(f"  Pedidos concluídos:       {(pedidos['status'] == 'concluído').sum()}")