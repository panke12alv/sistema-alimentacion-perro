from dataclasses import dataclass
from src.db_connection import get_conn

@dataclass
class Alimento:
    id: int
    tipo: str
    marca: str
    calorias_por_100g: float
    unidad: str = "g"

    @classmethod
    def crear(cls, tipo, marca, calorias_por_100g):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO alimentos (tipo, marca, calorias_por_100g, unidad) VALUES (%s,%s,%s,%s)",
                (tipo, marca, calorias_por_100g, "g")
            )
            conn.commit()
            aid = cur.lastrowid
            return cls(aid, tipo, marca, calorias_por_100g)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, tipo, marca, calorias_por_100g, unidad FROM alimentos ORDER BY tipo")
            rows = cur.fetchall()
            return [cls(*r) for r in rows]
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, tipo, marca, calorias_por_100g, unidad FROM alimentos WHERE id=%s", (id_,))
            r = cur.fetchone()
            return cls(*r) if r else None
        finally:
            cur.close()
            conn.close()

    def describir(self):
        return f"{self.tipo} ({self.marca}) — {self.calorias_por_100g} kcal/100g"

    def calcular_porcion(self, perro):
        factor_edad = 1.0
        if perro.edad < 1: factor_edad = 1.5
        elif perro.edad > 8: factor_edad = 0.9
        porcion = 30 * perro.peso * factor_edad
        return porcion
