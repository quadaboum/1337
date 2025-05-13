
import psycopg2
import os

def init_db():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "voie_eclipse"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASS", "password")
    )
    cur = conn.cursor()
    with open("schema.sql", "r") as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()
    print("Base de données initialisée.")

if __name__ == "__main__":
    init_db()
