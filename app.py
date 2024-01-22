import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    # Restante do código...

    # Encontrar landmarks faciais com dlib
    landmarks = predictor_landmarks(frame, dlib.rectangle(left, top, right, bottom))
    
    # Desenhar as landmarks no rosto identificado
    for i in range(68):
        x, y = landmarks.part(i).x, landmarks.part(i).y
        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)


# ...

# Carregar as imagens conhecidas e seus respectivos nomes
conhecidos = []
nomes_conhecidos = []

def carregar_imagens_conhecidas():
    diretorio_conhecidos = 'imagens_conhecidos'
    for arquivo in os.listdir(diretorio_conhecidos):
        if arquivo.endswith('.jpg') or arquivo.endswith('.jpeg') or arquivo.endswith('.png'):
            imagem_conhecido = face_recognition.load_image_file(os.path.join(diretorio_conhecidos, arquivo))
            encoding_conhecido = face_recognition.face_encodings(imagem_conhecido)[0]
            conhecidos.append(encoding_conhecido)
            nomes_conhecidos.append(os.path.splitext(arquivo)[0])

carregar_imagens_conhecidas()

# Inicializar a câmera fora da rota de interesse
captura = cv2.VideoCapture(0)
frame = None  # Armazenar o último frame da câmera
face_locations = []  # Inicializar face_locations globalmente
face_encodings = []  # Inicializar face_encodings globalmente


# Lógica de reconhecimento facial
def reconhecimento_facial():
    global frame, face_locations, face_encodings
    frame = np.array([])  # Adicione esta linha
    nome_identificado = "Desconhecido"
    while True:
        # Capturar um frame
        ret, frame = captura.read()

        # Encontrar rostos no frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Comparar com rostos conhecidos
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Comparar com as imagens conhecidas
            matches = face_recognition.compare_faces(conhecidos, face_encoding)

            if True in matches:
                first_match_index = matches.index(True)
                nome_identificado = nomes_conhecidos[first_match_index]

                # Desenhar retângulo e nome no rosto identificado
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, nome_identificado, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

                # Encontrar landmarks faciais com dlib
                landmarks = predictor_landmarks(frame, dlib.rectangle(left, top, right, bottom))
                
                # Desenhar as landmarks no rosto identificado
                for i in range(68):
                    x, y = landmarks.part(i).x, landmarks.part(i).y
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        # Exibir o frame com o reconhecimento facial
        cv2.imshow('Reconhecimento Facial', frame)

        # Encerrar o reconhecimento ao pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Retornar o nome identificado
    return nome_identificado

# Rota para a página principal
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
