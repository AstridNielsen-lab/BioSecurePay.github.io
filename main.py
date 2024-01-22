from flask import app, render_template
from app import app

if __name__ == '__main__':
    app.run(debug=True)


# Rota para a página principal
@app.route('/')
def home():
    return render_template('index.html')
