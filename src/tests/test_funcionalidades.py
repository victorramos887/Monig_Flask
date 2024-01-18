import os
import sys
import json

from dotenv import load_dotenv

#Importar testes


# Define o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Caminho para o arquivo .env
ENV_PATH = os.path.join(sys.path[0], '.env')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(ENV_PATH)


def test_cadastrar_uma_escola_e_verificar_se_o_edificio_e_o_principal(app, authenticated_app, new_escolas):
    with app.app_context():

        headers = {"Authorization": 'Bearer ' + authenticated_app['token']}

        json_data = json.dumps(new_escolas)
        response = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_data,
            content_type='application/json',
            headers=headers
        )
        decoded_json = response.get_data().decode('utf-8')# Decodificar a string JSON
        json_obj = json.loads(decoded_json)# Carregar o JSON em um objeto Python
        
        assert response.status_code == 200
        assert json_obj['dada_edificio']['principal'] == True


def test_cadastrar_um_segundo_edificio(app, authenticated_app, new_escolas, new_edificios):
    """Testando o cadstro de edificos e verificando como não sendo o principal"""

    with app.app_context():

        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}
        

        json_data = json.dumps(new_escolas)
        response = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_data,
            content_type='application/json',
            headers=headers
        )
        data = response.get_json()
        assert response.status_code == 200

        json_edificios = json.dumps(new_edificios)
        response_new_edificios = app.test_client().post(
            'api/v1/cadastros/edificios',
            data=json_edificios,
            content_type='application/json',
            headers=headers 
        )
        
        decoded_json = response_new_edificios.get_data().decode('utf-8')# Decodificar a string JSON
        json_obj = json.loads(decoded_json)# Carregar o JSON em um objeto Python

        assert response_new_edificios.status_code == 200
        assert json_obj['data']['principal'] == False
        

def test_edificios_update_principal(app, new_escolas, authenticated_app, new_edificios):
    """Testando se a trocar de edificio principal é realizada."""
    #cadastrar escola


    headers = {'Authorization': 'Bearer ' + authenticated_app['token']}
    json_escola = json.dumps(new_escolas)

    with app.app_context():

        insertNewEscola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escola,
            content_type='application/json',
            headers=headers
        )

        assert insertNewEscola.status_code == 200

        response_escola = json.loads(insertNewEscola.get_data())

    #selecionar edificio cadastrado

        response_edificios_01 = response_escola['dada_edificio']

    # verificar se é o principal
        assert response_edificios_01['principal'] == True

    # cadastrar novo edificio

        json_edificios = json.dumps(new_edificios)

        insertNewEficios = app.test_client().post(
            'api/v1/cadastros/edificios',
            data=json_edificios,
            content_type='application/json',
            headers=headers
        )

        assert insertNewEficios.status_code == 200

        response_edificios_02 = json.loads(insertNewEficios.get_data())
        
    # verificar se novo edificio não está como principal
        assert response_edificios_02['data']['principal'] == False

    # Update: o edificios 2 se tornará o principal

        json_=json.dumps({'principal':True})

        atualizarEdificioPrincipal = app.test_client().put(
            f'api/v1/editar/edificio-principal/{response_edificios_02["data"]["id"]}',
            data=json_,
            content_type='application/json'
        )

        response = json.loads(atualizarEdificioPrincipal.get_data())

        assert atualizarEdificioPrincipal.status_code == 200
        
        selecionarEdificio_02 = app.test_client().get(
            f'api/v1/send_frontend/edificio/{response_edificios_02["data"]["id"]}',
            content_type='application/json'
        )


        #  Verificar se o edificio 2 é o principal
        response_select_edificio_02 = json.loads(selecionarEdificio_02.get_data())
        assert selecionarEdificio_02.status_code == 200
        assert response_select_edificio_02['edificio']['principal'] == True
        
        #Selecionar edificios

        selecionarEdificio_01 = app.test_client().get(
            f'api/v1/send_frontend/edificio/{response_edificios_01["id"]}',
            content_type='application/json'
        )

        response_select_edificio_01 = json.loads(selecionarEdificio_01.get_data())
        assert selecionarEdificio_01.status_code == 200
        assert response_select_edificio_01['edificio']['principal'] == False