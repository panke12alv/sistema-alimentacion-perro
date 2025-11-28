from src.models.perro import Perro
from src.models.alimento import Alimento
from src.models.historial import HistorialComida

def test_registrar_comida(mysql_test_db):
    """
    Este test verifica que se pueda registrar una comida correctamente
    y que luego se pueda recuperar del historial del perro.
    """

    # Crear un perro de ejemplo
    p = Perro.crear("Coco", "Pug", 4, 8, "Laura")

    # Crear un alimento de ejemplo
    a = Alimento.crear("Humedo", "MarcaY", 120)

    # Registrar una comida en el historial para este perro
    h = HistorialComida.registrar(p.id, a.id, 80, notas="Cena")

    # Comprobamos que la comida registrada tenga un ID asignado (existe en la BD)
    assert h.id is not None

    # Obtener todo el historial de comidas de este perro
    historial = HistorialComida.obtener_por_perro(p.id)

    # Comprobamos que haya al menos un registro en el historial
    assert len(historial) >= 1

    # Comprobamos que la cantidad registrada sea la misma que ingresamos
    assert historial[0].cantidad == 80
