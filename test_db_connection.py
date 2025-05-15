import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.environ.get("PGHOST"),
        database=os.environ.get("PGDATABASE"),
        user=os.environ.get("PGUSER"),
        password=os.environ.get("PGPASSWORD"),
        port=os.environ.get("PGPORT", 5432)
    )
    print("✅ Connexion à la base PostgreSQL réussie.")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users LIMIT 1;")
    result = cur.fetchone()
    if result:
        print("📄 Exemple d'utilisateur :", result)
    else:
        print("⚠️ Aucune donnée dans la table 'users'.")
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Erreur lors de la connexion ou de la requête SQL :")
    print(e)
