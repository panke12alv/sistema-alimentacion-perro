from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.db_connection import get_conn

@dataclass
class Usuario:
    id: Optional[int]
    nombre: str
    fecha_registro: Optional[datetime] = None
    rol: str = "DUENO"

    @classmethod
    def crear(cls, nombre: str, rol: str = "DUENO"):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombre, rol, fecha_registro) VALUES (%s, %s, NOW())",
                (nombre, rol)
            )
            conn.commit()
            uid = cur.lastrowid
            return cls(uid, nombre, datetime.now(), rol)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_id(cls, id_: int):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, nombre, fecha_registro, rol FROM usuarios WHERE id=%s",
                (id_,)
            )
            r = cur.fetchone()
            return cls(*r) if r else None
        finally:
            cur.close()
            conn.close()
