from dataclasses import dataclass
from src.db_connection import get_conn
from src.models.perro import Perro
from src.models.alimento import Alimento
from datetime import datetime

@dataclass
class HistorialComida:
    """
    Clase que representa un registro de comida para un perro.
    Cada registro indica qué alimento, en qué cantidad y en qué fecha se administró.
    """
    id: int
    perro_id: int
    alimento_id: int
    cantidad: float
    fecha: str
    notas: str = None  # opcional, para observaciones o comentarios

    # ------------------- Métodos de clase -------------------

    @classmethod
    def registrar(cls, perro_id, alimento_id, cantidad, notas=None):
        """
        Registra una nueva comida en la base de datos.
        Devuelve un objeto HistorialComida con los datos guardados.
        """
        conn = get_conn()
        try:
            cur = conn.cursor()
            # Inserta el registro en la tabla 'comidas'
            cur.execute(
                "INSERT INTO comidas (perro_id, alimento_id, cantidad, notas) VALUES (%s,%s,%s,%s)",
                (perro_id, alimento_id, cantidad, notas)
            )
            conn.commit()
            cid = cur.lastrowid  # obtiene el id del registro recién creado

            # Obtenemos la fecha asignada automáticamente por MySQL
            cur.execute("SELECT fecha FROM comidas WHERE id=%s", (cid,))
            fecha = cur.fetchone()[0]

            return cls(cid, perro_id, alimento_id, cantidad, fecha, notas)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_por_perro(cls, perro_id):
        """
        Obtiene todos los registros de comida de un perro específico,
        ordenados de más reciente a más antiguo.
        Devuelve una lista de objetos HistorialComida.
        """
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, perro_id, alimento_id, cantidad, fecha, notas "
                "FROM comidas WHERE perro_id=%s ORDER BY fecha DESC",
                (perro_id,)
            )
            rows = cur.fetchall()
            return [cls(*r) for r in rows]
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todos(cls):
        """
        Obtiene todos los registros de comida de todos los perros,
        ordenados de más reciente a más antiguo.
        Devuelve una lista de objetos HistorialComida.
        """
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, perro_id, alimento_id, cantidad, fecha, notas "
                "FROM comidas ORDER BY fecha DESC"
            )
            rows = cur.fetchall()
            return [cls(*r) for r in rows]
        finally:
            cur.close()
            conn.close()
