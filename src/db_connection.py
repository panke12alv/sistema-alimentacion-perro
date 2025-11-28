import os
from mysql.connector import pooling, Error
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "dogfeeder_db"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "autocommit": False,
    "charset": "utf8mb4",
}

POOL_NAME = os.getenv("POOL_NAME", "df_pool")
POOL_SIZE = int(os.getenv("POOL_SIZE", 5))

_pool = None

def get_conn():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name=POOL_NAME,
            pool_size=POOL_SIZE,
            **DB_CONFIG
        )
    return _pool.get_connection()

def create_connection():
    # conexión simple (útil para scripts de init)
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        return conn
    except Error as e:
        print("Error connecting:", e)
        return None
