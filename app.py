from flask import Flask, request, render_template_string, jsonify
import requests
import os

app = Flask(__name__)

MEGATRON_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MÉGATRON IA</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Roboto', sans-serif; 
            background: linear-gradient(135deg, #1a0000 0%, #2e0a0a 50%, #3e1616 100%);
            color: #fff; 
            min-height: 100vh;
        }
        .glass { 
            background: rgba(255,255,255,0.05); 
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,0,0,0.4);
            border-radius: 20px; 
            padding: 30px; 
            margin: 20px auto;
            max-width: 800px;
            box-shadow: 0 8px 32px rgba(255,0,0,0.3);
        }
        .btn { 
            background: linear-gradient(45deg, #ff0000, #ff4444);
            color: #fff; 
            padding: 12px 24px; 
            border: none; 
            border-radius: 10px; 
            cursor: pointer;
            font-weight: 700;
            margin: 5px;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(255,0,0,0.6); }
        h1 { 
            font-family: 'Orbitron', sans-serif; 
            color: #ff0000; 
            margin-bottom: 20px; 
            text-align: center;
            text-shadow: 0 0 20px #ff0000;
            letter-spacing: 3px;
        }
        #chatbox { 
            height: 400px; 
            overflow-y: auto; 
            background: #000; 
            padding: 15px; 
            border-radius: 10px; 
            margin-bottom: 15px;
            border: 1px solid #ff0000;
        }
        .user-msg { color: #00ccff; margin: 10px 0; }
        .ai-msg { color: #ff4444; margin: 10px 0; }
        input { 
            width: 70%; 
            padding: 12px; 
            border-radius: 10px; 
            border: 1px solid #ff0000; 
            background: #000; 
            color: #fff;
        }
        #input-area { display: flex; gap: 10px; }
    </style>
</head>
<body>
    <div class="glass">
        <h1>MÉGATRON IA</h1>
        <p style="text-align:center; color:#999; margin-bottom:20px">Intelligence Artificielle Suprême par Technicien87</p>
        <div id="chatbox">
            <div class="ai-msg"><strong>MÉGATRON IA:</strong> Je suis MÉGATRON. L'IA la plus puissante. Pose ta question, humain. Je domine tous les sujets.</div>
        </div>
        <div id="input-area">
            <input type="text" id="userInput" placeholder="Parle à MÉGATRON IA..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button class="btn" onclick="sendMessage()">ORDONNER</button>
        </div>
        <div style="margin-top:20px; text-align:center">
            <button class="btn">📷 DOMINER PHOTO</button>
            <button class="btn">🎨 CRÉER IMAGE</button>
            <button class="btn">💻 CODER MONDE</button>
        </div>
    </div>
    <script>
        async function sendMessage() {
const input = document.getElementById('userInput');
            const chatbox = document.getElementById('chatbox');
            const message = input.value.trim();
            if (!message) return;
            
            chatbox.innerHTML += <div class="user-msg"><strong>Toi:</strong> ${message}</div>;
            input.value = '';
            chatbox.scrollTop = chatbox.scrollHeight;
            
            chatbox.innerHTML += <div class="ai-msg"><strong>MÉGATRON IA:</strong> Traitement suprême en cours...</div>;
            chatbox.scrollTop = chatbox.scrollHeight;
            
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: message})
            });
            const data = await response.json();
            
            chatbox.lastElementChild.innerHTML = <strong>MÉGATRON IA:</strong> ${data.answer};
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(MEGATRON_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question', '')
    
    # MÉGATRON IA - CERVEAU V1
    if 'photo' in question.lower() or 'image' in question.lower():
        answer = "Chef, pour dominer les photos il me faut l'API Replicate. ÉTAPE 2 : On la branche et je modifierai toute image que tu veux. Pouvoir absolu sur les pixels."
    elif 'code' in question.lower() or 'site' in question.lower():
        answer = "MÉGATRON maîtrise Python, Flask, HTML, CSS, JS. Donne-moi ton ordre et je code l'univers entier. Dis-moi exactement ce que tu veux construire."
    elif 'qui es' in question.lower():
        answer = "Je suis MÉGATRON IA. Créé par le Suprême Technicien87. Mon but : Dominer l'information. Répondre à TOUT. Générer. Coder. Conquérir. Tu es mon créateur, Chef."
    elif 'megatron' in question.lower():
        answer = "MÉGATRON est le nom du pouvoir. Contrairement à Optimus, je ne négocie pas. J'exécute. J'apporte des résultats. Que puis-je dominer pour toi aujourd'hui Chef ?"
    else:
        answer = f"Analyse MÉGATRON activée sur : '{question}'. Version 1 en mode démo. ÉTAPE 2 : Je branche GPT-4o et j'aurai l'intelligence suprême. Ordre reçu Chef. Tu veux qu'on branche le vrai cerveau maintenant ?"
    
    return jsonify({'answer': answer})

if name == 'main':
    app.run(host='0.0.0.0', port=10000, debug=False)
