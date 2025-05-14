import psycopg2
import os

# Connexion à PostgreSQL via les variables d'environnement
conn = psycopg2.connect(
    host=os.getenv("PGHOST"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    dbname=os.getenv("PGDATABASE"),
    port=os.getenv("PGPORT", 5432)
)

cur = conn.cursor()

# Exemple de structure minimale (adaptée à ton projet)
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    level INTEGER DEFAULT 1,
    prestige INTEGER DEFAULT 0,
    argent INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS invitation_codes (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    used_by TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS donations (
    id SERIAL PRIMARY KEY,
    username TEXT,
    montant INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
cur.close()
conn.close()

print("✅ Base de données initialisée avec succès.")
