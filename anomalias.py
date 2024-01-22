import cv2
import numpy as np
import matplotlib.pyplot as plt

# Carrega a imagem de exemplo
imagem = cv2.imread(r'\Users\Dell\PycharmProjects\biosecurepay\imagem.png')

# Verifica se a leitura da imagem foi bem-sucedida
if imagem is None:
    print("Erro: Não foi possível ler a imagem. Verifique o caminho da imagem.")
    exit()

print("Imagem carregada com sucesso.")

# Converte a imagem para escala de cinza
imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Aplica um filtro de limiarização para segmentar as células
_, imagem_limiarizada = cv2.threshold(imagem_cinza, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Encontra os contornos das células segmentadas
contornos, _ = cv2.findContours(imagem_limiarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(f"Encontrados {len(contornos)} contornos.")

# Inicializa as listas para armazenar os resultados de tamanho, forma e diferença de cor
tamanhos = []
formas = []
diferencas_cor = []

# Loop sobre cada contorno encontrado
for i, contorno in enumerate(contornos):
    # Calcula a área do contorno
    area = cv2.contourArea(contorno)

    # Calcula o perímetro do contorno
    perimetro = cv2.arcLength(contorno, True)

    # Aproxima o contorno para determinar a forma
    forma = cv2.approxPolyDP(contorno, 0.04 * perimetro, True)

    # Calcula a diferença de cor média na região do contorno
    mascara = np.zeros(imagem_cinza.shape, dtype=np.uint8)
    cv2.drawContours(mascara, [contorno], -1, (255), thickness=cv2.FILLED)
    media_cor = cv2.mean(imagem_cinza, mask=mascara)[0]

    # Armazena os resultados nas respectivas listas
    tamanhos.append(area)
    formas.append(len(forma))
    diferencas_cor.append(media_cor)

    # Desenha os contornos encontrados na imagem original
    cv2.drawContours(imagem, [contorno], -1, (0, 255, 0), 2)

# Define os thresholds para contagem de células mais escuras e maiores
threshold_escuras = 100  # Defina o threshold desejado
threshold_maiores = 200  # Defina o threshold desejado

# Contagem de células mais escuras e maiores
contagem_escuras = sum(diferenca_cor > threshold_escuras for diferenca_cor in diferencas_cor)
contagem_maiores = sum(tamanho > threshold_maiores for tamanho in tamanhos)

# Define os thresholds limite para nível de anormalidade
threshold_escuras_limite = 3  # Defina o threshold limite desejado
threshold_maiores_limite = 5  # Defina o threshold limite desejado

# Nível de anormalidade
nivel_anormalidade = "Baixo"
if contagem_escuras > threshold_escuras_limite or contagem_maiores > threshold_maiores_limite:
    nivel_anormalidade = "Alto"

# Diagnóstico
diagnostico = "Normal"
if nivel_anormalidade == "Alto":
    diagnostico = "Anomalia Detectada"

medida_padrao = 0.05

# Calcular a porcentagem em relação ao volume padrão
porcentagem_volume = [(tamanho / medida_padrao) * 100 for tamanho in tamanhos]

# Calcular a quantidade total de infestação com base no indivíduo de 100 kg
peso_individual = 100  # kg
quantidade_infestacao = sum(tamanhos) / medida_padrao * peso_individual

# Calcular a porcentagem em relação aos 100 kg do paciente
porcentagem_infestacao = (quantidade_infestacao / (peso_individual * 1000)) * 100

# Mapear os níveis de infestação para as descrições correspondentes
mapeamento_descricoes = {
    "hiperplasia": "aumento no número de células",
    "hipoplasia": "diminuição no número de células",
    "hipertrofia": "aumento no tamanho das células",
    "hipotrofia": "diminuição no tamanho das células",
    "atrofia": "diminuição no tamanho e no número de células",
    "metaplasia": "alteração no tipo de células",
    "acúmulos intracelulares": "acúmulo de substâncias dentro das células"
}

# Gerar descrição do nível de infestação
descricoes_infestacao = []
for parametro, descricao in mapeamento_descricoes.items():
    if parametro in diagnostico.lower():
        descricoes_infestacao.append(descricao)

# Exibir os resultados individuais de cada célula
for i in range(len(contornos)):
    descricao = ""
    if porcentagem_volume[i] < 100:
        descricao += "Atrofia celular, "
    if formas[i] != 4:
        descricao += "Metaplasia, "
    if diferencas_cor[i] > 0:
        descricao += "Acúmulos intracelulares"

    print(
        f"Célula {i + 1}: Tamanho = {porcentagem_volume[i]:.2f}%, Forma = {formas[i]}, Diferença de Cor = {diferencas_cor[i]:.2f}, {descricao}")

# Exibir a quantidade total de infestação
print(f"Quantidade total de Relação: {quantidade_infestacao:.2f} %")
print(f"Nível de Relação: {', '.join(descricoes_infestacao)}")
print(f"Porcentagem em relação ao usuario: {porcentagem_infestacao:.2f}%")

# Cria o gráfico
plt.figure()
plt.plot(porcentagem_volume, 'r', label='Tamanho (em porcentagem)')
plt.plot(diferencas_cor, 'g', label='Diferença de Cor')
plt.xlabel('Células')
plt.ylabel('Valores')
plt.title('Detecção de Anomalias')
plt.legend()

# Exibe a imagem original com os contornos
cv2.imshow("Imagem com Contornos", imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
