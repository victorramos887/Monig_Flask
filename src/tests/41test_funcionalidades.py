import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def test_quantidade_de_areas_umidas_do_edificio_selecionado(app):
    response = app.test_client().get(
        'api/v1/funcionalidades/quantidades_au_edificio?=1'
    )
    assert response.status_code == 200