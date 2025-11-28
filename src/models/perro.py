from dataclasses import dataclass
from src.db_connection import get_conn

@dataclass
class Perro:
    id: int
    nombre: str
    raza: str
    edad: int
    peso: float
    propietario_nombre: str
    rutina_id: int = None

    @classmethod
    def crear(cls, nombre, raza, edad, peso, propietario_nombre):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO perros (nombre, raza, edad, peso, propietario_nombre) VALUES (%s,%s,%s,%s,%s)",
                (nombre, raza, edad, peso, propietario_nombre)
            )
            conn.commit()
            pid = cur.lastrowid
            return cls(pid, nombre, raza, edad, peso, propietario_nombre)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, raza, edad, peso, propietario_nombre, rutina_id FROM perros ORDER BY nombre")
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
            cur.execute("SELECT id, nombre, raza, edad, peso, propietario_nombre, rutina_id FROM perros WHERE id=%s", (id_,))
            r = cur.fetchone()
            return cls(*r) if r else None
        finally:
            cur.close()
            conn.close()

    def actualizar(self):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE perros SET nombre=%s, raza=%s, edad=%s, peso=%s, propietario_nombre=%s, rutina_id=%s WHERE id=%s",
                (self.nombre, self.raza, self.edad, self.peso, self.propietario_nombre, self.rutina_id, self.id)
            )
            conn.commit()
        finally:
            cur.close()
            conn.close()

    def eliminar(self):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM perros WHERE id=%s", (self.id,))
            conn.commit()
        finally:
            cur.close()
            conn.close()
