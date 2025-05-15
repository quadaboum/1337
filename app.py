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
