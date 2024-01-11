import os
import sys
from time import sleep
import json

from dotenv import load_dotenv

from datetime import datetime, date


# Define o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))



print(sys.path)
# Caminho para o arquivo .env
ENV_PATH = os.path.join(sys.path[0], '.env')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(ENV_PATH)


def date_encoder(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()  # Converte para string no formato ISO 8601
    raise TypeError("Object of type %s is not JSON serializable" % type(obj))


def test_cadastro_escola(app, authenticated_app,new_escolas):
    
    """
        Testa o cadastro de escola.

        Cenário:
        - Um usuário autenticado com token válido.
        - Cadastro de um escola associada ao cliente.

        Passos:
        1. Autentica o usuário e obtém um token válido.
        2. Cadastra uma escola usando o token.
        3. Verifica se o cadastro da escola foi bem-sucedido.
        4. Verifica se o cadastro da escola foi bem-sucedido.

        Resultado Esperado:
        - O Cadastros da escola devem ser bem-sucedidos.
        - Os códigos de status das respostas devem ser 200.

        Observações:
        - O cadastro do cliente, da role e do usuário é feito pela fixture `authenticated_app`
        - Este teste assume que a API permite o cadastro de escola associados ao cliente.
        - Os dados de `new_escolas` e `authenticated_app` devem ser fornecidos como parâmetros.
    """


    headers = {'Authorization': 'Bearer ' + authenticated_app['token']}
    # Converte o objeto para JSON
    json_data = json.dumps(new_escolas)
    

    response = app.test_client().post(
        'api/v1/cadastros/escolas',
        data=json_data,
        content_type='application/json',
        headers=headers
    )
    
    data = response.get_json()
    assert response.status_code == 200
    


def test_cadastro_edificios(app, authenticated_app, new_escolas, new_edificios):
    """
        Testa o cadastro de edifícios.

        Cenário:
        - Um usuário autenticado com token válido.
        - Criação de uma escola como pré-requisito.
        - Cadastro de um edifício associado à escola.

        Passos:
        1. Autentica o usuário e obtém um token válido.
        2. Cadastra uma escola usando o token.
        3. Verifica se o cadastro da escola foi bem-sucedido.
        4. Prepara os dados do edifício, associando-o à escola cadastrada.
        5. Cadastra o edifício com um token de autenticação.
        6. Verifica se o cadastro do edifício foi bem-sucedido.

        Resultado Esperado:
        - Ambos os cadastros (escola e edifício) devem ser bem-sucedidos.
        - Os códigos de status das respostas devem ser 200.

        Observações:
        - O cadastro do cliente, da role e do usuário é feito pela fixture `authenticated_app`
        - Este teste assume que a API permite o cadastro de edifícios associados a escolas.
        - Os dados de `authenticated_app`, `new_escolas` e `new_edificios` devem ser fornecidos como parâmetros.
    """
    # Execute a lógica do teste
    with app.app_context():

        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}
        
        #Cadastro escola
        test_cadastro_escola(app, authenticated_app, new_escolas)

        #Cadastrar Edificio

        json_data = json.dumps(new_edificios)
        response = app.test_client().post(
            'api/v1/cadastros/edificios',
            data=json_data,
            content_type='application/json',
            headers=headers
        )
        
        # Verifique o código de status da resposta
        assert response.status_code == 200
        

def test_cadastro_area_umida(app, authenticated_app, new_escolas, new_edificios, new_area_umida):

    """
        Testa o cadastro de area úmida.

        Cenário:
        - Um usuário autenticado com token válido.
        - Criação de uma escola como pré-requisito.
        - Criação de um edifício como pré-requisito.
        - Cadastro de um edifício associado à escola.
        - Cadastro da área úmida associado ao edifício.

        Passos:
        1. Autentica o usuário e obtém um token válido.
        2. Cadastra uma escola usando o token.
        3. Verifica se o cadastro da escola foi bem-sucedido.
        4. Prepara os dados do edifício, associando-o à escola cadastrada.
        5. Cadastra o edifício usando o token de autenticação.
        6. Verifica se o cadastro do edifício foi bem-sucedido.
        7. Cadastra a área úmida usando o token de autenticação.
        8. Verifica se o cadastro da área úmida foi bem-sucedido.

        Resultado Esperado:
        - Todos os resultados devem ser bem-sucedido.
        - Os códigos de status das respostas devem ser 200.

        Observações:
        - O cadastro do cliente, da role e do usuário é feito pela fixture `authenticated_app`
        - Este teste assume que a API permite o cadastro de edifícios associados a escolas.
        - Este teste assume que a API permite o cadastro de área úmida associados ao edifícios.
        - Os dados de `authenticated_app`, `new_escolas`,  `new_edificios` e `new_area_umida` devem ser fornecidos como parâmetros.
    """


    with app.app_context():

        #Cadsatros necessários
        test_cadastro_edificios(app, authenticated_app, new_escolas, new_edificios)
        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}
        
        json_data = json.dumps(new_area_umida)

        response = app.test_client().post(
            'api/v1/cadastros/area-umida',
            data=json_data,
            content_type='application/json',
            headers=headers
        )

        response_dict = json.loads(response.get_data())
        print(response_dict)

        assert response.status_code == 200


def test_cadastro_equipamento(app, authenticated_app, new_escolas, new_edificios, new_area_umida, new_equipamentos):

    """
        Testa o cadastro de equipamentos.

        Cenário:
        - Um usuário autenticado com token válido.
        - Criação de uma escola como pré-requisito.
        - Criação de um edifício como pré-requisito.
        - Criação de uma área úmida como pré-requsito.
        - Cadastro de um edifício associado à escola.
        - Cadastro da área úmida associado ao edifício.
        - Cadastro de um equipameto associado a área úmida

        Passos:
        1. Autentica o usuário e obtém um token válido.
        2. Cadastra uma escola usando o token.
        3. Verifica se o cadastro da escola foi bem-sucedido.
        4. Prepara os dados do edifício, associando-o à escola cadastrada.
        5. Cadastra o edifício usando o token de autenticação.
        6. Verifica se o cadastro do edifício foi bem-sucedido.
        7. Cadastra a área úmida usando o token de autenticação.
        8. Verifica se o cadastro da área úmida foi bem-sucedido.
        9. Cadastra o equipamento usando o token de autenticação.
        10. Verifica se o cadastro do equipamento foi bem-sucedido.

        Resultado Esperado:
        - Todos os resultados devem ser bem-sucedido.
        - Os códigos de status das respostas devem ser 200.

        Observações:
        - O cadastro do cliente, da role e do usuário é feito pela fixture `authenticated_app`
        - Este teste assume que a API permite o cadastro de edifícios associados a escolas.
        - Este teste assume que a API permite o cadastro de área úmida associados ao edifícios.
        - Este teste assume que a API permite o cadastro de equipamento associados ao área úmida.
        - Os dados de `authenticated_app`, `new_escolas`,  `new_edificios`, `new_area_umida`, `new_equipamentos` devem ser fornecidos como parâmetros.
    """


    with app.app_context():

        #Pré requsito, teste de cadastro de área umida
        test_cadastro_area_umida(app, authenticated_app, new_escolas, new_edificios, new_area_umida)


        #Cadstro de equipamento

        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}
        
        #Cadastrando 10 equipamentos
        for d in range(0, 10):
            json_data = json.dumps(new_equipamentos)

            response = app.test_client().post(
                'api/v1/cadastros/equipamentos',
                data=json_data,
                content_type='application/json',
                headers=headers
            )

            assert response.status_code == 200



def test_cadastro_populacao(app, authenticated_app, new_escolas, new_edificios, new_populacao):


    """
        Testa o cadastro de equipamentos.

        Cenário:
        - Um usuário autenticado com token válido.
        - Criação de uma escola como pré-requisito.
        - Criação de um edifício como pré-requisito.
        - Criação de uma população associada ao edifício
        - Cadastro de um edifício associado à escola.
        - Cadastro de um população associado ao edifício.
        
        Passos:
        1. Autentica o usuário e obtém um token válido.
        2. Cadastra uma escola usando o token.
        3. Verifica se o cadastro da escola foi bem-sucedido.
        4. Prepara os dados do edifício, associando-o à escola cadastrada.
        5. Cadastra o edifício usando o token de autenticação.
        6. Verifica se o cadastro do edifício foi bem-sucedido.
        7. Cadastra a população usando o token de autenticação.
        8. Verifica se o cadastro da população foi bem-sucedido.

        Resultado Esperado:
        - Todos os resultados devem ser bem-sucedido.
        - Os códigos de status das respostas devem ser 200.

        Observações:
        - O cadastro do cliente, da role e do usuário é feito pela fixture `authenticated_app`
        - Este teste assume que a API permite o cadastro de edifícios associados a escolas.
        - Este teste assume que a API permite o cadastro de população associados ao edifícios.
        - Os dados de `authenticated_app`, `new_escolas`,  `new_edificios` e `new_populacao` devem ser fornecidos como parâmetros.
    """

    with app.app_context():

        #Cadsatros necessários
        test_cadastro_edificios(app, authenticated_app, new_escolas, new_edificios)
        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        json_data = json.dumps(new_populacao)

        response = app.test_client().post(
            'api/v1/cadastros/populacao',
            data=json_data,
            content_type='application/json',
            headers=headers
        )

        assert response.status_code == 200


def test_cadastro_hidrometro(app, authenticated_app, new_escolas, new_edificios, new_hidrometro):

    """
        Testa o cadastro de equipamentos.

        Cenário:
        - Um usuário autenticado com token válido.
        - Criação de uma escola como pré-requisito.
        - Criação de um edifício como pré-requisito.
        - Criação de um hidrometro associada ao edifício
        - Cadastro de um edifício associado à escola.
        - Cadastro de um hidrometro associado ao edifício.
        
        Passos:
        1. Autentica o usuário e obtém um token válido.
        2. Cadastra uma escola usando o token.
        3. Verifica se o cadastro da escola foi bem-sucedido.
        4. Prepara os dados do edifício, associando-o à escola cadastrada.
        5. Cadastra o edifício usando o token de autenticação.
        6. Verifica se o cadastro do edifício foi bem-sucedido.
        7. Cadastra o hidrometro usando o token de autenticação.
        8. Verifica se o cadastro do hidrometro foi bem-sucedido.

        Resultado Esperado:
        - Todos os resultados devem ser bem-sucedido.
        - Os códigos de status das respostas devem ser 200.

        Observações:
        - O cadastro do cliente, da role e do usuário é feito pela fixture `authenticated_app`
        - Este teste assume que a API permite o cadastro de edifícios associados a escolas.
        - Este teste assume que a API permite o cadastro de hidrometro associados ao edifícios.
        - Os dados de `authenticated_app`, `new_escolas`,  `new_edificios` e `new_hidrometro` devem ser fornecidos como parâmetros.
    """

    with app.app_context():
        
        #Cadsatros necessários
        test_cadastro_edificios(app, authenticated_app, new_escolas, new_edificios)
        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        json_data = json.dumps(new_hidrometro)

        response = app.test_client().post(
            'api/v1/cadastros/hidrometros',
            data=json_data,
            content_type='application/json',
            headers=headers
        )
        print(response.get_data())
        assert response.status_code == 200


def test_cadastro_reservatorio(app, authenticated_app, new_escolas, new_reservatorio):

    """
        Testa o cadastro de reservatórios.

        Cenário:
        - Um usuário autenticado com token válido.
        - Criação de uma escola como pré-requisito.
        - Cadastro de um reservatório associado à escola.

        Passos:
        1. Autentica o usuário e obtém um token válido.
        2. Cadastra uma escola usando o token.
        3. Verifica se o cadastro da escola foi bem-sucedido.
        4. Prepara os dados do reservatório, associando-o à escola cadastrada.
        5. Cadastra o reservatório com um token de autenticação.
        6. Verifica se o cadastro do reservatório foi bem-sucedido.

        Resultado Esperado:
        - Ambos os cadastros (escola e reservatório) devem ser bem-sucedidos.
        - Os códigos de status das respostas devem ser 200.

        Observações:
        - O cadastro do cliente, da role e do usuário é feito pela fixture `authenticated_app`
        - Este teste assume que a API permite o cadastro de reservatórios associados a escolas.
        - Os dados de `authenticated_app`, `new_escolas` e `new_reservatorio` devem ser fornecidos como parâmetros.
    """

    with app.app_context():
        
        #Cadastros necessários


        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}
        
        #Cadastro escola
        test_cadastro_escola(app, authenticated_app, new_escolas)

        json_data = json.dumps(new_reservatorio)

        response = app.test_client().post(
            'api/v1/cadastros/reservatorios',
            data=json_data,
            content_type='application/json',
            headers=headers
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
        

def test_cadastro_usuario(app, new_cliente, new_usuario):

    with app.app_context():
        
        #Cadastro de cliente
        test_cadastro_cliente(app, new_cliente)

        #Cadastrar role
        response_role = app.test_client().post(
                '/api/v1/auth/roles',
                data='{"name":"admin"}',
                content_type="application/json"
            )
        assert response_role.status_code == 200

        #Cadastro de usuários
        json_data = json.dumps(new_usuario)

        response = app.test_client().post(
            '/api/v1/auth/register',
            data=json_data,
            content_type='application/json'
        )
        print("Response: ", response.get_data())
        assert response.status_code == 200



def test_cadastro_tipo_eventos_ocasional(app, authenticated_app, new_escolas, new_tipo_evento_ocasional):
    with app.app_context():
        
        test_cadastro_escola(app, authenticated_app, new_escolas)

        json_data = json.dumps(new_tipo_evento_ocasional)       
        
        response = app.test_client().post(
            '/api/v1/cadastro-evento/tipo-de-evento-ocasional',
            data=json_data,
            content_type='application/json'
        )
        print(response.get_data())
        assert response.status_code == 200

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

        print("Response: ",response.get_data()) 
        assert response.status_code == 200


def dtest_cadastro_de_tipo_de_evento_vazio(app, new_tipo_de_vento_vazio):

    with app.app_context():

        json_data = json.dumps(new_tipo_de_vento_vazio)

        response = app.test_client().post(
        "/api/v1/cadastro-evento/tipo-evento",
        data=json_data,
        content_type='application/json'
        )
    
    assert response.status_code == 200


def test_cadastro_eventos(app, new_evento):


    with app.app_context():


        # new_evento['datainicio'] = new_evento['datainicio'].strftime("%Y-%d-%m")
        # new_evento['datafim'] = new_evento['datafim'].strftime("%Y-%d-%m")
        
        # new_evento['datainicio'] = datetime.datetime.strptime(new_evento['datainicio'], '%Y-%m-%d %H:%M:%S')
        # new_evento['datafim'] = datetime.datetime.strptime(new_evento['datafim'], '%Y-%m-%d %H:%M:%S')
        # new_evento['datainicio'] = '2023-02-23'
        # new_evento['datafim'] = '2023-02-28'

        
        # new_evento['datainicio'] = new_evento['datainicio'].strftime("%Y-%m-%d %H:%M:%S")
        # new_evento['datafim'] = new_evento['datafim'].strftime("%Y-%m-%d %H:%M:%S")


        #json_data = json.dumps(new_evento, indent=4, ensure_ascii=True, default=None)
        
        #print(json.dumps(new_evento))
        
        
        response = app.test_client().post(
            'api/v1/cadastro-evento/eventos',
            data=json.dumps(new_evento),
            content_type='application/json'
        )
        print(response.get_data())
        assert response.status_code == 200