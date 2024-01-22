from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dados temporários para simular o login
usuarios_cadastrados = [
    {'nome': 'Usuario1', 'email': 'usuario1@email.com', 'senha': 'senha123'},
    # Adicione mais usuários conforme necessário
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/pagina_pessoal')
def pagina_pessoal():
    return render_template('pagina_pessoal.html')

@app.route('/login', methods=['POST'])
def login():
    # Verificar se o usuário existe (simulação simples)
    # Em uma aplicação real, você usaria um banco de dados para verificar credenciais
    email = request.form['email']
    senha = request.form['senha']

    for usuario in usuarios_cadastrados:
        if usuario['email'] == email and usuario['senha'] == senha:
            return redirect(url_for('pagina_pessoal'))

    # Se não encontrar o usuário, redirecionar de volta para a página de login
    return redirect(url_for('index'))

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    # Lógica para cadastrar um novo usuário (adapte conforme necessário)
    novo_usuario = {
        'nome': request.form['nome'],
        'email': request.form['email'],
        'senha': request.form['senha']
    }

    usuarios_cadastrados.append(novo_usuario)

    # Redirecionar para a página pessoal após o cadastro
    return redirect(url_for('pagina_pessoal'))

if __name__ == '__main__':
    app.run(debug=True)
