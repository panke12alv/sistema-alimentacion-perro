from src.models.alimento import Alimento
from src.models.perro import Perro

def test_crear_alimento_y_calcula_porcion(mysql_test_db):
    """
    Este test verifica dos cosas:
    1. Que se pueda crear un alimento correctamente en la base de datos de test.
    2. Que el método calcular_porcion funcione y devuelva un valor positivo.
    """

    # Crear un alimento de ejemplo
    a = Alimento.crear("Seco", "MarcaX", 350)

    # Crear un perro de ejemplo
    p = Perro.crear("Luna", "Beagle", 2, 10, "Carlos")

    # Calcular la porción recomendada para este perro
    por = a.calcular_porcion(p)

    # Comprobamos que la porción sea un valor positivo
    assert por > 0

    # Comprobamos que la porción calculada sea la esperada:
    # 30g * peso en kg * factor_edad
    # Para un perro de 2 años, factor_edad = 1.0
    assert abs(por - (30 * 10)) < 1e-6
