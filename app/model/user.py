from app.config import connection
from app.utils import auth as authUser

def getUsers(user_id: int = None, email: str = None):
    if user_id is not None and email is not None:
        raise ValueError("Os parâmetros 'user_id' e 'email' não podem ser usados juntos.")
    
    try:
        conn = connection.getConnection()
        with conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM users"
                data = None

                if user_id is not None:
                    query += " WHERE user_id = %s"
                    data = (user_id,)

                elif email is not None:
                    query += " WHERE email = %s"
                    data = (email,)

                cursor.execute(query, data) if data else cursor.execute(query)

                return cursor.fetchone() if data else cursor.fetchall()

    except Exception as E:
        print(f"Erro ao consultar usuário no banco de dados! [Erro: {E}]")

def createUser(nome: str, email: str, senha: str):
    try:
        conn = connection.getConnection()
        conn.begin()
        with conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO users (
                        nome, email, senha
                    )
                    VALUES (
                        %s, %s, %s
                    )
                """
                
                hashPassword = authUser.hashPassword(senha)

                data = (nome, email, hashPassword)

                result = cursor.execute(query, data)
                if result > 0:
                    conn.commit()
                    print("Usuário criado com sucesso!")
                    return True

                else:
                    conn.rollback()
                    print("Erro ao criar usuário!")
                    return False
                
    except Exception as E:
        conn.rollback()
        print(f"Erro ao criar novo usuário! [Erro: {E}]")
        return False

def getPasswordHash(email: str = None):
    if email is not None:
        try:
            conn = connection.getConnection()
            with conn:
                with conn.cursor() as cursor:
                    query = """
                        SELECT senha
                        FROM users
                        WHERE email = %s
                    """ 

                    data = (email,)
                    cursor.execute(query, data)

                    result = cursor.fetchone()
                    if result is not None:
                        hash = result[0]
                        return hash

                    else:
                        print("Nenhum usuário encontrado!")
                        return None

        except Exception as E:
            print(f"Erro ao consultar hash de senha do usuário no banco de dados! [Erro: {E}]")

    else:
        raise ValueError("O parâmetro 'email' é obrigatório!")    



def getUsername(email: str):
    try:
        conn = connection.getConnection()
        with conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT nome
                    FROM users
                    WHERE email = %s
                """ 

                data = (email,)
                cursor.execute(query, data)

                result = cursor.fetchone()
                if result is not None:
                    username = result[0]
                    return username

                else:
                    print("Nenhum usuário encontrado!")
                    return None


    except Exception as E:
        print(f"Erro ao consultar nome de usuário! [Erro: {E}]")