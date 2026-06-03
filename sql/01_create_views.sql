DROP VIEW IF EXISTS vw_faturamento_mensal;

CREATE VIEW vw_faturamento_mensal AS
SELECT
    strftime('%Y-%m', data_pedido) AS ano_mes,
    count(pedido_id)               AS total_pedidos,
    ROUND(SUM(valor_total), 2)     AS faturamento,
    ROUND(AVG(valor_total), 2)     AS ticket_medio
FROM pedidos
WHERE status = 'concluído'
GROUP BY ano_mes
ORDER BY ano_mes;

DROP VIEW IF EXISTS vw_top_produtos;

CREATE VIEW vw_top_produtos AS
SELECT
    p.nome,
    p.categoria,
    SUM(i.quantidade)         AS unidades_vendidas,
    ROUND(SUM(i.subtotal), 2) AS faturamento
FROM itens_pedido i
JOIN produtos p  ON i.produto_id = p.produto_id
JOIN pedidos  pe ON i.pedido_id  = pe.pedido_id
WHERE pe.status = 'concluído'
GROUP BY p.produto_id
ORDER BY faturamento DESC
LIMIT 10;


DROP VIEW IF EXISTS vw_vendas_por_regiao;

CREATE VIEW vw_vendas_por_regiao AS
SELECT
    c.regiao,
    c.estado,
    COUNT(pe.pedido_id)             as total_pedidos,
    ROUND(sum(pe.valor_total), 2 )  as faturamento
from pedidos pe
JOIN clientes c ON pe.cliente_id = c.cliente_id
where pe.STATUS = 'concluído'
group by c.regiao, c.estado
ORDER BY faturamento DESC;


DROP VIEW IF EXISTS vw_vendas_por_canal;

CREATE view vw_vendas_por_canal as 
SELECT
    canal_venda,
    count(pedido_id)        as total_pedidos,
    ROUND(sum(valor_total), 2) as faturamento
from pedidos
where status = 'concluído'
GROUP BY canal_venda
ORDER BY faturamento DESC
