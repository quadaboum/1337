
from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "topaz_secret_key"

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "voie_eclipse"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASS", "password")
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, niveau FROM users WHERE pseudo=%s AND password=%s", (pseudo, password))
        user = cur.fetchone()
        if user:
            session["user_id"] = user[0]
            session["pseudo"] = pseudo
            session["niveau"] = user[1]
            cur.execute("UPDATE users SET ip_address = %s WHERE id = %s", (request.remote_addr, user[0]))
            conn.commit()
        cur.close()
        conn.close()
        if user:
            return redirect("/dashboard" if pseudo == "Topaz" else "/missions")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nom = request.form["nom"]
        code = request.form["code"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM invitation_codes WHERE code=%s AND used=FALSE", (code,))
        code_data = cur.fetchone()
        if code_data:
            cur.execute("INSERT INTO users (nom, pseudo, password, niveau) VALUES (%s, %s, %s, %s)",
                        (nom, 'Nouveau-' + code[:5], 'defaultpass', 1))
            user_id = cur.lastrowid
            cur.execute("UPDATE invitation_codes SET used=TRUE, used_by_user_id=%s WHERE id=%s", (user_id, code_data[0]))
            conn.commit()
            conn.close()
            return redirect("/login")
        conn.close()
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "pseudo" in session and session["pseudo"] == "Topaz":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT pseudo, niveau, prestige, argent, ip_address FROM users")
        users = cur.fetchall()
        cur.execute("SELECT code, used FROM invitation_codes")
        codes = cur.fetchall()
        conn.close()
        return render_template("dashboard.html", users=users, codes=codes)
    return redirect("/login")

@app.route("/missions")
def missions():
    if "user_id" in session:
        return render_template("missions.html")
    return redirect("/login")

@app.route("/boutique")
def boutique():
    if "user_id" in session:
        return render_template("boutique.html")
    return redirect("/login")

@app.route("/livre")
def livre():
    return render_template("livre.html")

@app.route("/testament")
def testament():
    if "user_id" in session:
        return render_template("testament.html")
    return redirect("/login")

@app.route("/commandements")
def commandements():
    return render_template("commandements.html")

@app.route("/dons")
def dons():
    return render_template("dons.html")

@app.route("/lore")
def lore():
    return render_template("lore.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
