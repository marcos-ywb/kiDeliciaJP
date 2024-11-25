import re

# Validar valores vazios
def emptyValue(value):
    return not value or value.strip() == ''

# Validar nome
def validateCompleteName(name):
    regex = r'^[a-zA-Z\s]+$'
    return re.match(regex, name) is not None

# Validar nome de produto
def validateProductName(name):
    regex = r'^[a-zA-Z0-9\s]+$'
    return re.match(regex, name) is not None

# Validar email
def validateEmail(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

# Validar senha
def validatePassword(password):
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'
    return re.match(regex, password) is not None

# Validar valores inteiros
def validateInt(number):
    regex = r'^\d+$'
    return re.match(regex, number) is not None

# Validar numeros de ponto flutuante
def validateFloat(number):
    regex = r'^\d+(\.\d+)?$'
    return re.match(regex, number) is not None

# Validar dados de cadastro
def validateSignupData(data):
    errors = {}
    try:
        if emptyValue(data['name']):
            errors['name'] = 'O nome é um campo obrigatório'

        elif not validateCompleteName(data['name']):
            errors['name'] = 'O campo "nome" deve conter apenas letras'

        if emptyValue(data['email']):
            errors['email'] = 'O email é um campo obrigatório'

        elif not validateEmail(data['email']):
            errors['email'] = 'Insira um email válido'

        if emptyValue(data['password']):
            errors['password'] = 'A senha é um campo obrigatório'

        elif not validatePassword(data['password']):
            errors['password'] = 'Senha deve ter no mínimo 8 caracteres, pelo menos uma letra maiúscula, uma letra minúscula e um número'

        if emptyValue(data['confirmPassword']):
            errors['confirmPassword'] = 'É necessário confirmar a senha!'

        elif data['password'] != data['confirmPassword']:
            errors['confirmPassword'] = 'As senhas não coincidem!'

    except KeyError as E:
        errors[E.args[0]] = 'Por favor, insira seu(a) ' + E.args[0]

    return errors

# Validar dados de login
def validateLoginData(data):
    errors = {}
    try:
        if emptyValue(data['email']):
            errors['email'] = 'O email é um campo obrigatório'

        elif not validateEmail(data['email']):
            errors['email'] = 'Insira um email válido'

        if emptyValue(data['password']):
            errors['password'] = 'A senha é um campo obrigatório'

        elif not validatePassword(data['password']):
            errors['password'] = 'Senha inválida'

    except KeyError as E:
        errors[E.args[0]] = 'Por favor, insira seu(a) ' + E.args[0]

    return errors



# Validar dados do novo produto
def validateNewProductData(data):
    errors = {}
    try:
        if emptyValue(data['nomeProduto']):
            errors['nomeProduto'] = 'O nome do produto é um campo obrigatório'

        elif not validateProductName(data['nomeProduto']):
            errors['nomeProduto'] = 'O campo "nome do produto" deve conter apenas letras e números'


        if emptyValue(data['precoProduto']):
            errors['precoProduto'] = 'O preço do produto é um campo obrigatório'

        elif not validateFloat(data['precoProduto']):
            errors['precoProduto'] = 'O campo "preço do produto" deve conter apenas numeros'


        if emptyValue(data['estoqueProduto']):
            errors['estoqueProduto'] = 'O estoque do produto é um campo obrigatório'

        elif not validateInt(data['estoqueProduto']):
            errors['estoqueProduto'] = 'O campo "estoque do produto" deve conter apenas numeros'


    except KeyError as E:
        errors[E.args[0]] = 'Por favor, insira seu(a) ' + E.args[0]

    return errors