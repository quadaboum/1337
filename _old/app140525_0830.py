from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "topaz_secret_key")

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

@app.before_request
def restrict_pages():
    open_routes = ['index', 'login', 'register', 'disclaimer', 'static']
    if not is_logged_in() and request.endpoint not in open_routes:
        return redirect(url_for('login'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE pseudo = %s", (pseudo,))
        row = cur.fetchone()
        if row:
            user_id, hashed_pw = row
            if check_password_hash(hashed_pw, password):
                session["user_id"] = user_id
                session["pseudo"] = pseudo
                cur.execute(
                    "UPDATE users SET ip_address = %s, user_agent = %s WHERE id = %s",
                    (request.remote_addr, request.headers.get("User-Agent"), user_id)
                )
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('dashboard') if pseudo == "Topaz" else url_for('menu'))
        cur.close()
        conn.close()
        return "Échec de connexion"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        code = request.form["code"]
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
        cur.execute(
            "INSERT INTO users (nom, pseudo, password, niveau) VALUES (%s, %s, %s, %s)",
            (pseudo, pseudo, hashed_pw, 1)
        )
        conn.commit()
        cur.execute("SELECT id FROM users WHERE pseudo = %s", (pseudo,))
        user_id = cur.fetchone()[0]
        cur.execute(
            "UPDATE invitation_codes SET used = TRUE, used_by_user_id = %s WHERE id = %s",
            (user_id, code_row[0])
        )
        conn.commit()
        cur.execute(
            "UPDATE users SET ip_address = %s, user_agent = %s WHERE id = %s",
            (request.remote_addr, request.headers.get("User-Agent"), user_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        session["user_id"] = user_id
        session["pseudo"] = pseudo
        return redirect(url_for('dashboard') if pseudo == "Topaz" else url_for('menu'))
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if session.get("pseudo") != "Topaz":
        return "Accès interdit"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, pseudo, niveau, prestige, argent, dons, ip_address, user_agent FROM users")
    users = cur.fetchall()
    cur.execute(
        "SELECT code, used, (SELECT pseudo FROM users WHERE id = invitation_codes.used_by_user_id) FROM invitation_codes"
    )
    codes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("dashboard.html", users=users, codes=codes)

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
