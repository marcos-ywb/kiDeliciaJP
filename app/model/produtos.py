from app.config import connection

def getProdutos(produto_id: int = None):
    try:
        conn = connection.getConnection()
        with conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM produtos WHERE status = 1"
                data = None

                if produto_id is not None:
                    query += " AND produto_id = %s"
                    data = (produto_id,)

                cursor.execute(query, data) if data else cursor.execute(query)

                return cursor.fetchone() if data else cursor.fetchall()
            
    except Exception as E:
        print(f"Erro ao consultar produto no banco de dados! [Erro: {E}]")



def createProduto(nome: str, preco: float, estoque: int):
    try:
        conn = connection.getConnection()
        conn.begin()
        with conn:
            with conn.cursor() as cursor:
                query = """
                        INSERT INTO produtos (
                            nome, preco, estoque
                        )
                        VALUES (
                            %s, %s, %s
                        )
                    """
                
                data = (nome, preco, estoque)
                cursor.execute(query, data)

                if conn.affected_rows() > 0:
                    conn.commit()
                    print("Produto criado com sucesso!")
                    return True

                else:
                    conn.rollback()
                    print("Erro ao criar produto!")
                    return False
                
    except Exception as E:
        conn.rollback()
        print(f"Erro ao criar produto! [Erro: {E}]")
        return False
    


def disableProduto(produto_id: int):
    try:
        conn = connection.getConnection()
        with conn:
            conn.begin()
            with conn.cursor() as cursor:
                query = """
                    UPDATE produtos
                    SET status = 0
                    WHERE produto_id = %s          
                """

                data = (produto_id,)
                cursor.execute(query, data)

                if conn.affected_rows() > 0:
                    conn.commit()
                    print("Produto desativado com sucesso!")
                    return True

                else:
                    conn.rollback()
                    print("Erro ao desativar produto!")
                    return False
                
    except Exception as E:
        conn.rollback()
        print(f"Erro ao deletar produto! [Erro: {E}]")
        return False
    
def enableProduto(produto_id: int):
    try:
        conn = connection.getConnection()
        with conn:
            conn.begin()
            with conn.cursor() as cursor:
                query = """
                    UPDATE produtos
                    SET status = 1
                    WHERE produto_id = %s          
                """

                data = (produto_id,)
                cursor.execute(query, data)

                if conn.affected_rows() > 0:
                    conn.commit()
                    print("Produto ativado com sucesso!")
                    return True

                else:
                    conn.rollback()
                    print("Erro ao ativar produto!")
                    return False
                
    except Exception as E:
        conn.rollback()
        print(f"Erro ao deletar produto! [Erro: {E}]")
        return False
    
    


def getDisabledProdutos():
    try:
        conn = connection.getConnection()
        with conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT *
                    FROM produtos
                    WHERE status = 0
                """

                cursor.execute(query)

                return cursor.fetchall()

    except Exception as E:
        print(f"Erro ao consultar produtos desativados! [Erro: {E}]")