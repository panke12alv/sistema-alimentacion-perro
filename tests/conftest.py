# tests/conftest.py
import os
import pytest
from src.db_connection import create_connection  # no se usa aquí, pero podría servir para conectar
import mysql.connector

# Fixture de Pytest para crear y manejar una base de datos de prueba
@pytest.fixture(scope="session")
def mysql_test_db():
    """
    Esta función crea una base de datos temporal para ejecutar los tests.
    Se ejecuta una sola vez por sesión de testing.
    """

    # Configuración de conexión a MySQL (usando variables de entorno o valores por defecto)
    cfg = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "")
    }

    # Conectar a MySQL y preparar cursor
    conn = mysql.connector.connect(**cfg)
    cur = conn.cursor()

    # Asegurarnos de empezar desde cero: eliminamos cualquier base de datos previa de test
    cur.execute("DROP DATABASE IF EXISTS dogfeeder_test;")
    # Creamos la base de datos de test
    cur.execute("CREATE DATABASE dogfeeder_test;")
    conn.commit()

    # Cerramos la conexión inicial
    cur.close()
    conn.close()

    # Modificamos temporalmente la variable de entorno DB_NAME para que use la base de datos de test
    os.environ["DB_NAME"] = "dogfeeder_test"

    # Ejecutamos el schema (tablas) en la base de datos de test
    from src.init_db import run_schema
    run_schema()

    # yield permite que los tests se ejecuten con esta DB de prueba
    yield

    # Teardown: después de los tests, eliminamos la base de datos de test
    conn = mysql.connector.connect(**cfg)
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS dogfeeder_test;")
    conn.commit()
    cur.close()
    conn.close()
