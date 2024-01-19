import os
import sys
from time import sleep
import json
from faker import Faker
from dotenv import load_dotenv
from datetime import datetime, date
from random import randint
from dateutil.relativedelta import relativedelta

# Define o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))


# Caminho para o arquivo .env
ENV_PATH = os.path.join(sys.path[0], '.env')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(ENV_PATH)
fake = Faker()
niveis = fake.random_element(
    elements=('Fundamental', 'Médio', 'Superior', 'Creche', 'Berçario', 'CEU'))


def cnpj():
    return f'{randint(0, 9)}{randint(0, 9)}.{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}.{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}/0001-{randint(0, 9)}{randint(0, 9)}'


def date_encoder(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()  # Converte para string no formato ISO 8601
    raise TypeError("Object of type %s is not JSON serializable" % type(obj))


def test_cadastrar_consumo(app, authenticated_app):

    data = datetime.strptime("2023/12/05", "%Y/%m/%d")
    dataFimPeriodo = datetime.strptime("2023/12/05", "%Y/%m/%d")
    dataInicioPeriodo = datetime.strptime("2023/11/05", "%Y/%m/%d")

    headers = {'Authorization': 'Bearer ' + authenticated_app['token']}
    for de in range(0, 2):
        escola = {
            'nome': fake.company(),
            'cnpj': cnpj(),
            'email': fake.email(),
            'telefone': fake.phone_number(),
            'bairro': fake.city_suffix(),
            'cep': fake.postcode(),
            'cidade': fake.city(),
            'estado': fake.state_abbr(),
            'complemento': fake.secondary_address(),
            'logradouro': fake.street_name(),
            'nivel': ['Médio', 'Fundamental'],
            'numero': fake.random_int(min=1, max=1000)
        }

        json_data_escola = json.dumps(escola)
        response = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_data_escola,
            content_type='application/json',
            headers=headers
        )
        decoded_json = response.get_data().decode('utf-8')  # Decodificar a string JSON
        # Carregar o JSON em um objeto Python
        json_obj = json.loads(decoded_json)
        assert response.status_code == 200
        assert json_obj['mensagem'] == 'Cadastro Realizado'
        # print(f"Escola: {de+1}",json_obj)
        hidrometros = json.dumps({
            "fk_edificios": de+1,
            "fk_hidrometro": de+1,
            "hidrometro": fake.company()
        })

        response_hidrometros = app.test_client().post(
            'api/v1/cadastros/hidrometros',
            data=hidrometros,
            content_type='application/json',
            headers=headers
        )

        assert response_hidrometros.status_code == 200
        decoded_json = response_hidrometros.get_data().decode(
            'utf-8')  # Decodificar a string JSON
        # Carregar o JSON em um objeto Python
        json_hidrometro = json.loads(decoded_json)

        for i in range(0, 13):

            data = data + relativedelta(months=1)
            dataFimPeriodo = dataFimPeriodo + relativedelta(months=1)
            dataInicioPeriodo = dataInicioPeriodo + relativedelta(months=1)

            consumo = json.dumps({
                "consumo": 136+i,
                "data": str(data),
                "dataFimPeriodo": str(dataFimPeriodo),
                "dataInicioPeriodo": str(dataInicioPeriodo),
                "fk_escola": de+1,
                "hidrometro": de+1,
                "valor": 1.2+i
            })

            response_consumo = app.test_client().post(
                'api/v1/cadastros/consumo',
                data=consumo,
                content_type='application/json',
            )
            assert response_consumo.status_code == 200

    return response_consumo



def test_media_consumo_todas_escolas(app, authenticated_app):

    # Retorno para front-end
    with app.app_context():

        # Cadastrar alguns consumos
        test_cadastrar_consumo(app, authenticated_app)

        response = app.test_client().get(
            '/api/v1/dashboard/media-consumo'
        )
        decoded_json = response.get_data().decode('utf-8')
        json_media_consumo = json.loads(decoded_json)
        assert response.status_code == 200

        print("Json Média: ", json_media_consumo)


def test_media_consumo_escola_selecionada(app, authenticated_app):

    # Retorno para front-end
    with app.app_context():

        # Cadastrar alguns consumos
        test_cadastrar_consumo(app, authenticated_app)

        response = app.test_client().get(
            '/api/v1/dashboard/media-consumo-escola/1'
        )
        decoded_json = response.get_data().decode('utf-8')
        json_media_consumo = json.loads(decoded_json)
        assert response.status_code == 200

        print("Json Média: ", json_media_consumo)


def test_media_consumo_percapto(app, authenticated_app):

    with app.app_context():
        test_cadastrar_consumo(app, authenticated_app)

        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        for d in range(1,3):

            populacao = {
                "fk_edificios": d,
                "alunos": fake.random_int(min=1, max=10000),
                "funcionarios": fake.random_int(min=1, max=500),
                "periodo": fake.random_element(elements=('Manhã', 'Tarde', 'Noite', 'Integral')),
                "nivel": fake.random_element(elements=('Médio', 'Superior', 'Fundamental', 'CEU', 'Berçario', 'EJA'))
            }
            json_data = json.dumps(populacao)

            response = app.test_client().post(
                'api/v1/cadastros/populacao',
                data=json_data,
                content_type='application/json',
                headers=headers
            )

            assert response.status_code == 200


        response_retorno_percapto = app.test_client().get(
            '/api/v1/dashboard/media-consumo-pessoas'
        )
        assert response_retorno_percapto.status_code == 200
        decoded_json = response_retorno_percapto.get_data().decode('utf-8')
        json_media_consumo = json.loads(decoded_json)
        print("Validação: ", json_media_consumo)



def test_media_consumo_percapto_escola_selecionada(app, authenticated_app):
    
    with app.app_context():
        test_cadastrar_consumo(app, authenticated_app)

        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        populacao = {
            "fk_edificios": 1,
            "alunos": fake.random_int(min=1, max=10000),
            "funcionarios": fake.random_int(min=1, max=500),
            "periodo": fake.random_element(elements=('Manhã', 'Tarde', 'Noite', 'Integral')),
            "nivel": fake.random_element(elements=('Médio', 'Superior', 'Fundamental', 'CEU', 'Berçario', 'EJA'))
        }
        json_data = json.dumps(populacao)

        response = app.test_client().post(
            'api/v1/cadastros/populacao',
            data=json_data,
            content_type='application/json',
            headers=headers
        )

        assert response.status_code == 200


        response_retorno_percapto = app.test_client().get(
            '/api/v1/dashboard/media-consumo-pessoas-escola/1'
        )
        assert response_retorno_percapto.status_code == 200
        decoded_json = response_retorno_percapto.get_data().decode('utf-8')
        json_media_consumo = json.loads(decoded_json)
        print("Response: ", json_media_consumo)


def test_grafico_media_consumo_mensal_todas_escolas(app, authenticated_app):

    with app.app_context():
        test_cadastrar_consumo(app, authenticated_app)

        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        populacao = {
            "fk_edificios": 1,
            "alunos": fake.random_int(min=1, max=10000),
            "funcionarios": fake.random_int(min=1, max=500),
            "periodo": fake.random_element(elements=('Manhã', 'Tarde', 'Noite', 'Integral')),
            "nivel": fake.random_element(elements=('Médio', 'Superior', 'Fundamental', 'CEU', 'Berçario', 'EJA'))
        }
        json_data = json.dumps(populacao)

        response = app.test_client().post(
            'api/v1/cadastros/populacao',
            data=json_data,
            content_type='application/json',
            headers=headers
        )

        assert response.status_code == 200

        response_consumo = app.test_client().get(
            'api/v1/dashboard/grafico-media-consumo-mensal-todas-escolas'
        )

        assert response_consumo.status_code == 200

        print("Retorno: ", response_consumo.get_data())


def test_grafico_media_consumo_mensal_a_todas_escolas_nivel(app, authenticated_app):
    nivel_1 = fake.random_element(
    elements=('Fundamental', 'Médio', 'Superior', 'Creche', 'Berçario', 'CEU'))
    nivel_2 = fake.random_element(
    elements=('Fundamental', 'Médio', 'Superior', 'Creche', 'Berçario', 'CEU'))
    with app.app_context():
        valor = test_cadastrar_consumo(app, authenticated_app)
        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        for d in range(1, 3):
            populacao = {
                "fk_edificios": d,
                "alunos": fake.random_int(min=1, max=10000),
                "funcionarios": fake.random_int(min=1, max=500),
                "periodo": fake.random_element(elements=('Manhã', 'Tarde', 'Noite', 'Integral')),
                "nivel": nivel_1
            }
            json_data = json.dumps(populacao)

            response = app.test_client().post(
                'api/v1/cadastros/populacao',
                data=json_data,
                content_type='application/json',
                headers=headers
            )


            assert response.status_code == 200

        response_consumo = app.test_client().get(
            f'api/v1/dashboard/grafico-media-consumo-mensal-todas-escolas?niveis={nivel_1},{nivel_2}'
        )

        assert response_consumo.status_code == 200