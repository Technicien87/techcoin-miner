from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-moi')

def render_page(content):
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TECHCOIN</title>
    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#00ff88">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <link rel="apple-touch-icon" href="https://i.imgur.com/8QfQX8L.png">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Roboto', sans-serif; 
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #fff; 
            min-height: 100vh;
        }
        .glass { 
            background: rgba(255,255,255,0.05); 
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px; 
            padding: 30px; 
            margin: 20px auto;
            max-width: 600px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .btn { 
            background: linear-gradient(45deg, #00ff88, #00ccff);
            color: #000; 
            padding: 12px 24px; 
            border: none; 
            border-radius: 10px; 
            cursor: pointer;
            font-weight: 700;
            margin: 5px;
            text-decoration: none;
            display: inline-block;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,255,136,0.4); }
        .balance { font-size: 32px; font-weight: 900; color: #00ff88; margin: 20px 0; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px; }
        h2 { font-family: 'Orbitron', sans-serif; color: #00ff88; margin-bottom: 20px; }
        nav { text-align: center; padding: 20px; }
        nav a { color: #00ccff; margin: 0 15px; text-decoration: none; font-weight: 700; }
        #installBtn { 
            position: fixed; 
            bottom: 20px; 
            right: 20px; 
            z-index: 999;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0,255,136,0.7); }
            70% { box-shadow: 0 0 0 10px rgba(0,255,136,0); }
            100% { box-shadow: 0 0 0 0 rgba(0,255,136,0); }
        }
    </style>
</head>
<body>
    <nav>
        <a href="/">Accueil</a>
        <a href="/wallet">Wallet</a>
        <a href="/dex">DEX</a>
        <a href="/stats">Stats</a>
    </nav>
    ''' + content + '''
    <button id="installBtn" class="btn" style="display:none">📱 Installer TECHCOIN</button>
    <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/service-worker.js');
}
        let deferredPrompt;
        const installBtn = document.getElementById('installBtn');
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            installBtn.style.display = 'block';
        });
        installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                await deferredPrompt.userChoice;
                deferredPrompt = null;
                installBtn.style.display = 'none';
            }
        });
    </script>
</body>
</html>
    ''')

@app.route('/')
def index():
    content = f"""
    <div class="glass">
        <h2 style="font-family:Orbitron">TECHCOIN ECOSYSTEM</h2>
        <p style="color:#999">Blockchain révolutionnaire ultra-rapide</p>
        <div class="balance">10,000 TC</div>
        <p style="text-align:center">Bienvenue dans le futur de la crypto</p>
        <div class="grid">
            <a href="/wallet" class="btn">Mon Wallet</a>
            <a href="/dex" class="btn">Swap TC/USDT</a>
            <a href="/stats" class="btn">Statistiques</a>
            <a href="/faucet" class="btn">Faucet</a>
        </div>
    </div>
    """
    return render_page(content)

@app.route('/wallet')
def wallet():
    user = type('User', (), {'balance': 10000.0})()
    content = f"""
    <div class="glass">
        <h2 style="font-family:Orbitron">MON WALLET</h2>
        <p style="color:#999">Adresse: TC1qxy2k...9w0s</p>
        <div style="background:#000;padding:15px;border-radius:10px;margin:15px 0;word-break:break-all;font-size:12px">
            TC1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
        </div>
        <div class="balance">{user.balance:.4f} TC</div>
        <p style="text-align:center;color:#999">≈ ${(user.balance * 0.85):.2f} USD</p>
        <div class="grid">
            <button class="btn">Envoyer</button>
            <button class="btn">Recevoir</button>
            <button class="btn">Historique</button>
            <button class="btn">Sécurité</button>
        </div>
    </div>
    """
    return render_page(content)

@app.route('/dex')
def dex():
    content = f"""
    <div class="glass">
        <h2 style="font-family:Orbitron">TECHCOIN DEX</h2>
        <p style="color:#999">Swap TECHCOIN <-> USDT. Liquidité: $2.45M</p>
        <div style="background:#000;padding:20px;border-radius:10px;margin:20px 0">
            <p style="margin-bottom:10px">Tu donnes: <strong>1,000 TC</strong></p>
            <p>Tu reçois: <strong>850 USDT</strong></p>
            <p style="color:#999;font-size:14px;margin-top:10px">Taux: 1 TC = 0.85 USDT</p>
        </div>
        <button class="btn" style="width:100%">SWAP MAINTENANT</button>
    </div>
    """
    return render_page(content)

@app.route('/stats')
def stats():
    content = f"""
    <div class="glass">
        <h2 style="font-family:Orbitron">STATISTIQUES RÉSEAU</h2>
        <div class="grid" style="grid-template-columns:1fr 1fr;text-align:left">
            <div style="background:#000;padding:15px;border-radius:10px">
                <p style="color:#999">TPS</p>
                <p style="font-size:24px;font-weight:700;color:#00ff88">50,000</p>
            </div>
            <div style="background:#000;padding:15px;border-radius:10px">
                <p style="color:#999">Bloc Time</p>
                <p style="font-size:24px;font-weight:700;color:#00ccff">0.5s</p>
            </div>
            <div style="background:#000;padding:15px;border-radius:10px">
                <p style="color:#999">Wallets</p>
                <p style="font-size:24px;font-weight:700">125,430</p>
            </div>
            <div style="background:#000;padding:15px;border-radius:10px">
                <p style="color:#999">Market Cap</p>
                <p style="font-size:24px;font-weight:700">$8.5M</p>
            </div>
        </div>
    </div>
    """
    return render_page(content)
@app.route('/faucet')
def faucet():
    content = f"""
    <div class="glass">
        <h2 style="font-family:Orbitron">TECHCOIN FAUCET</h2>
        <p style="color:#999">Réclame 100 TC gratuits toutes les 24h</p>
        <div style="background:#000;padding:20px;border-radius:10px;margin:20px 0;text-align:center">
            <p style="font-size:48px;margin:10px 0">🎁</p>
            <p>Prochain claim dans: <strong>00:00:00</strong></p>
        </div>
        <button class="btn" style="width:100%">RÉCLAMER 100 TC</button>
        <p style="color:#666;font-size:12px;margin-top:15px;text-align:center">
            Connecte ton wallet pour réclamer
        </p>
    </div>
    """
    return render_page(content)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
