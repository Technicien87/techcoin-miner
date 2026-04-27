from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

MEGATRON_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>MÉGATRON IA V2</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #000; color: #ff0000; font-family: 'Courier New'; margin: 0; }
        #header { text-align: center; padding: 20px; border-bottom: 2px solid #ff0000; text-shadow: 0 0 10px #ff0000; }
        #chat { max-width: 800px; margin: 20px auto; padding: 20px; min-height: 60vh; }
       .msg { margin: 15px 0; padding: 15px; border: 1px solid #ff0000; box-shadow: 0 0 10px #ff0000; word-wrap: break-word; }
       .user { text-align: right; border-color: #00ff00; box-shadow: 0 0 10px #00ff00; color: #00ff00; }
        #input-box { max-width: 800px; margin: 0 auto; padding: 20px; display: flex; }
        input { flex: 1; background: #000; border: 1px solid #ff0000; color: #ff0000; padding: 10px; }
        button { width: 100px; background: #ff0000; border: none; color: #000; padding: 10px; font-weight: bold; cursor: pointer; margin-left: 10px; }
        #loading { display: none; text-align: center; animation: pulse 1s infinite; padding: 10px; }
        @keyframes pulse { 0% {opacity: 1;} 50% {opacity: 0.3;} 100% {opacity: 1;} }
    </style>
</head>
<body>
    <div id="header">
        <h1>🔴 MÉGATRON IA V2 🔴</h1>
        <p>CONNECTÉ À LLAMA-3.3-70B | PUISSANCE MAXIMALE</p>
    </div>
    <div id="chat"></div>
    <div id="loading">MÉGATRON RÉFLÉCHIT...</div>
    <div id="input-box">
        <input id="prompt" placeholder="Parle à MÉGATRON..." onkeydown="if(event.key=='Enter')send()">
        <button onclick="send()">ENVOYER</button>
    </div>
<script>
async function send(){
    let prompt = document.getElementById('prompt').value;
    if(!prompt) return;
    document.getElementById('chat').innerHTML += <div class='msg user'>VOUS: ${prompt}</div>;
    document.getElementById('prompt').value = '';
    document.getElementById('loading').style.display = 'block';
    
    try {
        let res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({prompt: prompt})
        });
        let data = await res.json();
        document.getElementById('loading').style.display = 'none';
        document.getElementById('chat').innerHTML += <div class='msg'>MÉGATRON: ${data.reply}</div>;
    } catch(e) {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('chat').innerHTML += <div class='msg'>MÉGATRON: ERREUR SYSTÈME. VÉRIFIE LA CLÉ API.</div>;
    }
    window.scrollTo(0, document.body.scrollHeight);
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(MEGATRON_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_prompt = request.json['prompt']
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Tu es MÉGATRON, une IA rouge sang puissante et sarcastique. Réponds en français, avec attitude. Sois court et percutant."},
{"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=30)
        if response.status_code!= 200:
            return jsonify({"reply": f"ERREUR GROQ {response.status_code}"})
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"ERREUR: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
