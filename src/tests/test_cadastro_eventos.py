import os
import sys
from time import sleep
import json

from dotenv import load_dotenv

from datetime import datetime, date


#Importar Testes
from src.tests.test_cadastros import test_cadastro_escola

# Define o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))



# Caminho para o arquivo .env
ENV_PATH = os.path.join(sys.path[0], '.env')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(ENV_PATH)


def date_encoder(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()  # Converte para string no formato ISO 8601
    raise TypeError("Object of type %s is not JSON serializable" % type(obj))


def test_cadastro_tipo_eventos_ocasional(app, authenticated_app, new_escolas, new_tipo_evento_ocasional):
    with app.app_context():
        
        test_cadastro_escola(app, authenticated_app, new_escolas)

        json_data = json.dumps(new_tipo_evento_ocasional)       
        
        response = app.test_client().post(
            '/api/v1/cadastro-evento/tipo-de-evento-ocasional',
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200


#Teste de cadastro de tipo de evento recorrente
def test_cadastro_tipo_eventos_recorrente(app, authenticated_app, new_escolas, new_tipo_evento_recorrente):
    """Teste de cadastro de tipo de evento."""


    with app.app_context():
        test_cadastro_escola(app, authenticated_app, new_escolas)

        json_dump = json.dumps(new_tipo_evento_recorrente)

        
        # Mocka a requisição
        response = app.test_client().post(
            "/api/v1/cadastro-evento/tipo-evento-recorrente",
            data=json_dump,
            content_type='application/json'
            )

        # Valida a resposta 
        assert response.status_code == 200

#Cadastro de evento tipo ocasional

def test_cadastro_evento_ocasional(app, authenticated_app, new_evento_ocasional, new_tipo_evento_ocasional, new_escolas):

    with app.app_context():
        test_cadastro_tipo_eventos_recorrente(app, authenticated_app, new_escolas, new_tipo_evento_ocasional)


        new_evento_ocasional['tipo_de_evento'] = new_tipo_evento_ocasional["nome_do_evento"]

        json_data = json.dumps(new_evento_ocasional)
        print("Json Ocasional: ", json_data)
        response = app.test_client().post(
            '/api/v1/cadastro-evento/eventos',
            data=json_data,
            content_type='application/json'
        )

        # Valida a resposta 
        assert response.status_code == 200

#Cadastro de evento tipo ocasional

def test_cadastro_evento_recorrente(app, authenticated_app, new_evento_recorrente, new_escolas, new_tipo_evento_recorrente):

    with app.app_context():
        # test_cadastro_escola(app, authenticated_app, new_escolas)
        test_cadastro_tipo_eventos_recorrente(app, authenticated_app, new_escolas, new_tipo_evento_recorrente)


        new_evento_recorrente['tipo_de_evento'] = new_tipo_evento_recorrente["nome_do_evento"]

        json_data = json.dumps(new_evento_recorrente)

        response = app.test_client().post(
            '/api/v1/cadastro-evento/eventos',
            data=json_data,
            content_type='application/json'
        )

        # Valida a resposta 
        assert response.status_code == 200
        