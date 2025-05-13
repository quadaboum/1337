from flask import Flask, render_template, request, redirect, session
import psycopg2
import os
import bcrypt

app = Flask(__name__)
app.secret_key = "topaz_secret_key"

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
    allowed = ['index', 'login', 'register', 'disclaimer', 'static']
    if not is_logged_in() and not request.endpoint in allowed:
        return redirect("/login")

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
        password = request.form["password"].encode('utf-8')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE pseudo = %s", (pseudo,))
        user = cur.fetchone()
        if user and bcrypt.checkpw(password, user[1].encode('utf-8')):
            session["user_id"] = user[0]
            session["pseudo"] = pseudo
        cur.execute("UPDATE users SET ip_address = %s, user_agent = %s WHERE id = %s", (request.remote_addr, request.headers.get("User-Agent"), user[0]))
        conn.commit()
            return redirect("/dashboard" if pseudo == "Topaz" else "/menu")
        return "Échec de connexion"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"].encode('utf-8')
        code = request.form["code"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE pseudo=%s", (pseudo,))
        if cur.fetchone():
            return "Pseudo déjà utilisé"
        cur.execute("SELECT id FROM invitation_codes WHERE code=%s AND used=FALSE", (code,))
        code_data = cur.fetchone()
        if code_data:
            hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
            cur.execute("INSERT INTO users (nom, pseudo, password, niveau) VALUES (%s, %s, %s, %s)",
                        (pseudo, pseudo, hashed_pw, 1))
            conn.commit()
            cur.execute("SELECT id FROM users WHERE pseudo = %s", (pseudo,))
            user_id = cur.fetchone()[0]
            cur.execute("UPDATE invitation_codes SET used=TRUE, used_by_user_id=%s WHERE id=%s", (user_id, code_data[0]))
            conn.commit()
            session["user_id"] = user_id
            session["pseudo"] = pseudo
        cur.execute("UPDATE users SET ip_address = %s, user_agent = %s WHERE id = %s", (request.remote_addr, request.headers.get("User-Agent"), user[0]))
        conn.commit()
            cur.close()
            conn.close()
            return redirect("/dashboard" if pseudo == "Topaz" else "/menu")
        return "Clé invalide"
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if session.get("pseudo") != "Topaz":
        return "Accès interdit"
    return "Bienvenue dans le Dashboard divin de Topaz."

@app.route("/menu")
def menu():
    return "Bienvenue dans le Menu général. Tu es connecté."

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
