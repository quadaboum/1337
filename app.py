from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
import os
import secrets
import string

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

@app.route("/test_db")
def test_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return f"Connexion PostgreSQL réussie : {db_version[0]}"
    except Exception as e:
        return f"Erreur de connexion : {str(e)}"

@app.route("/init_db")
def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                nom TEXT,
                pseudo TEXT UNIQUE,
                password TEXT,
                niveau INTEGER DEFAULT 1,
                prestige INTEGER DEFAULT 0,
                argent INTEGER DEFAULT 0,
                dons INTEGER DEFAULT 0,
                ip_address TEXT
            );
            CREATE TABLE IF NOT EXISTS invitation_codes (
                id SERIAL PRIMARY KEY,
                code TEXT UNIQUE,
                used BOOLEAN DEFAULT FALSE,
                used_by_user_id INTEGER REFERENCES users(id)
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        return "Base de données initialisée avec succès."
    except Exception as e:
        return f"Erreur lors de l'initialisation : {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
