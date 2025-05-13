
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
