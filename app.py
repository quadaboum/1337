from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


# === CONFIGURATION DE BASE ===
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "topaz_secret_key")


# === OUTILS FONCTIONNELS ===

# Rendu avec version auto-injectée
def render_page(template_name, **kwargs):
    return render_template(template_name, version=load_version(), **kwargs)

# Vérifie si l'utilisateur connecté est Topaz
def is_admin():
    return is_logged_in() and session.get("username") == "Topaz"

def load_version():
    """Charge la version de l'application depuis version.txt."""
    try:
        with open('version.txt', 'r') as f:
            return f.read().strip()
    except Exception:
        return 'version inconnue'


def get_db_connection():
    """Crée une connexion PostgreSQL."""
    return psycopg2.connect(
        host=os.environ.get("PGHOST"),
        database=os.environ.get("PGDATABASE"),
        user=os.environ.get("PGUSER"),
        password=os.environ.get("PGPASSWORD"),
        port=os.environ.get("PGPORT", 5432)
    )


def is_logged_in():
    """Vérifie la présence d'une session utilisateur."""
    return "user_id" in session


def update_user_metadata(cur, user_id):
    """Met à jour l'IP et l'User-Agent de l'utilisateur."""
    cur.execute(
        "UPDATE users SET ip_address = %s, user_agent = %s WHERE id = %s",
        (request.remote_addr, request.headers.get("User-Agent"), user_id)
    )


# === SÉCURITÉ / ACCÈS ===
@app.before_request
def restrict_pages():
    """Protège toutes les pages sauf les publiques."""
    public_routes = ['index', 'login', 'register', 'disclaimer', 'static']
    if not is_logged_in() and request.endpoint not in public_routes:
        return redirect(url_for('login'))


# === ROUTES PUBLIQUES ===
@app.route("/")
def index():
    return render_page("index.html")


# === ROUTES À COMPLÉTER ===
# Ajouter ici login, register, menu, dashboard, missions, etc.


# === POINT D'ENTRÉE ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

@app.route("/dashboard")
def dashboard():
    if not is_logged_in() or session.get("username") != "Topaz":
        return render_page("unauthorized.html"), 403
    return render_page("dashboard.html")
