
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from pytest import fixture
from flask import Response
from models import *
from faker import Faker


from random import randint

fake = Faker()
@fixture
def app():
    #Configura a aplicação para usar o banco de dados de teste

    from src import create_app
    app = create_app({
        'TESTING':True,
        'SQLALCHEMY_DATA_BASE_URI':'sqlite:///test.db'
    })

    with app.app_context():
        #Cria o banco de dados de testes e tabelas
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


@fixture
def new_escolas():
    #criar novas escolas aleatórias
    return Escolas(
        nome=fake.company(),
        cnpj=cnpj(),
        email=fake.email(),
        telefone=fake.phone_number()
        )

# nivel=fake.random_element(elements=('fundamental', 'medio', 'superior', 'creche', 'bercario', 'ceu')),

@fixture
def new_edificios():
    return Edificios(
        fk_escola=1,
        nome_do_edificio=fake.company(),
        numero_edificio=fake.building_number(),
        bairro_edificio=fake.city_suffix(),
        cep_edificio=fake.postcode(),
        cnpj_edificio=fake.cnpj(),
        logradouro_edificio=fake.street_name(),
        complemento_edificio=fake.secondary_address(),
        cidade_edificio=fake.city(),
        estado_edificio=fake.state_abbr(),
        pavimentos_edificio=fake.random_int(min=1, max=10),
        area_total_edificio=fake.pyfloat(min_value=100, max_value=1000, right_digits=2),
        reservatorio=fake.boolean(),
        capacidade_m3_edificio=fake.pyfloat(min_value=100, max_value=1000, right_digits=2),
        agua_de_reuso=fake.boolean(),
        capacidade_reuso_m3_edificio=fake.pyfloat(min_value=100, max_value=1000, right_digits=2),
        principal=fake.boolean()
    ).to_json()


@fixture
def new_area_umida():
    return AreaUmida(
        fk_edificios = 1,
        tipo = fake.random_element(elements=('banheiro', 'cozinha', 'lavanderia')),
        nome_da_area_umida = fake.name(),
        localizacao = fake.address(),
        status = fake.random_element(elements = ('em uso', 'em manutencao'))
    ).to_json()



@fixture
def new_equipamentos():
    return Equipamentos(
        fk_area_umida=1,
        quant_inutilizada=fake.random_int(min=1, max=15),
        quant_problemas=fake.random_int(min=1, max=5),
        quant_total=fake.random_int(min=1, max=6),
        vazamentos=fake.random_int(min=1, max=5),
        tipo = fake.random_element(elements=('Torneira', 'descarga', 'descarga acoplada'))
    ).to_json()

