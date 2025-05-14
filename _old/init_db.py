import psycopg2
import os

def init_db():
    conn = psycopg2.connect(
        host=os.environ.get("PGHOST"),
        database=os.environ.get("PGDATABASE"),
        user=os.environ.get("PGUSER"),
        password=os.environ.get("PGPASSWORD"),
        port=os.environ.get("PGPORT", 5432)
    )
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
        ip_address TEXT,
        user_agent TEXT,
        used_invitation_code TEXT
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
    print("Base de données initialisée avec succès.")

if __name__ == "__main__":
    init_db()