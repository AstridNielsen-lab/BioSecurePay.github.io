let videoStream = null;

async function iniciarReconhecimentoFacial() {
    const videoElement = document.getElementById('camera-video');
    const cameraBox = document.getElementById('camera-box');
    const startMessage = document.getElementById('start-message');

    try {
        videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoElement.srcObject = videoStream;
        videoElement.play();

        cameraBox.style.border = 'none'; // Removendo a borda para mostrar o vídeo
        startMessage.style.display = 'none'; // Ocultando a mensagem inicial
    } catch (error) {
        console.error('Erro ao acessar a câmera:', error);
        alert('Não foi possível acessar a câmera. Verifique as permissões.');
    }
}

function pararReconhecimentoFacial() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
    }

    const videoElement = document.getElementById('camera-video');
    videoElement.srcObject = null;

    const cameraBox = document.getElementById('camera-box');
    const startMessage = document.getElementById('start-message');

    cameraBox.style.border = '2px solid #ddd'; // Restaurando a borda
    startMessage.style.display = 'block'; // Restaurando a mensagem inicial
}

function capturarFoto() {
    const videoElement = document.getElementById('camera-video');
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    const imagemBase64 = canvas.toDataURL('image/jpeg');
    
    // Enviar a imagem para o servidor
    enviarImagem(imagemBase64);
}

async function enviarImagem(imagemBase64) {
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const telefone = document.getElementById('telefone').value;

    // Enviar a imagem para o servidor usando AJAX (pode ser utilizado Fetch API)
    const response = await fetch('/cadastro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            nome: nome,
            email: email,
            telefone: telefone,
            imagemBase64: imagemBase64,
        }),
    });

    if (response.ok) {
        const resultados = await response.json();
        // Armazenar os resultados na localStorage para acessar na próxima página
        localStorage.setItem('resultados', JSON.stringify(resultados));
        // Redirecionar para a página de resultados
        window.location.href = '/cadastro';
    } else {
        alert('Erro ao processar o cadastro. Por favor, tente novamente.');
    }
}
