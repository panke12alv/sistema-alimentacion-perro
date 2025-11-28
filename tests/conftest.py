# tests/conftest.py
import os
import pytest
from src.db_connection import create_connection
import mysql.connector

@pytest.fixture(scope="session")
def mysql_test_db():
    # crear DB de pruebas
    cfg = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "")
    }
    conn = mysql.connector.connect(**cfg)
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS dogfeeder_test;")
    cur.execute("CREATE DATABASE dogfeeder_test;")
    conn.commit()
    cur.close()
    conn.close()
    # modificar temporalmente DB_NAME para tests
    os.environ["DB_NAME"] = "dogfeeder_test"
    # ejecutar schema
    from src.init_db import run_schema
    run_schema()
    yield
    # teardown
    conn = mysql.connector.connect(**cfg)
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS dogfeeder_test;")
    conn.commit()
    cur.close()
    conn.close()
