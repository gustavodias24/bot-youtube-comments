<h1> bot-youtube-comments </h1>
<p> Projeto que era pra ser um bot para ficar comentando no YouTube,porém, já foi caunterado antes de funcionar, então, vai ficar ae até eu pensar outro jeito de rodar!😌 </p>

<h2>Mini-tutorial...</h2>
<h3>Passo - 1: Clone o repositório</h3>

```
git clone --branch master https://github.com/gustavodias24/bot-youtube-comments.git
```
<h3>Passo - 2: Configure o arquvio .env</h3>

```
MONGO_URI={URL DO DATABASE}
MAX_CHANNEL_LIMIT={LIMITE POR RODADA}
VIDEO={VIDOE PRA EXTRAIR OS CANAIS}
IS_LINUX={False ou True}
```

<h3>Passo - 3: Instale todos os requerimentos e execute a aplicação
  
```
python main.py
```
  
<p>Vai exibir uma interface parecida com essa: </p>
  <br/>
 <img src="https://raw.githubusercontent.com/gustavodias24/bot-youtube-comments/master/telaAtual.PNG" alt="image-interface" /> 
