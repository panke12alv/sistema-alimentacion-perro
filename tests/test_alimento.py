from src.models.alimento import Alimento
from src.models.perro import Perro

def test_crear_alimento_y_calcula_porcion(mysql_test_db):
    a = Alimento.crear("Seco", "MarcaX", 350)
    p = Perro.crear("Luna", "Beagle", 2, 10, "Carlos")
    por = a.calcular_porcion(p)
    assert por > 0
    # esperada: 30g * kg * factor_edad (beagle 2 años => factor 1.0)
    assert abs(por - (30 * 10)) < 1e-6
