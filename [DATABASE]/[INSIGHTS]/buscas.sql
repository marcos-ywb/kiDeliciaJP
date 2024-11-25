/*Vendas mensais*/
SELECT 
    YEAR(data_venda) AS ano,
    MONTH(data_venda) AS mes,
    COUNT(venda_id) AS total_vendas
FROM vendas
GROUP BY YEAR(data_venda), MONTH(data_venda)
ORDER BY ano DESC, mes DESC;

/*Receita total por mes*/
SELECT 
    YEAR(v.data_venda) AS ano,
    MONTH(v.data_venda) AS mes,
    SUM(pv.preco_total) AS total_receita
FROM vendas v
JOIN produtos_venda pv ON v.venda_id = pv.venda_id
GROUP BY YEAR(v.data_venda), MONTH(v.data_venda)
ORDER BY ano DESC, mes DESC;


/*Vendas por produtos*/
SELECT 
    p.nome AS produto,
    SUM(pv.quantidade) AS total_vendido
FROM produtos_venda pv
JOIN produtos p ON pv.produto_id = p.produto_id
GROUP BY p.produto_id
ORDER BY total_vendido DESC;



/*Receita por produto*/
SELECT 
    p.nome AS produto,
    SUM(pv.preco_total) AS total_receita
FROM produtos_venda pv
JOIN produtos p ON pv.produto_id = p.produto_id
GROUP BY p.produto_id
ORDER BY total_receita DESC;


/*Vendas por usuarios*/
SELECT 
    u.nome AS usuario,
    COUNT(v.venda_id) AS total_vendas
FROM vendas v
JOIN users u ON v.user_id = u.user_id
GROUP BY u.user_id
ORDER BY total_vendas DESC;


/*Produtos em estoque*/
SELECT 
    nome,
    estoque
FROM produtos
ORDER BY estoque DESC;


/*Vendas por dia*/
SELECT 
    DATE(data_venda) AS data,
    COUNT(venda_id) AS total_vendas
FROM vendas
GROUP BY DATE(data_venda)
ORDER BY data DESC;


/*Receita por dia*/
SELECT 
    DATE(v.data_venda) AS data,
    SUM(pv.preco_total) AS total_receita
FROM vendas v
JOIN produtos_venda pv ON v.venda_id = pv.venda_id
GROUP BY DATE(v.data_venda)
ORDER BY data DESC;


/*Produtos mais vendidos*/
SELECT 
    YEAR(v.data_venda) AS ano,
    MONTH(v.data_venda) AS mes,
    p.nome AS produto,
    SUM(pv.quantidade) AS total_vendido
FROM vendas v
JOIN produtos_venda pv ON v.venda_id = pv.venda_id
JOIN produtos p ON pv.produto_id = p.produto_id
GROUP BY YEAR(v.data_venda), MONTH(v.data_venda), p.produto_id
ORDER BY total_vendido DESC;


/*Vendas por status*/
SELECT 
    p.status AS status_produto,
    COUNT(v.venda_id) AS total_vendas
FROM vendas v
JOIN produtos_venda pv ON v.venda_id = pv.venda_id
JOIN produtos p ON pv.produto_id = p.produto_id
GROUP BY p.status
ORDER BY total_vendas DESC;
