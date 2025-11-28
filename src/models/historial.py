# src/models/historial.py
from dataclasses import dataclass
from src.db_connection import get_conn
from src.models.perro import Perro
from src.models.alimento import Alimento

@dataclass
class HistorialComida:
    id: int
    perro_id: int
    alimento_id: int
    cantidad: float
    fecha: str
    notas: str = None

    @classmethod
    def registrar(cls, perro_id, alimento_id, cantidad, notas=None):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO comidas (perro_id, alimento_id, cantidad, notas) VALUES (%s,%s,%s,%s)",
                        (perro_id, alimento_id, cantidad, notas))
            conn.commit()
            cid = cur.lastrowid
            cur.execute("SELECT fecha FROM comidas WHERE id=%s", (cid,))
            fecha = cur.fetchone()[0]
            return cls(cid, perro_id, alimento_id, cantidad, fecha, notas)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_por_perro(cls, perro_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, perro_id, alimento_id, cantidad, fecha, notas FROM comidas WHERE perro_id=%s ORDER BY fecha DESC", (perro_id,))
            rows = cur.fetchall()
            return [cls(*r) for r in rows]
        finally:
            cur.close()
            conn.close()
