from werkzeug.security import generate_password_hash
import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("PGHOST"),
        database=os.environ.get("PGDATABASE"),
        user=os.environ.get("PGUSER"),
        password=os.environ.get("PGPASSWORD"),
        port=os.environ.get("PGPORT", 5432)
    )

def create_topaz():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE pseudo = %s", ('Topaz',))
    if not cur.fetchone():
        hashed_pw = generate_password_hash("azertyuiop")
        cur.execute(
            "INSERT INTO users (nom, pseudo, password, niveau) VALUES (%s, %s, %s, %s)",
            ('Topaz', 'Topaz', hashed_pw, 666)
        )
        conn.commit()
        print("Topaz créé avec succès.")
    else:
        print("Topaz existe déjà.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_topaz()
