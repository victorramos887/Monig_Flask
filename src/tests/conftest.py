from random import randint
from faker import Faker
from flask import Response
from pytest import fixture
import sys
import os
import json
from datetime import date

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

fake = Faker()

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)

@fixture
def app():
    # Configura a aplicação para usar o banco de dados de teste

    from src import create_app
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATA_BASE_URI': 'sqlite:///test.db'
    })


    app.json_encoder = CustomJSONEncoder
    
    with app.app_context():
        # Cria o banco de dados de testes e tabelas
        from src.models import db
        db.create_all()
        yield app

        # Limpando banco de dados de teste após cada execução do teste
        db.session.remove()
        db.drop_all()

@fixture
def assert_response():
    def _assert_response(response: Response, status_code: int, content_type: str, content: bytes):
        assert response.status_code == status_code
        assert response.content_type == content_type
        assert content in response.data

    return _assert_response


def cnpj():
    return f'{randint(0, 9)}{randint(0, 9)}.{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}.{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}/0001-{randint(0, 9)}{randint(0, 9)}'


niveis = fake.random_element(
    elements=('Fundamental', 'Médio', 'Superior', 'Creche', 'Berçario', 'CEU'))


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
        'nivel': [niveis, niveis],
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
        "fk_edificios":1,
        "hidrometro":fake.name()
    }

@fixture
def new_reservatorio():

    return {
        "fk_escola":1,
        "nome":fake.name()
    }

@fixture
def new_cliente():
    
   return {
        "nome": fake.name(),
        "email": fake.email(),
        "cnpj":  cnpj(),
        "telefone": fake.phone_number()
    }

@fixture
def new_usuario():
    
   return {
        "cod_cliente": 1,
        "nome": fake.name(),
        "email": fake.email(),
        "senha":  fake.password(),
      
    }

from datetime import date, datetime


@fixture
def new_tipo_evento():

   return {
        "fk_cliente":1,
        "nome_do_tipo_evento":fake.name(),
        "periodicidade":fake.random_int(min=1, max=7),
        "dataSazonal":datetime(2023, 8, 24, 10, 0, 0) ,#datetime.strptime("2023-02-22 10:10:00", '%Y-%m-%dT%H:%M:%S'),
        "requerResposta":fake.boolean(),
        "tolerancia":fake.random_int(min=1, max=7),
        "unidade":fake.random_element(
            elements=(
                "Semana",
                "Mês",
                "Dia",
                "Ano"
            )
        ),
        "qual_tipo_evento":None,
        "ehResposta":None
    }

@fixture
def new_evento():
    
    return {
        "fk_tipo":fake.random_int(min=1, max=10),
        "nome":fake.name(),
        "datainicio":fake.date_object(),
        "datefim":fake.data_object(),
        "prioridade":fake.random_element(
            element=(
                "Alta",
                "Baixa"
            )
        ),
        "local":fake.random_int(min=1, max=1000),
        "tipo_de_local":fake.random_int(min=1, max=10),
        "observacao":fake.text(),
        "cod_usuarios":fake.random_int(min=1, max=10)
    }