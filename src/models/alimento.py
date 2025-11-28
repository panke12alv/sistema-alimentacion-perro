from dataclasses import dataclass
from src.db_connection import get_conn  # importamos la función para conectarnos a la base de datos

@dataclass
class Alimento:
    # Esta clase representa un alimento que se le puede dar a un perro
    id: int  # identificador único en la base de datos
    tipo: str  # tipo de alimento (ej. Seco, Húmedo)
    marca: str  # marca del alimento
    calorias_por_100g: float  # cantidad de calorías por cada 100 gramos
    unidad: str = "g"  # unidad de medida, por defecto gramos

    @classmethod
    def crear(cls, tipo, marca, calorias_por_100g):
        # Método para crear un nuevo alimento en la base de datos
        conn = get_conn()  # abrimos conexión
        try:
            cur = conn.cursor()
            # insertamos el nuevo alimento en la tabla 'alimentos'
            cur.execute(
                "INSERT INTO alimentos (tipo, marca, calorias_por_100g, unidad) VALUES (%s,%s,%s,%s)",
                (tipo, marca, calorias_por_100g, "g")
            )
            conn.commit()  # confirmamos cambios
            aid = cur.lastrowid  # obtenemos el id generado por la base de datos
            return cls(aid, tipo, marca, calorias_por_100g)  # devolvemos una instancia de Alimento
        finally:
            cur.close()
            conn.close()  # cerramos conexión

    @classmethod
    def listar_todos(cls):
        # Método para obtener todos los alimentos de la base de datos
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, tipo, marca, calorias_por_100g, unidad FROM alimentos ORDER BY tipo")
            rows = cur.fetchall()  # obtenemos todos los resultados
            return [cls(*r) for r in rows]  # devolvemos una lista de objetos Alimento
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_id(cls, id_):
        # Método para buscar un alimento específico usando su id
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, tipo, marca, calorias_por_100g, unidad FROM alimentos WHERE id=%s", (id_,))
            r = cur.fetchone()  # obtenemos el registro
            return cls(*r) if r else None  # devolvemos un objeto Alimento o None si no existe
        finally:
            cur.close()
            conn.close()

    def describir(self):
        # Devuelve una descripción legible del alimento
        return f"{self.tipo} ({self.marca}) — {self.calorias_por_100g} kcal/100g"

    def calcular_porcion(self, perro):
        # Calcula la porción recomendada de este alimento para un perro específico
        factor_edad = 1.0  # factor de ajuste según la edad
        if perro.edad < 1:  # cachorros comen más proporcionalmente
            factor_edad = 1.5
        elif perro.edad > 8:  # perros mayores comen un poco menos
            factor_edad = 0.9
        porcion = 30 * perro.peso * factor_edad  # fórmula básica: 30g por kg de peso ajustado
        return porcion
