import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv("PGHOST"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    dbname=os.getenv("PGDATABASE"),
    port=os.getenv("PGPORT", 5432)
)

cur = conn.cursor()

# Supprimer les tables si elles existent
tables = ['donations', 'invitation_codes', 'user']
for table in tables:
    cur.execute(f'DROP TABLE IF EXISTS {table} CASCADE;')

conn.commit()
cur.close()
conn.close()

print("🧨 Base de données réinitialisée (tables supprimées).")
