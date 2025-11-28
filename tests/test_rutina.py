from src.models.rutina import RutinaAlimentacion
from src.models.perro import Perro

def test_crear_rutina_simple(mysql_test_db):
    p = Perro.crear("Nico", "Mixto", 0, 3, "Mamá")
    r = RutinaAlimentacion.crear_o_actualizar(p.id, [1], "08:00,18:00", 150)
    assert r.perro_id == p.id
    assert "08:00" in r.horarios
