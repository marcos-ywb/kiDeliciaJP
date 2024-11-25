from app.config import connection

def getVendas(venda_id: int = None):
    try:
        conn = connection.getConnection()
        with conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT
                        v.venda_id,
                        v.data_venda,
                        u.user_id,
                        u.nome AS nome_funcionario,
                        GROUP_CONCAT(
                            CONCAT(
                                p.nome,
                                ' (<b>', pv.quantidade, 'x</b>)'
                            ) SEPARATOR ', '
                        ) AS quantidade_produtos,
                        SUM(pv.preco_total) AS preco_total,

                        JSON_ARRAYAGG(
                            JSON_OBJECT(
                                'produto', p.nome,
                                'preco_unitario', p.preco,
                                'quantidade', pv.quantidade
                            )
                        ) AS detalhes_produtos
                    FROM vendas v
                    JOIN produtos_venda pv ON v.venda_id = pv.venda_id
                    JOIN produtos p ON pv.produto_id = p.produto_id
                    JOIN users u ON v.user_id = u.user_id
                    GROUP BY v.venda_id;

                """
                data = None

                if venda_id is not None:
                    query += " HAVING v.venda_id = %s"
                    data = (venda_id,)

                cursor.execute(query, data) if data else cursor.execute(query)

                return cursor.fetchone() if data else cursor.fetchall()

    except Exception as E:
        print(f"Erro ao consultar venda! [Erro: {E}]")




def getFuncionario(user_id: int):
    try:
        conn = connection.getConnection()
        with conn:
            with conn.cursor() as cursor:
                query = "SELECT nome FROM users WHERE user_id = %s"
                data = (user_id,)
                cursor.execute(query, data)

                return cursor.fetchone()[0]
            
    except Exception as E:
        print(f"Erro ao consultar funcionário! [Erro: {E}]")


def updateEstoque(produto_id: int, quantidade: int):
    try:
        conn = connection.getConnection()
        with conn:
            conn.begin()
            with conn.cursor() as cursor:
                query = """
                    UPDATE produtos
                    SET estoque = estoque - %s
                    WHERE produto_id = %s
                """
                data = (quantidade, produto_id)

                cursor.execute(query, data)

                if conn.affected_rows() > 0:
                    conn.commit()
                    print("Estoque atualizado com sucesso!")
                    return False

                else:
                    conn.rollback()
                    print("Erro ao atualizar estoque!")
                    return False


    except Exception as E:
        conn.rollback()
        print(f"Erro ao atualizar estoque! [Erro: {E}]")
        return False
    


def checkEstoque(produto_id: list[int], quantidade: list[int]) -> bool:
    try:
        conn = connection.getConnection()
        with conn:
            with conn.cursor() as cursor:
                for produto_id, quantidade in zip(produto_id, quantidade):
                    query = """
                        SELECT estoque 
                        FROM produtos
                        WHERE produto_id = %s
                    """

                    data = (produto_id,)
                    cursor.execute(query, data)

                    estoque = cursor.fetchone()
                    if not estoque:
                        print(f"Produto {produto_id} nao encontrado!")
                        return False
                    
                    if estoque[0] < quantidade:
                        print(f"Estoque insuficiente para o produto {produto_id}!")
                        return False
        return True
    except Exception as E:
        print(f"Erro ao consultar estoque! [Erro: {E}]")
    
    

def createVenda(user_id: int, produtos):
    try:
        conn = connection.getConnection()
        with conn:
            conn.begin()
            with conn.cursor() as cursor:
                queryUser = """
                    INSERT INTO vendas (
                        user_id
                    )
                    VALUES (
                        %s
                    )
                """

                dataUser = (user_id,)
                cursor.execute(queryUser, dataUser)

                venda_id = cursor.lastrowid

                for produto in produtos:
                    queryVenda = """
                        INSERT INTO produtos_venda (
                            venda_id, produto_id, quantidade, preco_total
                        )
                        VALUES (
                            %s, %s, %s, %s
                        )
                    """

                    updateEstoque(produto['produto_id'], produto['quantidade'])

                    dataVenda = (venda_id, produto['produto_id'], produto['quantidade'], produto['preco_total'],)

                    cursor.execute(queryVenda, dataVenda)

                conn.commit()
                return venda_id
            
    except Exception as E:
        conn.rollback()
        print(f"Erro ao criar venda! [Erro: {E}]")
        return False