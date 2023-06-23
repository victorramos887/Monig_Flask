import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def test_get_escolas(app):
    response = app.test_client().get(
        'api/v1/send_frontend/escolas')

    assert response.status_code == 200


def test_get_edificios(app):
    response = app.test_client().get(
        'api/v1/send_frontend/edificios?=1'
    )
    assert response.status_code == 200

def test_get_areas_umidas(app):
    response = app.test_client().get(
        'api/v1/send_frontend/area_umidas?=1'
    )
    assert response.status_code == 200

def test_get_equipamentos(app):
    response = app.test_client().get(
        'api/v1/send_frontend/equipamentos?=1'
    )
    assert response.status_code == 200
