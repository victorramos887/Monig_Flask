import os
import sys
from time import sleep
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def test_cadastro_escola(app, assert_response, new_escolas):

    response = app.test_client().post(
        'api/v1/cadastros/escolas',
        data = {
            **new_escolas
        }
    )
    data = response.get_json()
    # assert_response(response, 200, "application/json", True)
    assert response.status == '200 OK'
    assert data['id_escola'] == 1


def test_cadastro_edificios(app, assert_response, new_edificios):
        # Teste 2
    response = app.test_client().post(
        '/api/v1/cadastros/edificios',
        data={
            **new_edificios
        })
    assert response.status == '200 OK'
    
    # assert_response(response, 200, "text/html; charset=utf-8", b"<!DOCTYPE html>")



def test_cadastro_area_umida(app, assert_response, new_area_umida):

    response = app.test_client().post(
        '/api/v1/cadastros/area-umida',
        data = {
            **new_area_umida
        })

    assert_response(response, 200, "text/html; charset=utf-8", b"<!DOCTYPE html>")


def test_cadastro_equipamentos(app, assert_response, new_equipamentos):

    response =app.test_client().post(
        '/api/v1/cadastros/equipamentos',
        data={
            **new_equipamentos
        }
    )

    assert_response(response, 200, "text/html; charset=utf-8", b"<!DOCTYPE html>")
