from flask import Flask, render_template_string, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os, random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'techcoin-ecosystem-2027')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///techcoin.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CONFIG TECHCOIN ECOSYSTEM
TOTAL_SUPPLY = 100_000_000 # 100 Millions
PRIX_TECHCOIN = 10.00 # $10 affiché
TAUX_MINAGE = 1.0
DELAI_MINAGE = 24

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    dernier_minage = db.Column(db.DateTime, default=None)
    adresse_wallet = db.Column(db.String(42), default=lambda: "0x"+os.urandom(20).hex())
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

BASE = """
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TECHCOIN ECOSYSTEM</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{--gold:#FFD700;--bg:#050510;--glass:rgba(255,215,0,0.05)}
*{box-sizing:border-box;margin:0;font-family:Inter,sans-serif}
body{background:radial-gradient(circle at 20% 20%,#1a1a2e 0%,#050510 50%,#000 100%);color:#fff;min-height:100vh}
nav{display:flex;justify-content:space-between;align-items:center;padding:15px 5%;background:rgba(0,0,0,0.3);backdrop-filter:blur(10px);border-bottom:1px solid var(--glass);position:sticky;top:0;z-index:100}
.logo{font-family:Orbitron;font-size:24px;font-weight:900}.logo span{color:var(--gold);text-shadow:0 0 15px var(--gold)}
.nav-links a{color:#ccc;text-decoration:none;margin:0 15px;font-weight:600}.nav-links a:hover{color:var(--gold)}
.btn{background:linear-gradient(90deg,var(--gold),#FFA500);color:#000;padding:10px 20px;border-radius:8px;font-weight:900;text-decoration:none;border:none;cursor:pointer}
.container{max-width:1200px;margin:40px auto;padding:0 20px}
.glass{background:var(--glass);border:1px solid rgba(255,215,0,0.2);border-radius:20px;padding:30px;backdrop-filter:blur(15px);box-shadow:0 0 40px rgba(255,215,0,0.1)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin-top:30px}
.stat h3{color:#999;font-size:14px}.stat.val{font-size:28px;font-weight:900;color:var(--gold);font-family:Orbitron}
.balance{font-size:64px;text-align:center;color:var(--gold);text-shadow:0 0 20px var(--gold);font-family:Orbitron;margin:20px 0}
input,select{width:100%;padding:12px;margin:10px 0;background:#0A0A0F;border:1px solid var(--gold);border-radius:8px;color:#fff}
.flash{background:#FF4444;padding:12px;border-radius:8px;text-align:center;margin-bottom:15px}
.timer{text-align:center;color:#FF8A00;margin:15px 0;font-size:18px}
table{width:100%;border-collapse:collapse;margin-top:20px}th,td{padding:12px;text-align:left;border-bottom:1px solid var(--glass)}th{color:var(--gold)}
button:disabled{background:#333;color:#666;cursor:not-allowed}
.hero{text-align:center;padding:60px 0}.hero h1{font-size:52px;font-family:Orbitron}.hero h1 span{color:var(--gold)}
</style>
<script src="https://s3.tradingview.com/tv.js"></script>
</head><body>
<nav>
  <div class="logo">TECH<span>COIN</span></div>
  <div class="nav-links">
    <a href="{{ url_for('home') }}">Accueil</a>
    <a href="{{ url_for('dashboard') }}">Miner</a>
    <a href="{{ url_for('wallet') }}">Wallet</a>
<a href="{{ url_for('dex') }}">DEX</a>
    <a href="{{ url_for('leaderboard') }}">Top 100</a>
    {% if session.user_id %}<a href="/logout" class="btn">Déconnexion</a>{% else %}<a href="{{ url_for('login') }}" class="btn">Connexion</a>{% endif %}
  </div>
</nav>
<div class="container">
{% with m=get_flashed_messages() %}{% if m %}<div class="flash">{{ m[0] }}</div>{% endif %}{% endwith %}
{{ content|safe }}
</div></body></html>
"""

def render_page(content):
    return render_template_string(BASE, content=content)

@app.route('/')
def home():
    mine_total = db.session.query(db.func.sum(User.balance)).scalar() or 0
    holders = User.query.count()
    content = f"""
    <div class="hero">
        <h1>L'ECOSYSTEME <span>TECHCOIN</span></h1>
        <p style="color:#999;margin:20px 0;font-size:18px">Mine, Trade, HODL. Le futur de la finance décentralisée.</p>
        <a href="{url_for('register')}" class="btn" style="font-size:18px;padding:15px 30px">COMMENCER À MINER</a>
    </div>
    <div class="grid">
        <div class="glass stat"><h3>PRIX TECHCOIN</h3><div class="val">${PRIX_TECHCOIN:.2f}</div></div>
        <div class="glass stat"><h3>TOTAL SUPPLY</h3><div class="val">{TOTAL_SUPPLY:,}</div></div>
        <div class="glass stat"><h3>COIN MINÉS</h3><div class="val">{mine_total:,.0f}</div></div>
        <div class="glass stat"><h3>HOLDERS</h3><div class="val">{holders:,}</div></div>
    </div>
    <div class="glass" style="margin-top:30px;height:400px" id="tv_chart"></div>
    <script>new TradingView.widget({{"width":"100%","height":400,"symbol":"BINANCE:BTCUSDT","interval":"D","theme":"dark","style":"1","locale":"fr","toolbar_bg":"#f1f3f6","enable_publishing":false,"hide_top_toolbar":true,"save_image":false,"container_id":"tv_chart"}});</script>
    """
    return render_page(content)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    peut_miner = user.dernier_minage is None or datetime.utcnow() - user.dernier_minage >= timedelta(hours=DELAI_MINAGE)
    temps_restant = ""
    if not peut_miner:
        restant = timedelta(hours=DELAI_MINAGE) - (datetime.utcnow() - user.dernier_minage)
        h, rem = divmod(restant.seconds, 3600)
        m, s = divmod(rem, 60)
        temps_restant = f"{restant.days}j {h}h {m}m"
    content = f"""
    <div class="glass"><h2 style="text-align:center;font-family:Orbitron">MINING DASHBOARD</h2>
    <div class="balance">{user.balance:.4f} <span style="font-size:24px">TC</span></div>
    <p style="text-align:center;color:#999">≈ ${(user.balance * PRIX_TECHCOIN):,.2f} USD</p>
    {"<form method='post' action='"+url_for('miner')+"'><button type='submit' class='btn' style='width:100%;font-size:20px;padding:20px'>⛏️ MINER "+str(TAUX_MINAGE)+" TECHCOIN</button></form>" if peut_miner else "<button disabled class='btn' style='width:100%;font-size:20px;padding:20px'>MINAGE EN COURS</button><div class='timer'>Prochain minage dans: "+temps_restant+"</div>"}
    </div>
    """
    return render_page(content)

@app.route('/miner', methods=['POST'])
def miner():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if user.dernier_minage and datetime.utcnow() - user.dernier_minage < timedelta(hours=DELAI_MINAGE):
        flash("Tu as déjà miné. Attends 24h!")
    else:
        user.balance += TAUX_MINAGE
        user.dernier_minage = datetime.utcnow()
        db.session.commit()
        flash(f"Tu as miné {TAUX_MINAGE} TECHCOIN! +${TAUX_MINAGE * PRIX_TECHCOIN}")
    return redirect(url_for('dashboard'))

@app.route('/wallet')
def wallet():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
content = f"""
    <div class="glass"><h2 style="font-family:Orbitron">MON WALLET TECHCOIN</h2>
    <p style="color:#999">Adresse:</p><div style="background:#000;padding:10px;border-radius:8px;word-break:break-all;font-family:monospace">{user.adresse_wallet}</div>
    <div class="balance">{user.balance:.4f} TC</div><p style="text-align:center;color:#999">≈ ${(user.balance * PRIX_TECHCOIN):,.2f} USD</p>
    <div class="grid"><button class="btn">Envoyer</button><button class="btn">Recevoir</button></div>
    </div>
    """
    return render_page(content)

@app.route('/dex')
def dex():
    content = f"""
    <div class="glass"><h2 style="font-family:Orbitron">TECHCOIN DEX</h2>
    <p style="color:#999">Swap TECHCOIN <-> USDT. Liquidité: $2,450,000</p>
    <div class="grid" style="grid-template-columns:1fr 1fr">
        <div><label>Tu paies</label><input type="number" placeholder="0.0"><select><option>TECHCOIN</option></select></div>
        <div><label>Tu reçois</label><input type="number" placeholder="0.0"><select><option>USDT</option></select></div>
    </div>
    <button class="btn" style="width:100%;margin-top:20px">SWAP</button>
    <p style="text-align:center;color:#666;margin-top:15px;font-size:12px">1 TC = ${PRIX_TECHCOIN} USDT</p>
    </div>
    """
    return render_page(content)

@app.route('/leaderboard')
def leaderboard():
    top = User.query.order_by(User.balance.desc()).limit(100).all()
    rows = "".join([f"<tr><td>#{i+1}</td><td>{u.email[:3]}***{u.email[-4:]}</td><td>{u.balance:.2f} TC</td><td>${u.balance*PRIX_TECHCOIN:,.2f}</td></tr>" for i,u in enumerate(top)])
    content = f"""<div class="glass"><h2 style="font-family:Orbitron">TOP 100 MINEURS</h2><table><tr><th>Rang</th><th>Mineur</th><th>Balance</th><th>Valeur</th></tr>{rows}</table></div>"""
    return render_page(content)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        if User.query.filter_by(email=email).first():
            flash('Email déjà utilisé')
        else:
            user = User(email=email, password=generate_password_hash(request.form['password']))
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    content = """<div class="glass" style="max-width:400px;margin:auto"><h2 style="font-family:Orbitron;text-align:center">REJOINDRE TECHCOIN</h2><form method="post"><input name="email" type="email" placeholder="Email" required><input name="password" type="password" placeholder="Mot de passe" required><button type="submit" class="btn" style="width:100%">CRÉER MON WALLET</button></form></div>"""
    return render_page(content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Email ou mot de passe incorrect')
    content = """<div class="glass" style="max-width:400px;margin:auto"><h2 style="font-family:Orbitron;text-align:center">CONNEXION</h2><form method="post"><input name="email" type="email" placeholder="Email" required><input name="password" type="password" placeholder="Mot de passe" required><button type="submit" class="btn" style="width:100%">SE CONNECTER</button></form></div>"""
    return render_page(content)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
