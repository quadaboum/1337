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

def initialize_database():
    with open("schema.sql", "r") as f:
        sql_code = f.read()

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql_code)
        conn.commit()
        print("✅ Base de données initialisée avec succès.")
    except Exception as e:
        print("❌ Erreur lors de l'initialisation :", e)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    initialize_database()
