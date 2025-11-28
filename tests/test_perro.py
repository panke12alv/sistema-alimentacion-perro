from src.models.perro import Perro

def test_crear_y_buscar_perro(mysql_test_db):
    """
    Este test verifica que se pueda crear un perro en la base de datos
    y que luego se pueda buscar por su ID correctamente.
    """

    # Creamos un perro de ejemplo
    p = Perro.crear("Fido", "Labrador", 3, 20.5, "Ana")

    # Comprobamos que el ID del perro se haya generado (registro exitoso)
    assert p.id is not None

    # Buscamos el perro en la base de datos usando su ID
    found = Perro.buscar_por_id(p.id)

    # Verificamos que el nombre coincida con el que registramos
    assert found.nombre == "Fido"

    # Verificamos que el peso coincida aproximadamente con el que registramos
    assert abs(found.peso - 20.5) < 0.01
