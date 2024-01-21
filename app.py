import os
import cv2
import dlib
import base64
from flask import Flask, render_template, request, Response
import pandas as pd
import face_recognition
import urllib.request
import bz2
import shutil
import requests
import numpy as np

# Baixar o modelo shape_predictor_68_face_landmarks.dat
dlib_model_url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
dlib_model_path_bz2 = "shape_predictor_68_face_landmarks.dat.bz2"
dlib_model_path = "modelos/shape_predictor_68_face_landmarks.dat"

# Baixar o arquivo comprimido
with urllib.request.urlopen(dlib_model_url) as response, open(dlib_model_path_bz2, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

# Descompactar o arquivo
with bz2.open(dlib_model_path_bz2, 'rb') as f_in, open(dlib_model_path, 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)

# Caminho para o modelo descompactado
shape_predictor_path = "modelos/shape_predictor_68_face_landmarks.dat"

# Inicializar o detector de landmarks faciais
detector_landmarks = dlib.get_frontal_face_detector()
predictor_landmarks = dlib.shape_predictor(shape_predictor_path)


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
    global frame
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

        # Lógica de reconhecimento facial
        nome_identificado = reconhecimento_facial()

        return render_template('obrigado.html', nome=nome, nome_identificado=nome_identificado)

# Rota para iniciar o reconhecimento facial
@app.route('/iniciar_reconhecimento_facial')
def iniciar_reconhecimento_facial():
    global frame
    frame = None  # Limpar o frame antes de começar
    nome_identificado = reconhecimento_facial()
    return nome_identificado

# Rota para parar o reconhecimento facial
@app.route('/parar_reconhecimento_facial')
def parar_reconhecimento_facial():
    # Liberar os recursos da câmera ao encerrar o reconhecimento facial
    captura.release()
    cv2.destroyAllWindows()

    # Converter o último frame em base64 para exibir na página
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')

    return render_template('parado.html', imagem_base64=frame_base64)

if __name__ == '__main__':
    app.run(debug=True)
