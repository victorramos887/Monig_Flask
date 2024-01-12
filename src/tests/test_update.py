import os
import sys
# trunk-ignore(ruff/F401)
from time import sleep
import json
from dotenv import load_dotenv

from test_cadastro_eventos import test_cadastro_evento_ocasional

# Define o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
print(sys.path)
# Caminho para o arquivo .env
ENV_PATH = os.path.join(sys.path[0], '.env')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(ENV_PATH)


def test_update_escola(app, new_escolas, authenticated_app, update_escola):
    
    json_data = json.dumps(new_escolas)

    with app.app_context():

        # Defina a configuração 'testing' no objeto current_app
        app.config.update({'testing': True})

        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        escola = json.dumps(new_escolas)

        insertrescola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=escola,
            content_type='application/json',
            headers=headers
        )

        assert insertrescola.status_code == 200

        response_dict = json.loads(insertrescola.get_data())
        update_escola['nome'] = 'Escola Edição'
        
        json_data = json.dumps(update_escola)
        response = app.test_client().put(
            f"/api/v1/editar/escolas/{response_dict['id']}",  # Correção aqui
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200
        
        
        #VERSIONAMENTO
        
        response_version_escola = app.test_client().get(
            'api/v1/version/escolas-editadas'
        )

        version_update = json.loads(response_version_escola.get_data())
        
        assert response_version_escola.status_code == 200
        assert version_update[0]['nome'] == 'Escola Edição'


def test_update_edificios(app, authenticated_app, new_escolas, new_edificios):
    
    json_data = json.dumps(new_escolas)

    with app.app_context():

        #Autorização
        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        
        app.config.update({'testing': True})

        edificio = json.dumps(new_escolas)

        insertescola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=edificio,
            content_type='application/json',
            headers=headers
        )

        assert insertescola.status_code == 200

        response_dict = json.loads(insertescola.get_data())

        
        new_edificios['nome_do_edificio'] = 'Edificio Edição'
        json_data = json.dumps(new_edificios)
        response = app.test_client().put(
            f"/api/v1/editar/edificios/{response_dict['id']}",  
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200
        
        #VERSIONAMENTO
        response_version_edificio = app.test_client().get(
            'api/v1/version/edificio-editados'
        )

        version_update = json.loads(response_version_edificio.get_data())
        
        assert response_version_edificio.status_code == 200
        # assert version_update[0]['nome'] == 'Edificio Edição'


#testar
def test_update_reservatorio(app, authenticated_app, new_escolas, new_reservatorio):

    json_data = json.dumps(new_escolas)

    with app.app_context():
        
        #Autorização
        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}       

        app.config.update({'testing': True})

        escola = json.dumps(new_escolas)
        insertescola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=escola,
            content_type='application/json',
            headers=headers
        )

        assert insertescola.status_code == 200

        json_data = json.dumps(new_reservatorio)
        response = app.test_client().post(
            "/api/v1/cadastros/reservatorios",  
            data=json_data,
            content_type='application/json',
            headers=headers
        )

        assert response.status_code == 200

        json_data = json.dumps(new_reservatorio)
        response_dict = json.loads(response.get_data())

        print(response_dict)

        response = app.test_client().put(
            f"/api/v1/editar/reservatorios/{response_dict['data']['id']}",  
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200


def test_update_hidrometro(app, authenticated_app, new_hidrometro, new_escolas):

    json_data = json.dumps(new_hidrometro)

    with app.app_context():
        
        #Autorização
        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        app.config.update({'testing': True})

        escola = json.dumps(new_escolas)
        insert_escola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=escola,
            content_type='application/json',
            headers=headers
        )

        assert insert_escola.status_code == 200


        json_data = json.dumps(new_hidrometro)
        response = app.test_client().post(
            # trunk-ignore(git-diff-check/error)
            "api/v1/cadastros/hidrometros",  
            data=json_data,
            content_type='application/json',
            headers=headers
        )

        assert response.status_code == 200
        response_dict = json.loads(response.get_data())


        json_data = json.dumps(new_hidrometro)
        response = app.test_client().put(
            f"api/v1/editar/hidrometros/{response_dict['id']}",  
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200


def test_update_populacao(app, new_escolas, authenticated_app, new_populacao):

    json_data = json.dumps(new_escolas)

    with app.app_context():

        #Autorização
        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        app.config.update({'testing': True})

        escola = json.dumps(new_escolas)
        insert_escola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=escola,
            content_type='application/json',
            headers=headers
        )

        assert insert_escola.status_code == 200

        json_data = json.dumps(new_populacao)
        response = app.test_client().post(
            # trunk-ignore(git-diff-check/error)
            "/api/v1/cadastros/populacao",  
            data=json_data,
            content_type='application/json',
            headers=headers
        )

        assert response.status_code == 200
        response_dict = json.loads(response.get_data())
        

        json_data = json.dumps(new_populacao)
        response = app.test_client().put(
            f"/api/v1/editar/populacao/{response_dict['id']}",  
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200


def test_update_area_umida(app, authenticated_app, new_escolas, new_area_umida):

    json_data = json.dumps(new_escolas)

    with app.app_context():

        #Autorização
        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        app.config.update({'testing': True})

        escola = json.dumps(new_escolas)
        insert_escola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=escola,
            content_type='application/json',
            headers=headers
        )

        assert insert_escola.status_code == 200

        json_data = json.dumps(new_area_umida)
        response = app.test_client().post(
            # trunk-ignore(git-diff-check/error)
            "/api/v1/cadastros/area-umida",  
            data=json_data,
            content_type='application/json',
            headers=headers
        )

        assert response.status_code == 200
        response_dict = json.loads(response.get_data())

        json_data = json.dumps(new_area_umida)
        response = app.test_client().put(
            f"/api/v1/editar/area-umida/{response_dict['id']}",  
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200


def test_update_equipamentos(app, authenticated_app, new_escolas, new_area_umida, new_equipamentos):

    json_data = json.dumps(new_area_umida)

    with app.app_context():

        #Autorização
        headers = {'Authorization': 'Bearer ' + authenticated_app['token']}

        app.config.update({'testing': True})

        escola = json.dumps(new_escolas)
        insert_escola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=escola,
            content_type='application/json',
            headers=headers
        )

        assert insert_escola.status_code == 200

        area_umida = json.dumps(new_area_umida)

        insertareaumida = app.test_client().post(
            'api/v1/cadastros/area-umida',
            data=area_umida,
            content_type='application/json',
            headers=headers
        )

        assert insertareaumida.status_code == 200

        json_data = json.dumps(new_equipamentos)
        response = app.test_client().post(
            # trunk-ignore(git-diff-check/error)
            "/api/v1/cadastros/equipamentos",  
            data=json_data,
            content_type='application/json',
            headers=headers
        )

        assert response.status_code == 200
        response_dict = json.loads(response.get_data())
        

        json_data = json.dumps(new_equipamentos)
        response = app.test_client().put(
            f"/api/v1/editar/equipamentos/{response_dict['id']}",  
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200

#Testar

def test_update_cliente(app, new_cliente):

    with app.app_context():


        app.config.update({'testing': True})

        cliente = json.dumps(new_cliente)
        insertcliente = app.test_client().post(
            'api/v1/cadastros/cliente',
            data=cliente,
            content_type='application/json'
        )

        response_dict = json.loads(insertcliente.get_data())
        print(response_dict)
        assert insertcliente.status_code == 200
        

        json_data = json.dumps(new_cliente)
        response = app.test_client().put(
            f"/api/v1/editar/cliente/{response_dict['data']['id']}",  
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200

       

def test_update_evento_ocasional(app, authenticated_app, new_evento_ocasional, new_tipo_evento_ocasional, new_escolas):
    
    json_data = json.dumps(new_tipo_evento_ocasional)

    with app.app_context():
        
        response = test_cadastro_evento_ocasional(app, authenticated_app, new_evento_ocasional, new_tipo_evento_ocasional, new_escolas)

        print(response.get_data())
        json_data = json.dumps(new_evento_ocasional)
        response = app.test_client().put(
            f"/api/v1/editar/evento/1",  
             data=json_data,
            content_type='application/json'
        )

        print("json_data: ", json_data)
        # assert response.status_code == 200
        

        
       # pytest -v -k "test_update_evento_ocasional"
