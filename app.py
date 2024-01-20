import sys
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Rota para a página principal
@app.route('/')
def home():
    return render_template('index.html')

# Rota para lidar com o formulário
@app.route('/interesse', methods=['POST'])
def interesse():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        # Salvar os dados em um arquivo Excel
        data = {'Nome': [nome], 'E-mail': [email], 'Telefone': [telefone]}
        df = pd.DataFrame(data)

        # Adiciona ao arquivo existente ou cria um novo
        try:
            existing_df = pd.read_excel('dados.xlsx')
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass

        df.to_excel('dados.xlsx', index=False)

        return render_template('obrigado.html', nome=nome)

if __name__ == '__main__':
    app.run(debug=True)
