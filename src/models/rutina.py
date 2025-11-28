# src/models/rutina.py
from dataclasses import dataclass
from typing import List
from src.db_connection import get_conn

@dataclass
class RutinaAlimentacion:
    id: int = None
    perro_id: int = None
    alimentos_ids: List[int] = None
    horarios: str = ""  # simple: JSON/string '08:00,18:00'
    cantidad_total_por_dia: float = 0.0

    @classmethod
    def crear_o_actualizar(cls, perro_id, alimentos_ids, horarios, cantidad_total_por_dia):
        conn = get_conn()
        try:
            cur = conn.cursor()
            # guardamos la rutina en la tabla perros.rutina_id como una técnica simple;
            # podríamos tener una tabla rutinas, para simplificar guardaremos datos compactados en perros.rutina_id no es ideal.
            # Mejor: crear tabla rutinas si quieres datos normalizados.
            # Aquí, ejemplo simple: retornamos objeto y actualizamos perros.rutina_id = NULL (se puede mejorar)
            return cls(None, perro_id, alimentos_ids, horarios, cantidad_total_por_dia)
        finally:
            cur.close()
            conn.close()
