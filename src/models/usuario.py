# src/models/usuario.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.db_connection import get_conn

@dataclass
class Usuario:
    id: Optional[int]
    nombre: str
    email: Optional[str] = None
    password_hash: Optional[str] = None
    fecha_registro: Optional[datetime] = None
    rol: str = "DUEÑO"  # DUEÑO or VETERINARIO

    @classmethod
    def crear(cls, nombre, email=None, password_hash=None, rol="DUEÑO"):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombre, email, password_hash, fecha_registro, rol) VALUES (%s, %s, %s, NOW(), %s)",
                (nombre, email, password_hash, rol)
            )
            conn.commit()
            uid = cur.lastrowid
            return cls(uid, nombre, email, password_hash, None, rol)
        finally:
            cur.close()
            conn.close()

    # Nota: en este ejemplo simple asumimos existencia de tabla usuarios si la deseas,
    # pero para cubrir el requisito de 3 tablas principales la app usa perros, alimentos, comidas.
