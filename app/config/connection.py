import pymysql as mysql
from pymysql.cursors import DictCursor, Cursor

def getConnection(cursorType=None):
    try:
        if cursorType is not None:
            if cursorType == "dict":
                cursorType = DictCursor
            elif cursorType == "tuple":
                cursorType = Cursor
            else:
                cursorType = Cursor
        else:
            cursorType = Cursor

        conn = mysql.connect(
            host="host",
            user="usuario",
            password="senha",
            database="kiDeliciaJP",
            cursorclass=cursorType
        )
        return conn
    except Exception as E:
        print(f"Erro ao conectar-se ao banco de dados! [Erro: {E}]")