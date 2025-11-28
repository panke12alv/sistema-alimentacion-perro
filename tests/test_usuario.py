from src.models.usuario import Usuario

def test_crear_y_buscar_usuario(mysql_test_db):
    # Crear un usuario de prueba
    u = Usuario.crear("Lupita")

    # Verifico que se asignó un ID
    assert u.id is not None

    # Busco el usuario creado por su ID
    found = Usuario.buscar_por_id(u.id)

    # Verifico que los datos coincidan
    assert found.nombre == "Lupita"
    assert found.rol == "DUENO"
