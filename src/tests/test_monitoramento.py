import os
import sys
from time import sleep
import json
from dotenv import load_dotenv
from datetime import datetime, date
from pprint import pprint
# Import teste
from test_cadastros_ import test_cadastro_hidrometro

# Define o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))


# Caminho para o arquivo .env
ENV_PATH = os.path.join(sys.path[0], '.env')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(ENV_PATH)


def date_encoder(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()  # Converte para string no formato ISO 8601
    raise TypeError("Object of type %s is not JSON serializable" % type(obj))


def test_cadastro_de_monitoramento(app, authenticated_app, new_escolas, new_edificios, new_hidrometro, new_monitoramento):

    with app.app_context():
        test_cadastro_hidrometro(
            app, authenticated_app, new_escolas, new_edificios, new_hidrometro)

        # json_data = json.dumps(new_monitoramento)


        json_data = {
            "fk_escola": 1,
            "hidrometro": "xxxxxxx",
            "leitura": "200,000",
            "hora": "07:00",
            "data": "01/01/2024"
        }
        response = app.test_client().post(
            'api/v1/monitoramento/cadastrarleitura',
            data=json.dumps(json_data),
            content_type='application/json'
        )

        print("Response:", response.get_data())
        assert response.status_code == 200


def teste_cadastro_de_dois_monitoramento(app, authenticated_app, new_escolas, new_edificios, new_hidrometro):

    with app.app_context():
        test_cadastro_hidrometro(
            app, authenticated_app, new_escolas, new_edificios, new_hidrometro)

        # 1º leitura correta
        json_1 = {
            "fk_escola": 1,
            "hidrometro": "xxxxxxx",
            "leitura": "200,000",
            "hora": "07:00",
            "data": "01/01/2024"
        }

        # 2º Leitura Correta
        json_2 = {
            "fk_escola": 1,
            "hidrometro": "xxxxxxx",
            "leitura": "200,150",
            "hora": "19:00",
            "data": "01/01/2024"
        }

        # Cadastrar primeira leitura

        response_01 = app.test_client().post(
            'api/v1/monitoramento/cadastrarleitura',
            data=json.dumps(json_1),
            content_type='application/json'
        )

        assert response_01.status_code == 200

        response_02 = app.test_client().post(
            'api/v1/monitoramento/cadastrarleitura',
            data=json.dumps(json_2),
            content_type='application/json'
        )

        assert response_02.status_code == 200


def teste_cadastro_de_tres_monitoramento(app, authenticated_app, new_escolas, new_edificios, new_hidrometro):

    with app.app_context():
        teste_cadastro_de_dois_monitoramento(
            app, authenticated_app, new_escolas, new_edificios, new_hidrometro)
        # 3º leitura errada
        json_3 = {
            "fk_escola": 1,
            "hidrometro": "xxxxxxx",
            "leitura": "200,500",
            "hora": "20:00",
            "data": "01/01/2024"
        }

        response_03 = app.test_client().post(
            'api/v1/monitoramento/cadastrarleitura',
            data=json.dumps(json_3),
            content_type='application/json'
        )

        # não é permitido criar mais de duas leituras por dia
        assert response_03.status_code == 400


# Cadastrar monitoramento menor do que o anterior
def test_cadastrar_monitoramento_menor_do_que_o_anterior(app, authenticated_app, new_escolas, new_edificios, new_hidrometro, new_monitoramento):

    with app.app_context():

        test_cadastro_de_monitoramento(
            app, authenticated_app, new_escolas, new_edificios, new_hidrometro, new_monitoramento)

        json_leitura_erro = {
            "fk_escola": 1,
            "hidrometro": "xxxxxxx",
            "leitura": "190,999",
            "hora": "20:00",
            "data": "01/01/2024"
        }

        response = app.test_client().post(
            'api/v1/monitoramento/cadastrarleitura',
            data=json.dumps(json_leitura_erro),
            content_type='application/json'
        )
        decoded_json = response.get_data().decode('utf-8')# Decodificar a string JSON
        json_obj = json.loads(decoded_json)# Carregar o JSON em um objeto Python

        assert response.status_code == 400 #não é permitido criar um leitura com valor menor que a anterior     
        assert json_obj['mensagem'] == "Não é possível inserir um valor menor do que o anterior!!"