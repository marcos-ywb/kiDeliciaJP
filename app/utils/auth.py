from bcrypt import (
    hashpw,
    checkpw,
    gensalt
)

def hashPassword(senha):
    hash = hashpw(senha.encode('utf-8'), gensalt())
    return hash

def checkPassword(senha, hash):
    result = checkpw(senha.encode('utf-8'), hash.encode('utf-8'))
    return result
