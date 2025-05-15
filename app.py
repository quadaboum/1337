from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os

# === CONFIGURATION DE BASE ===
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "topaz_secret_key")


# === OUTILS FONCTIONNELS ===
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
    return render_template("index.html", version=load_version())


# === ROUTES À COMPLÉTER ===
# Ajouter ici login, register, menu, dashboard, missions, etc.

