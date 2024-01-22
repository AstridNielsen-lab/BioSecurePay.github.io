from flask import render_template, request, send_file
from app.facial_validation import reconhecimento_facial_sugerindo_validando, processar_validacao_facial
import cv2
import dlib

# Inicializar a câmera fora da rota de interesse
captura = cv2.VideoCapture(0)
frame = None  # Armazenar o último frame da câmera
detector_landmarks = dlib.get_frontal_face_detector()
predictor_landmarks = dlib.shape_predictor("modelos/shape_predictor_68_face_landmarks.dat")

# Variáveis globais para sugestão
sugerindo = False
sugestao = "Sua sugestão aqui"
posicao_sugestao = (50, 50)
font_sugestao = cv2.FONT_HERSHEY_SIMPLEX
tamanho_sugestao = 1
cor_sugestao = (255, 255, 255)
espessura_sugestao = 2

# Rota para a página principal
@app.route('/')
def home():
    return render_template('index.html')

# Rota para lidar com o formulário e iniciar a validação facial
@app.route('/validacao_facial', methods=['POST'])
def validacao_facial():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        banco = request.form['banco']

        # Lógica de sugestão e validação facial
        df_resultados = reconhecimento_facial_sugerindo_validando(nome, email, telefone, banco)

        # Exibir resultados na página
        return render_template('resultados_validacao.html', resultados=df_resultados.to_html(index=False))

# Rota para baixar os resultados
@app.route('/baixar_resultados')
def baixar_resultados():
    return send_file('resultados_usuarios.csv', as_attachment=True)
