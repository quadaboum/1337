from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "topaz_secret")

# === UTILS ===

def get_db_connection():
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        database=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        port=os.environ.get("PGPORT", 5432)
    )

def is_logged_in():
    return "user_id" in session

def is_admin():
    return session.get("username") == "Topaz"

def get_version():
    try:
        with open("version.txt") as f:
            return f.read().strip()
    except:
        return "inconnue"

def render_page(template, **kwargs):
    return render_template(template, version=get_version(), **kwargs)

# === PROTECTION ===

@app.before_request
def restrict_routes():
    public_pages = {"index", "login", "register", "disclaimer", "static"}
    if not is_logged_in() and request.endpoint not in public_pages:
        return redirect(url_for("login"))

# === ROUTES ===

@app.route("/")
def index():
    return render_page("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_page("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_page("register.html")

@app.route("/dashboard")
def dashboard():
    if not is_admin():
        return render_page("unauthorized.html"), 403
    return render_page("dashboard.html")

@app.route("/disclaimer")
def disclaimer():
    return render_page("disclaimer.html")

# Ajouter ici d'autres routes simplifiées...

# === MAIN ===

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


def get_user_count():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users")
            return cur.fetchone()[0]

def get_latest_users(limit=5):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT username, niveau, prestige FROM users ORDER BY created_at DESC LIMIT %s", (limit,))
            return [dict(username=u, niveau=l, prestige=p) for (u, l, p) in cur.fetchall()]

def get_averages():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COALESCE(AVG(niveau), 0), AVG(prestige) FROM users")
            return cur.fetchone()

def generate_invite_code():
    import secrets
    return secrets.token_hex(8)

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not is_admin():
        return render_page("unauthorized.html"), 403

    user_count = get_user_count()
    latest_users = get_latest_users()
    avg_niveau, avg_prestige = get_averages()
    invite_code = session.pop("new_invite", None)

    return render_page("dashboard.html",
                       user_count=user_count,
                       latest_users=latest_users,
                       avg_niveau=round(avg_niveau or 0, 2),
                       avg_prestige=round(avg_prestige or 0, 2),
                       invite_code=invite_code)

@app.route("/generate_invite", methods=["POST"])
def generate_invite():
    if not is_admin():
        return redirect(url_for("dashboard"))
    code = generate_invite_code()
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO invites (code) VALUES (%s)", (code,))
            conn.commit()
    session["new_invite"] = code
    return redirect(url_for("dashboard"))

@app.route("/delete_user", methods=["POST"])
def delete_user():
    if not is_admin():
        return redirect(url_for("dashboard"))
    username = request.form.get("username")
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE username = %s", (username,))
            conn.commit()
    return redirect(url_for("dashboard"))

@app.route("/update_user", methods=["POST"])
def update_user():
    if not is_admin():
        return redirect(url_for("dashboard"))
    username = request.form.get("username")
    niveau = request.form.get("niveau")
    prestige = request.form.get("prestige")
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET niveau = %s, prestige = %s WHERE username = %s",
                        (niveau, prestige, username))
            conn.commit()
    return redirect(url_for("dashboard"))


@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/missions")
def missions():
    return render_template("missions.html")

@app.route("/boutique")
def boutique():
    return render_template("boutique.html")

@app.route("/dons")
def dons():
    return render_template("dons.html")

@app.route("/offrande")
def offrande():
    return render_template("offrande.html")

@app.route("/statistiques")
def statistiques():
    return render_template("statistiques.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
