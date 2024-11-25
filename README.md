# kiDeliciaJP

> Uma aplicação WEB leve e escalonável construída com Flask, Flask_Session e PyMySQL. Fornece um sistema de autenticação de usuários seguro com hashing de senhas usando bcrypt e insights detalhados sobre a venda de produtos, garantindo uma vantagem competitiva no mercados.

## Conteúdo
- [Recursos](#recursos)
- [Requisitos](#requisitos)
- [Instalação](#instalação)

---
## Recursos
- **Registro de Usuário**: Permite que novos usuários se registrem com uma senha segura.
- **Login de usuário**: Autentica usuários e estabelece sessões.
- **Gerenciamento de sessões**: Gerencia sessões de usuários com segurança usando Flask-Session.
- **Hashing de senha**: Usa bcrypt para hashing e validação de senha.
- **Insights detalhados**: Fornece diversos insights baseados nos registros do banco de dados.

## Requisitos
- Python 3.8+
- Flask
- Flask-Session
- PyMySQL
- bcrypt
- MySQL database

## Instalação

Siga as etapas abaixo para configurar e executar o projeto em sua máquina local:

### 1. Faça o Download do projeto

Para baixar apenas a versão mais recente do projeto (sem o histórico completo de commits), [clique aqui](https://github.com/marcos-ywb/kiDeliciaJP/archive/refs/heads/main.zip) para baixar o código-fonte código como um arquivo ZIP. Extraia o conteúdo para um diretório em sua máquina.

Alternativamente, você pode usar `git clone` para baixar apenas o commit mais recente:

```bash
git clone --depth 1 https://github.com/marcos-ywb/kiDeliciaJP.git
cd kiDeliciaJP
```

### 2. Crie e ative um ambiente virtual

Para uma configuração mais limpa, crie e ative um ambiente virtual:
```bash
python3 -m venv venv

source venv/bin/activate # No Linux/macOS
venv\Scripts\activate # No Windows: 
```

### 3. Instalar dependências

Com o ambiente virtual ativo, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 4. Crie o banco de dados

É necessário criar manualmente as tabelas do banco de dados disponibilizado no diretório do projeto. (`[DATABASE]/database.sql`)

### 5. Configure o projeto

Abra o arquivo de configuração de conexão com o banco de dados (`app/config/connection.py`) e atualize as seguintes configurações:

```python
host="host",
user="usuário",
password="senha",
database="kiDeliciaJP"
```
- Substitua `host`, `user`, `password` e `database` pelas credenciais do seu banco de dados MySQL.

### 6. Rode o projeto
```bash
python main.py
```

A aplicação estará disponível em `http://127.0.0.1:5000/` por padrão.
