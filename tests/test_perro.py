from src.models.perro import Perro

def test_crear_y_buscar_perro(mysql_test_db):
    p = Perro.crear("Fido", "Labrador", 3, 20.5, "Ana")
    assert p.id is not None
    found = Perro.buscar_por_id(p.id)
    assert found.nombre == "Fido"
    assert abs(found.peso - 20.5) < 0.01
