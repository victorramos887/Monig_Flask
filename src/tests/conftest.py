from datetime import date, datetime
from random import randint
from faker import Faker
from flask import Response
from pytest import fixture
import sys
import os
import json
from datetime import date
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import create_engine, text
from sqlalchemy.schema import CreateSchema
import psycopg2 as psg
from flask_sqlalchemy import SQLAlchemy


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

fake = Faker()


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)


def pytest_configure(config):
    config.addinivalue_line("filterwarnings", "ignore::DeprecationWarning")
    config.addinivalue_line(
        "filterwarnings", "ignore::sqlalchemy.exc.SAWarning")


@fixture
def app():
    # Configura a aplicação para usar o banco de dados de teste

    from src import create_app
    from src.models import add_opniveis, db
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@localhost:5432/testedb'
    })

    app.json_encoder = CustomJSONEncoder

    try:
        with app.app_context():
            # Cria o banco de dados de testes e tabelas
            if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
                create_database(app.config['SQLALCHEMY_DATABASE_URI'])
                engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

                db.session.execute(text('CREATE SCHEMA IF NOT EXISTS main;'))
                db.session.execute(text('CREATE EXTENSION postgis;'))
                db.session.execute(text('CREATE EXTENSION postgis_topology;'))
                db.session.commit()

                db.create_all()
                add_opniveis()
            yield app

            drop_database(app.config['SQLALCHEMY_DATABASE_URI'])
    except Exception as e:
        raise ValueError(f"{e}")


@fixture
def assert_response():
    def _assert_response(response: Response, status_code: int, content_type: str, content: bytes):
        assert response.status_code == status_code
        assert response.content_type == content_type
        assert content in response.data

    return _assert_response


def cnpj():
    return f'{randint(0, 9)}{randint(0, 9)}.{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}.{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}/0001-{randint(0, 9)}{randint(0, 9)}'


@fixture
def new_escolas():
    # criar novas escolas aleatórias
    return {
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
        'nivel': [fake.random_element(
    elements=('Fundamental', 'Médio', 'Superior', 'Creche', 'Berçario', 'CEU')), fake.random_element(
    elements=('Fundamental', 'Médio', 'Superior', 'Creche', 'Berçario', 'CEU'))],
        'numero': fake.random_int(min=1, max=1000)
    }


@fixture
def update_escola():

    return {
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
        'nivel': ['Fundamental'],
        'numero': fake.random_int(min=1, max=1000)
    }


@fixture
def new_edificios():
    return {
        'fk_escola': 1,
        'nome_do_edificio': fake.company(),
        'numero_edificio': fake.building_number(),
        'bairro_edificio': fake.city_suffix(),
        'cep_edificio': fake.postcode(),
        'cnpj_edificio': cnpj(),
        'logradouro_edificio': fake.street_name(),
        'complemento_edificio': fake.secondary_address(),
        'cidade_edificio': fake.city(),
        'estado_edificio': fake.state_abbr(),
        'pavimentos_edificio': fake.random_int(min=1, max=10),
        'area_total_edificio': fake.pyfloat(min_value=100, max_value=1000, right_digits=2),
        'reservatorio': [],
        'agua_de_reuso': fake.boolean(),
        'capacidade_reuso_m3_edificio': fake.pyfloat(min_value=100, max_value=1000, right_digits=2),
        'principal': fake.boolean()
    }


@fixture
def new_area_umida():
    return {
        'fk_edificios': 1,
        'tipo_area_umida': fake.random_element(elements=('Banheiro', 'Cozinha', 'Lavanderia',
                                                         'Piscina', 'Jardim', 'Areas Umida Comum')),
        'nome_area_umida': fake.name(),
        'localizacao_area_umida': fake.address(),
        'status_area_umida': fake.random_element(elements=('Aberto', 'Fechado')),
        'operacao_area_umida': fake.random_element(elements=('Fechado', 'Em Manutenção',
                                                             'Parcialmente funcionando', 'Aberto'))
    }


@fixture
def new_equipamentos():
    return {
        'fk_area_umida': 1,
        'quantInutil': fake.random_int(min=1, max=15),
        'quantProblema': fake.random_int(min=1, max=5),
        'quantTotal': fake.random_int(min=1, max=6),
        'tipo_equipamento': fake.random_element(
            elements=(
                "Bacia sanitária Caixa de descarga",
                "Bacia sanitária Válvula de descarga",
                "Banheira",
                "Bebedouro",
                "Bidê",
                "Chuveiro ou ducha",
                "Chuveiro elétrico",
                "Lavadora de pratos ou de roupas",
                "Lavatório",
                "Mictório cerâmico Válvula de descarga",
                "Mictório Caixa de descarga, registro de pressão ou válvula de descarga para mictório",
                "Mictório tipo calha",
                "Pia Torneira Gás",
                "Pia Toneira (Elétrica)",
                "Tanque",
                "Torneira de jardim ou lavagem em geral"

            ))
    }


@fixture
def new_populacao():

    return {
        "fk_edificios": 1,
        "alunos": fake.random_int(min=1, max=10000),
        "funcionarios": fake.random_int(min=1, max=500),
        "periodo": fake.random_element(elements=('Manhã', 'Tarde', 'Noite', 'Integral')),
        "nivel": fake.random_element(elements=('Médio', 'Superior', 'Fundamental', 'CEU', 'Berçario', 'EJA'))
    }


@fixture
def new_hidrometro():

    return {
        "fk_edificios": 1,
        "fk_hidrometro": 1,
        "hidrometro": "xxxxxxx"
    }


@fixture
def new_reservatorio():

    return {
        "fk_escola": 1,
        "nome": fake.name()
    }


@fixture
def new_cliente():

    return {
        "nome": fake.name(),
        "email": fake.email(),
        "cnpj":  cnpj(),
        "telefone": "964670934"
    }


@fixture
def new_usuario():

    return {
        "cod_cliente": 1,
        "nome": fake.name(),
        "email": fake.email(),
        "senha":  fake.password(),
        "escola": None,
        "roles": "admin"
    }


@fixture
def new_tipo_evento_ocasional():

    return {
        "fk_cliente": 1,
        "nome_do_evento": fake.name(),
        "dataRecorrente": fake.random_int(min=1, max=31),
        "mesRecorrente": 'Janeiro',
        "periodicidade": fake.random_element(
            elements=(
                "Recorrente",
                "Ocasional"
            )
        ),
        "requerResposta": fake.boolean(),
        "tolerancia": fake.random_int(min=1, max=12),
        "unidade": fake.random_element(
            elements=(
                "Semana",
                "Mês",
                "Dia",
                "Ano"
            )
        ),
        "ehResposta": fake.boolean()
    }


@fixture
def new_tipo_de_vento_vazio():
    return {
        "dataRecorrente": "",
        "ehResposta": False,
        "fk_cliente": 1,
        "mesRecorrente": "",
        "nome_do_evento": "Reunião",
        "periodicidade": "Ocasional",
        "requerResposta": False,
        "tolerancia": "",
        "unidade": ""
    }


@fixture
def new_evento():

    return {
        "fk_tipo": fake.random_int(min=1, max=10),
        "nome": fake.name(),
        "datainicio": None,  # fake.date_object(),
        "datafim": None,  # fake.date_object(),
        "local": fake.random_int(min=1, max=1000),
        "tipo_de_local": fake.random_element(elements=['Escola', 'Edificação', 'Área Umida', 'Reservatório', 'Equipamento', 'Hidrômetro']),
        "observacao": fake.text(),
    }

@fixture
def new_tipo_evento_ocasional():
    return {
        "fk_cliente": 1,
        "nome_do_evento": fake.word(),
        "dataRecorrente": fake.date(),
        "mesRecorrente": fake.random_element(["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]),
        "requerResposta": fake.boolean(),
        "tolerancia": fake.random_number(digits=2),
        "unidade": fake.random_element(['Dias', 'Semanas', 'Meses'])
    }


@fixture
def new_tipo_evento_recorrente():
    return {
        "fk_cliente": 1,
        "nome_do_evento": fake.word(),
        "dataRecorrente": fake.date(),
        "mesRecorrente": fake.random_element(["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]),
        "requerResposta": fake.boolean(),
        "tolerancia": fake.random_number(digits=2),
        "unidade":  fake.random_element(['Dias', 'Semanas', 'Meses'])
    }


@fixture
def new_evento_ocasional():
    return {
        "tipo_de_evento": 1,
        "nome_do_evento": fake.name(),
        "data": "2024-01-01",
        "data_fim": None,
        "local": 1,
        "tipo_de_local": 1,
        "observacoes": fake.text()
    }


@fixture
def new_evento_recorrente():
    dados = {
        "data_inicio": str(fake.date_between_dates(date_start=datetime(2024,1,1), date_end=datetime(2024,2,1))),
        "data_fim": str(fake.date_between_dates(date_start=datetime(2024,2,1), date_end=datetime(2024,2,28))),
        "local": 1,
        "nome_do_evento": fake.name(),
        "observacoes": fake.paragraph(),
        "tipo_de_evento": 1,
        "tipo_de_local": 1
    }
    return dados


#Monitoramento
@fixture
def new_monitoramento(app):
    return {
        "fk_escola":1,
        "hidrometro":"xxxxxxx",
        "leitura":"222,022",
        "hora": "12:56",
        "data": "11/01/2024",
        "escola": "",
    }




# AUTENTICAÇÃO
@fixture
def authenticated_app(app, new_cliente, new_usuario):
    with app.app_context():
        json_data_cliente = json.dumps(new_cliente)

        response_cliente = app.test_client().post(
            '/api/v1/cadastros/cliente',
            data=json_data_cliente,
            content_type='application/json'
        )
        assert response_cliente.status_code == 200

        response_role = app.test_client().post(
            '/api/v1/auth/roles',
            data='{"name":"admin"}',
            content_type="application/json"
        )
        assert response_role.status_code == 200

        json_data_usuario = json.dumps(new_usuario)

        response_usuario = app.test_client().post(
            'api/v1/auth/register',
            data=json_data_usuario,
            content_type='application/json'
        )
        assert response_usuario.status_code == 200

        username = json.loads(json_data_usuario)['email']
        senha = json.loads(json_data_usuario)['senha']
        login_data = {
            "email": str(username),
            "senha": str(senha)
        }

        response_login = app.test_client().post(
            '/api/v1/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        assert response_login.status_code == 200
        token = json.loads(response_login.data)['user']['access']

        yield {
            "token": token
        }