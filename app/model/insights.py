from app.config import connection

def getVendasMensais():
    try:
        conn = connection.getConnection(cursorType="dict")
        with conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        YEAR(data_venda) AS ano,
                        MONTH(data_venda) AS mes,
                        COUNT(venda_id) AS total_vendas
                    FROM vendas
                    GROUP BY YEAR(data_venda), MONTH(data_venda)
                    ORDER BY ano DESC, mes DESC
                """
                cursor.execute(query)
                result = cursor.fetchall()

                labels = [f"{item['mes']}/{item['ano']}" for item in result]
                values = [item['total_vendas'] for item in result]
                
                return {'labels': labels, 'values': values}
    except Exception as E:
        print(f"Erro ao consultar vendas mensais! [Erro: {E}]")
        return {'labels': [], 'values': []}



def getReceitaMensal():
    try:
        conn = connection.getConnection(cursorType="dict")
        with conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT
                        YEAR(v.data_venda) AS ano,
                        MONTH(v.data_venda) AS mes,
                        SUM(pv.preco_total) AS total_receita
                    FROM vendas v
                    JOIN produtos_venda pv ON v.venda_id = pv.venda_id
                    GROUP BY YEAR(v.data_venda), MONTH(v.data_venda)
                    ORDER BY ano DESC, mes DESC
                """
                cursor.execute(query)
                result = cursor.fetchall()

                labels = [f"{item['mes']}/{item['ano']}" for item in result]
                values = [item['total_receita'] for item in result]
                
                return {'labels': labels, 'values': values}
    except Exception as E:
        print(f"Erro ao consultar receita mensal! [Erro: {E}]")
        return {'labels': [], 'values': []}



def getVendasProdutos():
    try:
        conn = connection.getConnection(cursorType="dict")
        with conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT
                        p.nome AS produto,
                        SUM(pv.quantidade) AS total_vendido
                    FROM produtos_venda pv
                    JOIN produtos p ON pv.produto_id = p.produto_id
                    GROUP BY p.produto_id
                    ORDER BY total_vendido DESC
                """
                cursor.execute(query)
                result = cursor.fetchall()
                
                labels = [item['produto'] for item in result]
                values = [item['total_vendido'] for item in result]
                
                return {'labels': labels, 'values': values}
    except Exception as E:
        print(f"Erro ao consultar vendas por produto! [Erro: {E}]")
        return {'labels': [], 'values': []}



def getReceitaProdutos():
    try:
        conn = connection.getConnection(cursorType="dict")
        with conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        p.nome AS produto,
                        SUM(pv.preco_total) AS total_receita
                    FROM produtos_venda pv
                    JOIN produtos p ON pv.produto_id = p.produto_id
                    GROUP BY p.produto_id
                    ORDER BY total_receita DESC;
                """
                cursor.execute(query)
                result = cursor.fetchall()
                
                labels = [item['produto'] for item in result]
                values = [item['total_receita'] for item in result]
                
                return {'labels': labels, 'values': values}
    except Exception as E:
        print(f"Erro ao consultar receita por produto! [Erro: {E}]")
        return {'labels': [], 'values': []}



def getVendasUsuarios():
    try:
        conn = connection.getConnection(cursorType="dict")
        with conn:
            with conn.cursor() as cursor:
                query = """
                   SELECT 
                        u.nome AS usuario,
                        COUNT(v.venda_id) AS total_vendas
                    FROM vendas v
                    JOIN users u ON v.user_id = u.user_id
                    GROUP BY u.user_id
                    ORDER BY total_vendas DESC;
                """
                cursor.execute(query)
                result = cursor.fetchall()
                
                labels = [item['usuario'] for item in result]
                values = [item['total_vendas'] for item in result]
                
                return {'labels': labels, 'values': values}
    except Exception as E:
        print(f"Erro ao consultar vendas por usuário! [Erro: {E}]")
        return {'labels': [], 'values': []}



def getProdutosEstoque():
    try:
        conn = connection.getConnection(cursorType="dict")
        with conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        nome,
                        estoque
                    FROM produtos
                    ORDER BY estoque DESC;
                """
                cursor.execute(query)
                result = cursor.fetchall()
                
                labels = [item['nome'] for item in result]
                values = [item['estoque'] for item in result]
                
                return {'labels': labels, 'values': values}
    except Exception as E:
        print(f"Erro ao consultar produtos do estoque! [Erro: {E}]")
        return {'labels': [], 'values': []}



def getVendasDia():
    try:
        conn = connection.getConnection(cursorType="dict")
        with conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        DATE(data_venda) AS data,
                        COUNT(venda_id) AS total_vendas
                    FROM vendas
                    GROUP BY DATE(data_venda)
                    ORDER BY data DESC;
                """
                cursor.execute(query)
                result = cursor.fetchall()
                
                labels = [item['data'].strftime('%d/%m/%Y') for item in result]
                values = [item['total_vendas'] for item in result]
                
                return {'labels': labels, 'values': values}
    except Exception as E:
        print(f"Erro ao consultar vendas por dia! [Erro: {E}]")
        return {'labels': [], 'values': []}



def getReceitaDia():
    try:
        conn = connection.getConnection(cursorType="dict")
        with conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        DATE(v.data_venda) AS data,
                        SUM(pv.preco_total) AS total_receita
                    FROM vendas v
                    JOIN produtos_venda pv ON v.venda_id = pv.venda_id
                    GROUP BY DATE(v.data_venda)
                    ORDER BY data DESC;
                """
                cursor.execute(query)
                result = cursor.fetchall()
                
                labels = [item['data'].strftime('%d/%m/%Y') for item in result]
                values = [item['total_receita'] for item in result]
                
                return {'labels': labels, 'values': values}
    except Exception as E:
        print(f"Erro ao consultar receita por dia! [Erro: {E}]")
        return {'labels': [], 'values': []}


def getProdutosMaisVendidos():
    try:
        conn = connection.getConnection(cursorType="dict")
        with conn:
            with conn.cursor() as cursor:
                query = """
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
                """
                cursor.execute(query)
                result = cursor.fetchall()
                
                labels = [f"{item['produto']} ({item['mes']}/{item['ano']})" for item in result]
                values = [item['total_vendido'] for item in result]
                
                return {'labels': labels, 'values': values}
    except Exception as E:
        print(f"Erro ao consultar produtos mais vendidos por mes! [Erro: {E}]")
        return {'labels': [], 'values': []}
