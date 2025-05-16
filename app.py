
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os
import secrets
from flask import session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "topaz_secret_key")

# --- Utilitaires ---

def get_db_connection():
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
    allowed = ['index', 'login', 'register', 'disclaimer', 'unauthorized', 'static']
    if not is_logged_in() and request.endpoint not in allowed:
        return redirect(url_for("index"))

# --- Routes publiques ---




@app.context_processor
def inject_version():
    try:
        with open("version.txt") as f:
            version = f.read().strip()
            return dict(version=version)
    except Exception:
        return dict(version="Inconnue")
def inject_version():
    try:
        with open("version.txt") as f:
            lines = [l.strip() for l in f.readlines()]
            annee = lines[0] if lines else "Inconnue"
            version = lines[1] if len(lines) > 1 else "Inconnue"
            return dict(annee=annee, version=version)
    except Exception:
        return dict(annee="Inconnue", version="Inconnue")
def inject_version():
    try:
        with open("version.txt") as f:
            return dict(version=f.read().strip())
    except Exception:
        return dict(version="Inconnue")
@app.route("/")
def index():
    return render_template("index.html", version=current_version())

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html", version=current_version())

@app.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html", version=current_version())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM user WHERE pseudo = %s", (pseudo,))
        row = cur.fetchone()
        if row and check_password_hash(row[1], password):
            session["user_id"], session["pseudo"] = row[0], pseudo
            cur.execute("UPDATE user SET ip_address = %s, user_agent = %s WHERE id = %s",
                        (request.remote_addr, request.headers.get("User-Agent"), row[0]))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("dashboard") if pseudo == "Topaz" else url_for("menu"))
        cur.close()
        conn.close()
    return render_template("login.html", version=current_version())

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        code = request.form["code"]
        if pseudo == "Topaz":
            return "Pseudo réservé"
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM user WHERE pseudo = %s", (pseudo,))
        if cur.fetchone():
            return "Pseudo déjà pris"
        cur.execute("SELECT id FROM invitation_codes WHERE code = %s AND used = FALSE", (code,))
        code_row = cur.fetchone()
        if not code_row:
            return "Code invalide"
        hashed = generate_password_hash(password)
        cur.execute("INSERT INTO user (nom, pseudo, password, niveau, used_invitation_code) VALUES (%s, %s, %s, %s, %s)",
                    (pseudo, pseudo, hashed, 1, code))
        conn.commit()
        cur.execute("SELECT id FROM user WHERE pseudo = %s", (pseudo,))
        user_id = cur.fetchone()[0]
        cur.execute("UPDATE invitation_codes SET used = TRUE, used_by_user_id = %s WHERE id = %s",
                    (user_id, code_row[0]))
        conn.commit()
        cur.close()
        conn.close()
        session["user_id"], session["pseudo"] = user_id, pseudo
        return redirect(url_for("dashboard") if pseudo == "Topaz" else url_for("menu"))
    return render_template("register.html", version=current_version())

# --- Routes privées utilisateur ---

def get_user():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT niveau, prestige, pseudo FROM user WHERE id = %s", (session.get('user_id'),))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

@app.route("/menu")
def menu():
    return render_template("menu.html", user=get_user(), version=current_version())

@app.route("/missions")
def missions():
    return render_template("missions.html", user=get_user(), version=current_version())

@app.route("/boutique")
def boutique():
    return render_template("boutique.html", user=get_user(), version=current_version())

@app.route("/dons")
def dons():
    return render_template("dons.html", user=get_user(), version=current_version())

@app.route("/offrande")
def offrande():
    return render_template("offrande.html", user=get_user(), version=current_version())

@app.route("/statistiques")
def statistiques():
    return render_template("statistiques.html", user=get_user(), version=current_version())

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# --- Route Admin ---

@app.route("/dashboard")
def dashboard():
    if not is_admin():
        return redirect(url_for("unauthorized"))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, pseudo, niveau, prestige, argent, dons, ip_address, user_agent, used_invitation_code FROM user")
    user = cur.fetchall()
    cur.execute("SELECT code, used, (SELECT pseudo FROM user WHERE id = invitation_codes.used_by_user_id) FROM invitation_codes")
    codes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("dashboard.html", user=user, codes=codes, version=current_version())

def current_version():
    try:
        with open("version.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return "vUnknown"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
