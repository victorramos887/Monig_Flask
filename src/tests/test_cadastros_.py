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


def test_cadastro_cliente(app, new_cliente):

    with app.app_context():
        
        json_data = json.dumps(new_cliente)

        response = app.test_client().post(
            'api/v1/cadastros/cliente',
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200


def test_cadastro_usuario(app, new_usuario):

    with app.app_context():
        
        json_data = json.dumps(new_usuario)

        response = app.test_client().post(
            'api/v1/cadastros/usuario',
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200

def test_cadastro_tipo_eventos(app, new_tipo_evento):

    with app.app_context():

        json_data = json.dumps(new_tipo_evento)

        response = app.test_client().post(
            '/api/v1/cadastro-evento/tipo-evento',
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200

def test_tipo_evento_post(app, new_tipo_evento):
    """Teste de cadastro de tipo de evento."""
    # Mocka a requisição
    response = app.test_client().post("/api/v1/cadastro-evento/tipo-evento", json=new_tipo_evento)

    # Valida a resposta
    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "mensagem": "Cadastro Realizado",
        "data": {
            "nome_do_evento": "Evento de teste",
            "periodicidade": "Diário",
            "sazonal_periodo": "2023-08-22",
            "requer_acao": True,
            "tempo_de_tolerancia": 24,
            "unidade_de_tempo": "Horas",
            "acao": "Sim",
            "resposta": "Resposta do evento de teste",
        },
    }

def valor_test_cadastro_eventos(app, new_evento):


    with app.app_context():

        json_data = json.dumps(new_evento)
        
        response = app.test_client().post(
            'api/v1/...',
            data=json_data,
            context_type='application/json'
        )