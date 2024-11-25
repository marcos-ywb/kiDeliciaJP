from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
from markupsafe import Markup
from flask_session import Session

from app.model import user as modelUser
from app.model import produtos as modelProdutos
from app.model import vendas as modelVendas
from app.model import insights as modelInsights


from app.utils import validate
from app.utils import auth as userAuth
from app.utils import format as formatValues

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super secret key'

Session(app)

#============================================================================================================#
#======[    INDEX    ]=======================================================================================#
#============================================================================================================#
@app.route("/")
def index():
    return render_template(
        'index.html'
    )

#============================================================================================================#
#======[    AUTH    ]========================================================================================#
#============================================================================================================#
@app.route("/auth")
def auth():
    return render_template(
        'auth.html'
    )

#======[    SIGN UP    ]=====================================================================================#

@app.route("/trySignUp", methods=["POST"])
def trySignUp():
    data = {
        'name': request.form['nome'],
        'email': request.form['email'],
        'password': request.form['sign-up-password'],
        'confirmPassword': request.form['confirm-password']
    }

    errors = validate.validateSignupData(data)

    if errors:
        for field, error in errors.items():
            flash(Markup(f'{error}'), 'erro')
        return redirect(
            url_for('auth') + "#sign-up"
        )
    
    result = modelUser.createUser(data['name'], data['email'], data['password'])
    
    if result:
        flash("Cadastro realizado com sucesso!", "sucesso")
        return redirect(
            url_for('auth') + "#sign-in"
        )
    

#======[    SIGN IN    ]=====================================================================================#

@app.route("/trySignIn", methods=['POST'])
def trySignIn():
    data = {
        'email': request.form['email'],
        'password': request.form['sign-in-password']
    }

    errors = validate.validateLoginData(data)

    if errors:
        for field, error in errors.items():
            flash(Markup(f'{error}'), 'erro')
        return redirect(
            url_for('auth') + "#sign-in"
        )
    
    hash = modelUser.getPasswordHash(data['email'])
    if hash:
        verify = userAuth.checkPassword(data['password'], hash)
        if verify:
            session['user_logged'] = data['email']
            user  = modelUser.getUsers(email=data['email'])
            userData = {
                'user_id': user[0],
                'nome': user[1],
                'email': user[2]
            }
            
            flash(Markup(f"Seja Bem-Vindo(a), {userData['nome']}!"), 'sucesso')
            return redirect(
                url_for('home')
            )
        
        else:
            flash(Markup("Email e/ou senha incorretos!"), 'erro')
            return redirect(
                url_for('auth') + "#sign-in"
            )
        
    else:
        flash(Markup("Email incorreto ou inexistente!"), 'erro')
        return redirect(
            url_for('auth') + "#sign-in"
        )

#============================================================================================================#
#======[    HOME    ]========================================================================================#
#============================================================================================================#
@app.route("/home")
def home():
    if 'user_logged' in session:
        email = session['user_logged']
        user = modelUser.getUsers(email=email)

        if user is not None:
            userData = {
                'user_id': user[0],
                'nome': user[1],
                'email': user[2]
            }

            return render_template(
                'home.html',
                username = userData['nome']
            )
        
        else:
            flash(Markup("Usuário não encontrado!"), 'erro')
            return redirect(
                url_for('auth') + "#sign-in"
            )

    else:
        flash(Markup("Faça seu login para acessar!"), 'erro')
        return redirect(
            url_for('auth') + "#sign-in"
        )
    

#============================================================================================================#
#======[    PRODUTOS    ]====================================================================================#
#============================================================================================================#
@app.route("/produtos")
def produtos():
    if 'user_logged' in session:
        produtos = modelProdutos.getProdutos()
        formatCurrency = formatValues.formatCurrency
        disabledProdutos = modelProdutos.getDisabledProdutos()
        return render_template(
            'produtos.html',
            produtos = produtos,
            formatCurrency = formatCurrency,
            disabledProdutos = disabledProdutos
        )
    
    else:
        flash(Markup("Faça seu login para acessar!"), 'erro')
        return redirect(
            url_for('auth') + "#sign-in"
        )
    
#======[    TRY CREATE PRODUTO    ]==========================================================================#

@app.route("/tryCreateProduto", methods=["POST"])
def tryCreateProduto():
    data = {
        'nomeProduto': request.form['nomeProduto'],
        'precoProduto': request.form['precoProduto'],
        'estoqueProduto': request.form['estoqueProduto']
    }

    errors = validate.validateNewProductData(data)

    if errors:
        for field, error in errors.items():
            flash(Markup(f'{error}'), 'erro')
        return redirect(
            url_for('produtos')
        )

    result = modelProdutos.createProduto(data['nomeProduto'], data['precoProduto'], data['estoqueProduto'])
    if result:
        flash(Markup("Produto criado com sucesso!"), 'sucesso')
        return redirect(
            url_for('produtos')
        )
    
    else:
        flash(Markup("Erro ao criar produto!"), 'erro')
        return redirect(
            url_for('produtos')
        )


#======[    TRY DELETE PRODUTO    ]==========================================================================#

@app.route("/tryDisableProduto/<int:produto_id>", methods=["PATCH"])
def tryDisableProduto(produto_id):
    result = modelProdutos.disableProduto(produto_id)
    if result:
        response = {
            "message": "Produto desativado com sucesso!",
            "status": "success"
        }
        flash(Markup("Produto desativado com sucesso!"), 'sucesso')
        return jsonify(response), 200
    else:
        response = {
            "message": "Erro ao deletar produto!",
            "status": "error"
        }
        flash(Markup("Erro ao deletar produto!"), 'erro')
        return jsonify(response), 400
    

#======[    TRY ENABLE PRODUTO    ]==========================================================================#

@app.route("/tryEnableProduto/<int:produto_id>", methods=["PATCH"])
def tryEnableProduto(produto_id):
    result = modelProdutos.enableProduto(produto_id)
    if result:
        response = {
            "message": "Produto ativado com sucesso!",
            "status": "success"
        }
        flash(Markup("Produto ativado com sucesso!"), 'sucesso')
        return jsonify(response), 200
    else:
        response = {
            "message": "Erro ao ativar produto!",
            "status": "error"
        }
        flash(Markup("Erro ao ativar produto!"), 'erro')
        return jsonify(response), 400



#============================================================================================================#
#======[    VENDAS    ]======================================================================================#
#============================================================================================================#
@app.route("/vendas")
def vendas():
    if 'user_logged' in session:
        vendas = modelVendas.getVendas()
        formatDate = formatValues.formatDate
        funcionario = modelVendas.getFuncionario
        produtos = modelProdutos.getProdutos()
        formatCurrency = formatValues.formatCurrency
        return render_template(
            'vendas.html',
            vendas = vendas,
            formatDate = formatDate,
            formatCurrency = formatCurrency,
            funcionario = funcionario,
            produtos = produtos
        )
    
    else:
        flash(Markup("Faça seu login para acessar!"), 'erro')
        return redirect(
            url_for('auth') + "#sign-in"
        )
    

#======[    TRY NEW VENDA    ]===============================================================================#

@app.route('/tryNewVenda', methods=['POST'])
def tryNewVenda():
    try:
        user_id = modelUser.getUsers(email = session['user_logged'])[0]
        if not user_id:
            flash(Markup("Usuário nao encontrado!"), 'erro')
            return redirect(
                url_for('vendas')
            )
        
        produtos = request.form.getlist('produto[]')
        quantidades = request.form.getlist('quantidade[]')
        precos = request.form.getlist('preco[]')
        print(f"Produtos: {produtos}, Quantidades: {quantidades}, Preços: {precos}")

        if not produtos or not quantidades or not precos:
            flash(Markup("Dados incompletos no formulário!"), 'erro')
            return redirect(
                url_for('vendas')
            )
        
        produto_ids = [int(p) for p in produtos]
        qtds = [int(q) for q in quantidades]
        if not modelVendas.checkEstoque(produto_ids, qtds):
            flash(Markup("Estoque insuficiente para alguns produtos!"), 'erro')
            return redirect(
                url_for('vendas')
            )        
        
        produtos_venda = []
        for produto_id, quantidade, preco in zip(produtos, quantidades, precos):
            produto_venda = {
                "produto_id": int(produto_id),
                "quantidade": int(quantidade),
                "preco_total": float(preco) * int(quantidade)
            }
            produtos_venda.append(produto_venda)


        result = modelVendas.createVenda(user_id, produtos_venda)

        flash(Markup("Venda registrada com sucesso!"), "sucesso")
        return redirect(
            url_for('vendas', venda_id = result)
        )
    
    except Exception as E:
        print(f"Erro ao registrar venda! [Erro: {E}]")
        return jsonify(
            {
                "error": "Erro ao registrar venda!"
            }
        ), 500
    

#============================================================================================================#
#======[    INSIGHTS    ]====================================================================================#
#============================================================================================================#
@app.route("/insights")
def insights():
    if 'user_logged' in session:
        return render_template(
            'insights.html'
        )

    else:
        flash(Markup("Faça seu login para acessar!"), 'erro')
        return redirect(
            url_for('auth') + "#sign-in"
        )
        

#======[    FILTER INSIGHT    ]==============================================================================#

@app.route("/filterInsight", methods=["POST"])
def filterInsight():
    inputFilter = request.json.get('categoria-filtro', None)
    if inputFilter:

        match inputFilter:

            #Vendas Mensais
            case "vendas-mensais":
                data = modelInsights.getVendasMensais()

            #Receita Mensal
            case "receita-mensal":
                data = modelInsights.getReceitaMensal()
            
            case "vendas-diarias":
                data = modelInsights.getVendasDia()


            case "receita-diaria":
                data = modelInsights.getReceitaDia()


            case "vendas-produto":
                data = modelInsights.getVendasProdutos()

            
            case "receita-produto":
                data = modelInsights.getReceitaProdutos()


            case "produtos-estoque":
                data = modelInsights.getProdutosEstoque()


            case "produtos-mais-vendidos":
                data = modelInsights.getProdutosMaisVendidos()


            case "vendas-usuario":
                data = modelInsights.getVendasUsuarios()


            #Nenhuma categoria
            case _:
                return jsonify(
                    {
                        "erro": f"Categoria {inputFilter} nao encontrada!"
                    }
                ), 404
            

        if data and isinstance(data, dict) and all(k in data for k in ["labels", "values"]):
            print(f"Dados enviados: {data}")
            return jsonify(data)
        
        else:
            return jsonify(
                {
                    "erro": "Dados invalidos!"
                }
            ), 500

    else:
        return jsonify(
            {
                "erro": "Filtro invalido!"
            }
        ), 400      



#============================================================================================================#
#======[    REPORTS    ]=====================================================================================#
#============================================================================================================#
@app.route("/reports")
def reports():
    if 'user_logged' in session:
        return render_template(
            'reports.html'
        )

    else:
        flash(Markup("Faça seu login para acessar!"), 'erro')
        return redirect(
            url_for('auth') + "#sign-in"
        )


#============================================================================================================#
#======[    LOGOUT    ]======================================================================================#
#============================================================================================================#
@app.route("/logOut")
def logOut():
    session.pop('user_logged', None)
    flash(Markup("Logout realizado com sucesso!"), "sucesso")

    return redirect(
        url_for('auth') + "#sign-in"
    )
    
#============================================================================================================#
#======[    RUN    ]=========================================================================================#
#============================================================================================================#
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )