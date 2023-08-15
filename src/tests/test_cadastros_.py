import os
import sys
from time import sleep
import json



from dotenv import load_dotenv

# Define o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
print(sys.path)
# Caminho para o arquivo .env
ENV_PATH = os.path.join(sys.path[0], '.env')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(ENV_PATH)

def test_cadastro_escola(app, assert_response, new_escolas):
    # Converte o objeto para JSON
    json_data = json.dumps(new_escolas.to_json())
    
    response = app.test_client().post(
        'api/v1/cadastros/escolas',
        data=json_data,
        content_type='application/json'
    )
    
    data = response.get_json()
    assert response.status_code == 200
    assert data['id_escola'] == 1


# def test_cadastro_edificios(app, assert_response, new_edificios):
#         # Teste 2
#     response = app.test_client().post(
#         '/api/v1/cadastros/edificios',
#         data={
#             **new_edificios
#         })
#     assert response.status == '200 OK'
    
#     # assert_response(response, 200, "text/html; charset=utf-8", b"<!DOCTYPE html>")



# def test_cadastro_area_umida(app, assert_response, new_area_umida):

#     response = app.test_client().post(
#         '/api/v1/cadastros/area-umida',
#         data = {
#             **new_area_umida
#         })

#     assert_response(response, 200, "text/html; charset=utf-8", b"<!DOCTYPE html>")


# def test_cadastro_equipamentos(app, assert_response, new_equipamentos):

#     response =app.test_client().post(
#         '/api/v1/cadastros/equipamentos',
#         data={
#             **new_equipamentos
#         }
#     )

#     assert_response(response, 200, "text/html; charset=utf-8", b"<!DOCTYPE html>")
