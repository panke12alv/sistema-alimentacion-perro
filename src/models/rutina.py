from dataclasses import dataclass
from typing import List
from src.db_connection import get_conn

@dataclass
class RutinaAlimentacion:
    id: int = None
    perro_id: int = None
    alimentos_ids: List[int] = None
    horarios: str = ""  # ejemplo '08:00,18:00'
    cantidad_total_por_dia: float = 0.0

    @classmethod
    def crear_o_actualizar(cls, perro_id, alimentos_ids, horarios, cantidad_total_por_dia):
        conn = get_conn()
        try:
            cur = conn.cursor()
            # convierto lista de ids a string separado por coma
            alimentos_str = ",".join(str(i) for i in alimentos_ids)
            # reviso si ya existe rutina para este perro
            cur.execute("SELECT id FROM rutinas WHERE perro_id=%s", (perro_id,))
            row = cur.fetchone()
            if row:
                # actualizo rutina existente
                cur.execute(
                    "UPDATE rutinas SET alimentos_ids=%s, horarios=%s, cantidad_total_por_dia=%s WHERE id=%s",
                    (alimentos_str, horarios, cantidad_total_por_dia, row[0])
                )
                rutina_id = row[0]
            else:
                # creo nueva rutina
                cur.execute(
                    "INSERT INTO rutinas (perro_id, alimentos_ids, horarios, cantidad_total_por_dia) VALUES (%s,%s,%s,%s)",
                    (perro_id, alimentos_str, horarios, cantidad_total_por_dia)
                )
                rutina_id = cur.lastrowid
            conn.commit()
            return cls(rutina_id, perro_id, alimentos_ids, horarios, cantidad_total_por_dia)
        finally:
            cur.close()
            conn.close()
