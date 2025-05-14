
from functools import wraps
from flask import redirect, session, url_for, render_template

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return render_template("punition.html"), 403
        return f(*args, **kwargs)
    return decorated_function



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
    if not is_logged_in() and request.endpoint not in ['index', 'login', 'register', 'disclaimer', 'static']:
        return redirect(url_for('login'))

def update_user_metadata(cur, user_id):
    cur.execute(
        "UPDATE users SET ip_address = %s, user_agent = %s WHERE id = %s",
        (request.remote_addr, request.headers.get("User-Agent"), user_id)
    )

@app.route('/')
def index():
    return redirect(url_for('menu'))

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
        if row and check_password_hash(row[1], password):
            session["user_id"], session["pseudo"] = row[0], pseudo
            update_user_metadata(cur, row[0])
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('dashboard') if pseudo == "Topaz" else url_for('menu'))
        cur.close()
        conn.close()
        return "Traversée du portail astral refusée !"
    return render_template("login.html")

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
        cur.execute(
            "INSERT INTO users (nom, pseudo, password, niveau, used_invitation_code) VALUES (%s, %s, %s, %s, %s)",
            (pseudo, pseudo, hashed_pw, 1, code)
        )
        conn.commit()
        cur.execute("SELECT id FROM users WHERE pseudo = %s", (pseudo,))
        user_id = cur.fetchone()[0]
        cur.execute(
            "UPDATE invitation_codes SET used = TRUE, used_by_user_id = %s WHERE id = %s",
            (user_id, code_row[0])
        )
        update_user_metadata(cur, user_id)
        conn.commit()
        cur.close()
        conn.close()
        session["user_id"] = user_id
        session["pseudo"] = pseudo
        return redirect(url_for('dashboard') if pseudo == "Topaz" else url_for('menu'))
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    if session.get("pseudo") != "Topaz":
        return "Accès interdit"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, pseudo, niveau, prestige, argent, dons, ip_address, user_agent, used_invitation_code FROM users")
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

@app.route("/missions")
@login_required
def missions():
    if not is_logged_in():
        return redirect("/login")
    return render_template("missions.html")

@app.route("/boutique")
@login_required
def boutique():
    if not is_logged_in():
        return redirect("/login")
    return render_template("boutique.html")

@app.route("/dons")
@login_required
def dons():
    if not is_logged_in():
        return redirect("/login")
    return render_template("dons.html")

@app.route("/offrande")
@login_required
def offrande():
    if not is_logged_in():
        return redirect("/login")
    return render_template("offrande.html")

@app.route("/statistiques")
@login_required
def statistiques():
    if not is_logged_in():
        return redirect("/login")
    return render_template("statistiques.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)



@app.context_processor
def inject_user():
    if 'user_id' in session:
        cur = conn.cursor()
        cur.execute("SELECT username, niveau, prestige FROM users WHERE id = %s", (session['user_id'],))
        row = cur.fetchone()
        cur.close()
        if row:
            return dict(user={'username': row[0], 'niveau': row[1], 'prestige': row[2]})
    return dict(user={'username': 'Inconnu', 'niveau': '-', 'prestige': '-'})
