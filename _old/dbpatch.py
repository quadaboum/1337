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

def add_used_invitation_code_column():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            ALTER TABLE users
            ADD COLUMN IF NOT EXISTS used_invitation_code TEXT;
        """)
        conn.commit()
        print("✅ Colonne used_invitation_code ajoutée.")
    except Exception as e:
        print("❌ Erreur :", e)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    add_used_invitation_code_column()
