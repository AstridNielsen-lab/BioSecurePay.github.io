# BioSecurePay

<h2>Descrição</h2>
<p>BioSecurePay é um sistema de reconhecimento facial com integração a um formulário web para coleta de dados de interesse.</p>

<h2>Requisitos</h2>
<ul>
  <li>Python 3.x</li>
  <li>Bibliotecas Python listadas em <code>requirements.txt</code></li>
</ul>

<h2>Instalação</h2>
<ol>
  <li>Clone o repositório:</li>
  <pre><code>git clone https://github.com/AstridNielsen-lab/biosecurepay.git
cd biosecurepay</code></pre>

  <li>Crie e ative um ambiente virtual:</li>
  <pre><code>python -m venv venv
source venv/bin/activate  # para sistemas Unix
# ou
.\venv\Scripts\activate   # para sistemas Windows</code></pre>

  <li>Instale as dependências:</li>
  <pre><code>pip install -r requirements.txt</code></pre>
</ol>

<h2>Uso</h2>
<ol>
  <li>Baixe o modelo <code>shape_predictor_68_face_landmarks.dat</code> e coloque-o em <code>modelos/</code>.</li>
  <li>Adicione imagens conhecidas em <code>imagens_conhecidos/</code>.</li>
  <li>Inicie o aplicativo:</li>
  <pre><code>python app.py</code></pre>
  <li>Acesse o aplicativo no navegador em <a href="http://127.0.0.1:5000/" target="_blank">http://127.0.0.1:5000/</a>.</li>
</ol>

<h2>Estrutura de Diretórios</h2>
<p>Explicação sobre a estrutura de diretórios do projeto.</p>

<h2>Contribuições</h2>
<p>Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.</p>

<h2>Licença</h2>
<p>Este projeto é licenciado sob a MIT License.</p>

<h2>Autor</h2>
<p>Astrid Nielsen - <a href="https://github.com/AstridNielsen-lab" target="_blank">GitHub</a></p>
