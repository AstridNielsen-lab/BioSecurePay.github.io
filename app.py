import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Diretório para armazenar as imagens do cadastro
cadastro_dir = 'static/cadastro_images'

if not os.path.exists(cadastro_dir):
    os.makedirs(cadastro_dir)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de cadastro
@app.route('/cadastro')
def exibir_cadastro():
    return render_template('cadastro.html')

# Rota para processar o formulário de cadastro
@app.route('/processar_cadastro', methods=['POST'])
def processar_cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        imagem_base64 = request.form['imagemBase64'].replace("data:image/jpeg;base64,", "")
        imagem_bin = bytes(imagem_base64, 'utf-8')
        
        # Salvar a imagem no diretório do cadastro
        imagem_path = os.path.join(cadastro_dir, f'{nome}.jpg')
        with open(imagem_path, 'wb') as f:
            f.write(imagem_bin)
       
        # Redirecionar para a página com os resultados
        return jsonify({'nome': nome, 'email': email, 'telefone': telefone, 'imagem_path': imagem_path})

if __name__ == '__main__':
    app.run(debug=True)
