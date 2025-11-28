from src.models.rutina import RutinaAlimentacion
from src.models.perro import Perro

def test_crear_rutina_simple(mysql_test_db):
    """
    Este test verifica que se pueda crear una rutina de alimentación para un perro
    y que los datos se guarden correctamente.
    """

    # Creamos un perro de ejemplo
    p = Perro.crear("Nico", "Mixto", 0, 3, "Mamá")

    # Creamos o actualizamos la rutina del perro con un alimento (id=1),
    # horarios a las 08:00 y 18:00, y cantidad total diaria de 150g
    r = RutinaAlimentacion.crear_o_actualizar(p.id, [1], "08:00,18:00", 150)

    # Verificamos que la rutina pertenezca al perro que creamos
    assert r.perro_id == p.id

    # Comprobamos que los horarios contengan la hora 08:00
    assert "08:00" in r.horarios
