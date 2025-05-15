with open("version.txt") as f:
    current_version = f.read().strip()


from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "topaz_secret_key")

# --- Fonctions Utilitaires ---

def get_db_connection():
    """Connexion sécurisée à la base PostgreSQL via variables d'environnement."""
    return psycopg2.connect(
        host=os.environ.get("PGHOST"),
        database=os.environ.get("PGDATABASE"),
        user=os.environ.get("PGUSER"),
        password=os.environ.get("PGPASSWORD"),
        port=os.environ.get("PGPORT", 5432)
    )

def is_logged_in():
    return "user_id" in session

def is_admin():
    return session.get("pseudo") == "Topaz"


@app.before_request
def restrict_pages():
    allowed_endpoints = ['index', 'login', 'register', 'disclaimer', 'static']
    if request.endpoint and any(request.endpoint.startswith(e) for e in allowed_endpoints):
        return
    if not is_logged_in():
        return redirect(url_for('login'))

# --- Routes Publiques ---

@app.route("/")
def index():
    return render_template("index.html", version=current_version)

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html", version=current_version)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE pseudo = %s", (pseudo,))
        row = cur.fetchone()
        if row and check_password_hash(row[1], password):
            session["user_id"], session["pseudo"] = row[0], pseudo
            cur.execute("UPDATE users SET ip_address = %s, user_agent = %s WHERE id = %s",
                        (request.remote_addr, request.headers.get("User-Agent"), row[0]))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("dashboard") if pseudo == "Topaz" else url_for("menu"))
        cur.close()
        conn.close()
        return "Traversée du portail astral refusée !"
    return render_template("login.html", version=current_version)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        code = request.form["code"]
        if pseudo == "Topaz":
            return "Topaz ne peut pas être recréé."
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE pseudo = %s", (pseudo,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return "Pseudo déjà utilisé"
        cur.execute("SELECT id FROM invitation_codes WHERE code = %s AND used = FALSE", (code,))
        code_row = cur.fetchone()
        if not code_row:
            cur.close()
            conn.close()
            return "Clé invalide"
        hashed_pw = generate_password_hash(password)
        cur.execute("INSERT INTO users (nom, pseudo, password, niveau, used_invitation_code) VALUES (%s, %s, %s, %s, %s)",
                    (pseudo, pseudo, hashed_pw, 1, code))
        conn.commit()
        cur.execute("SELECT id FROM users WHERE pseudo = %s", (pseudo,))
        user_id = cur.fetchone()[0]
        cur.execute("UPDATE invitation_codes SET used = TRUE, used_by_user_id = %s WHERE id = %s",
                    (user_id, code_row[0]))
        conn.commit()
        cur.close()
        conn.close()
        session["user_id"] = user_id
        session["pseudo"] = pseudo
        return redirect(url_for("dashboard") if pseudo == "Topaz" else url_for("menu"))
    return render_template("register.html", version=current_version)

# --- Routes Utilisateur ---

@app.route("/menu")
def menu():
    return render_template("menu.html", version=current_version, user=user)

@app.route("/missions")
def missions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT niveau, prestige, pseudo FROM users WHERE id = %s", (session.get('user_id'),))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("missions.html", version=current_version, , prestige, pseudo FROM users WHERE id = %s", (session.get('user_id'),))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("boutique.html", version=current_version, , prestige, pseudo FROM users WHERE id = %s", (session.get('user_id'),))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("dons.html", version=current_version, , prestige, pseudo FROM users WHERE id = %s", (session.get('user_id'),))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("offrande.html", version=current_version, , prestige, pseudo FROM users WHERE id = %s", (session.get('user_id'),))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("statistiques.html", version=current_version, , version=current_version)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, pseudo, niveau, prestige, argent, dons, ip_address, user_agent, used_invitation_code FROM users")
    users = cur.fetchall()
    cur.execute("SELECT code, used, (SELECT pseudo FROM users WHERE id = invitation_codes.used_by_user_id) FROM invitation_codes")
    codes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("dashboard.html", users=users, codes=codes, version=current_version, user=user)

# --- Footer Automatique sur pages publiques ---

@app.after_request
def inject_footer(response):
    try:
        if request.endpoint in ['index', 'login', 'register', 'disclaimer']:
            content = response.get_data(as_text=True)
            css = "<style>footer { position: absolute; bottom: 10px; width: 100%; text-align: center; font-size: 0.8em; color: #666; }</style>"
            footer_html = "<footer>- La Voie de l'Éclipse™ - Ce site n'est pas réel - 2025 © -</footer>"
            content = content.replace("</head>", css + "</head>")
            content = content.replace("</body>", footer_html + "</body>")
            response.set_data(content)
    except Exception:
        pass
    return response

# --- Lancement local ---

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


@app.context_processor
def inject_version():
    try:
        with open("version.txt", "r") as f:
            version = f.read().strip()
    except:
        version = "inconnue"
    return dict(version=version)
