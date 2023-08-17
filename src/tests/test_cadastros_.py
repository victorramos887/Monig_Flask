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

def test_cadastro_escola(app, new_escolas):
    # Converte o objeto para JSON
    json_data = json.dumps(new_escolas)
    
    response = app.test_client().post(
        'api/v1/cadastros/escolas',
        data=json_data,
        content_type='application/json'
    )
    
    data = response.get_json()

    assert response.status_code == 200
    


def test_cadastro_edificios(app, new_edificios):

    # Execute a lógica do teste
    with app.app_context():
        json_data = json.dumps(new_edificios)
        response = app.test_client().post(
            'api/v1/cadastros/edificios',
            data=json_data,
            content_type='application/json'
        )
        
        # Verifique o código de status da resposta
        assert response.status_code == 200
        

def test_cadastro_area_umida(app, new_area_umida):

    with app.app_context():
        json_data = json.dumps(new_area_umida)

        response = app.test_client().post(
            'api/v1/cadastros/area-umida',
            data=json_data,
            content_type='application/json'
        )

        response_dict = json.loads(response.get_data())

        print(response_dict)
        assert response.status_code == 200


def test_cadastro_equipamento(app, new_equipamentos):

    with app.app_context():

        json_data = json.dumps(new_equipamentos)

        response = app.test_client().post(
            'api/v1/cadastros/equipamentos',
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200



def test_cadastro_populacao(app, new_populacao):

    with app.app_context():

        json_data = json.dumps(new_populacao)

        response = app.test_client().post(
            'api/v1/cadastros/populacao',
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200


def test_cadastro_hidrometro(app, new_hidrometro):

    with app.app_context():

        json_data = json.dumps(new_hidrometro)

        response = app.test_client().post(
            'api/v1/cadastros/hidrometros',
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200


def test_cadastro_reservatorio(app, new_reservatorio):

    with app.app_context():
        
        json_data = json.dumps(new_reservatorio)

        response = app.test_client().post(
            'api/v1/cadastros/reservatorios',
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200