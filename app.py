from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
import os
import secrets
import string

app = Flask(__name__)
app.secret_key = "topaz_secret_key"

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS")
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
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        code = request.form["code"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM invitation_codes WHERE code=%s AND used=FALSE", (code,))
        code_data = cur.fetchone()
        if code_data:
            cur.execute("INSERT INTO users (nom, pseudo, password, niveau) VALUES (%s, %s, %s, %s)",
                        (pseudo, pseudo, password, 1))
            conn.commit()
            cur.execute("SELECT id FROM users WHERE pseudo = %s", (pseudo,))
            user_id = cur.fetchone()[0]
            cur.execute("UPDATE invitation_codes SET used=TRUE, used_by_user_id=%s WHERE id=%s", (user_id, code_data[0]))
            conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "pseudo" in session and session["pseudo"] == "Topaz":
        conn = get_db_connection()
        cur = conn.cursor()
        if request.method == "POST" and "generate" in request.form:
            new_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            cur.execute("INSERT INTO invitation_codes (code) VALUES (%s)", (new_code,))
            conn.commit()
        if request.method == "POST" and "update_dons" in request.form:
            user_id = request.form["user_id"]
            new_don = request.form["new_don"]
            cur.execute("UPDATE users SET dons = %s WHERE id = %s", (new_don, user_id))
            conn.commit()
        cur.execute("SELECT id, pseudo, niveau, prestige, argent, dons, ip_address FROM users")
        users = cur.fetchall()
        cur.execute("SELECT code, used, (SELECT pseudo FROM users WHERE id = invitation_codes.used_by_user_id) FROM invitation_codes")
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

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
