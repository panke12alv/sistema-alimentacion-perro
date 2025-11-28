# src/init_db.py
import os
from src.db_connection import create_connection
def run_schema():
    conn = create_connection()
    if not conn:
        print("No se pudo conectar para crear la BD. Revisa credenciales.")
        return
    with open(os.path.join(os.path.dirname(__file__), "sql", "schema.sql"), "r") as f:
        sql_script = f.read()
    cur = conn.cursor()
    for stmt in sql_script.split(";"):
        stmt = stmt.strip()
        if stmt:
            try:
                cur.execute(stmt)
            except Exception as e:
                # algunas líneas CREATE DATABASE pueden fallar si ya existe
                print("NOTICE:", e)
    conn.commit()
    cur.close()
    conn.close()
    print("Esquema ejecutado.")
if __name__ == "__main__":
    run_schema()
