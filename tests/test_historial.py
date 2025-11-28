from src.models.perro import Perro
from src.models.alimento import Alimento
from src.models.historial import HistorialComida

def test_registrar_comida(mysql_test_db):
    p = Perro.crear("Coco", "Pug", 4, 8, "Laura")
    a = Alimento.crear("Humedo", "MarcaY", 120)
    h = HistorialComida.registrar(p.id, a.id, 80, notas="Cena")
    assert h.id is not None
    historial = HistorialComida.obtener_por_perro(p.id)
    assert len(historial) >= 1
    assert historial[0].cantidad == 80
