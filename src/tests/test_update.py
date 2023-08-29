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


def test_update_escola(app, new_escolas, update_escola):
    
    json_data = json.dumps(new_escolas)

    with app.app_context():

        # Defina a configuração 'testing' no objeto current_app
        app.config.update({'testing': True})

        escola = json.dumps(new_escolas)

        insertrescola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=escola,
            content_type='application/json'
        )

        assert insertrescola.status_code == 200

        response_dict = json.loads(insertrescola.get_data())

        json_data = json.dumps(update_escola)
        response = app.test_client().put(
            f"/api/v1/editar/escolas/{response_dict['id']}",  # Correção aqui
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200


def test_update_edificios(app, new_escolas, new_edificios):
    
    json_data = json.dumps(new_escolas)

    with app.app_context():

        
        app.config.update({'testing': True})

        edificio = json.dumps(new_escolas)

        insertescola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=edificio,
            content_type='application/json'
        )

        assert insertescola.status_code == 200

        response_dict = json.loads(insertescola.get_data())

        json_data = json.dumps(new_edificios)
        response = app.test_client().put(
            f"/api/v1/editar/edificios/{response_dict['id']}",  
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200

#testar
def test_update_reservatorio(app, new_escolas, new_reservatorio):

    json_data = json.dumps(new_escolas)

    with app.app_context():
        
        app.config.update({'testing': True})

        escola = json.dumps(new_escolas)
        insertescola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=escola,
            content_type='application/json'
        )

        assert insertescola.status_code == 200

        json_data = json.dumps(new_reservatorio)
        response = app.test_client().post(
            "/api/v1/cadastros/reservatorios",  
            data=json_data,
            content_type='application/json'
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


def test_update_hidrometro(app, new_hidrometro, new_edificios):

    json_data = json.dumps(new_edificios)

    with app.app_context():
        
        app.config.update({'testing': True})

        edificio = json.dumps(new_edificios)
        insertedificio = app.test_client().post(
            'api/v1/cadastros/edificios',
            data=edificio,
            content_type='application/json'
        )

        assert insertedificio.status_code == 200


        json_data = json.dumps(new_hidrometro)
        response = app.test_client().post(
            f"/api/v1/cadastros/hidrometros",  
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200
        response_dict = json.loads(response.get_data())


        json_data = json.dumps(new_hidrometro)
        response = app.test_client().put(
            f"/api/v1/editar/hidrometros/{response_dict['id']}",  
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200


def test_update_populacao(app, new_edificios, new_populacao):

    json_data = json.dumps(new_edificios)

    with app.app_context():

        
        app.config.update({'testing': True})

        edificio = json.dumps(new_edificios)

        insertedificio = app.test_client().post(
            'api/v1/cadastros/edificios',
            data=edificio,
            content_type='application/json'
        )

        assert insertedificio.status_code == 200

        json_data = json.dumps(new_populacao)
        response = app.test_client().post(
            f"/api/v1/cadastros/populacao",  
            data=json_data,
            content_type='application/json'
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


def test_update_area_umida(app, new_edificios, new_area_umida):

    json_data = json.dumps(new_edificios)

    with app.app_context():

        
        app.config.update({'testing': True})

        edificio = json.dumps(new_edificios)

        insertedificio = app.test_client().post(
            'api/v1/cadastros/edificios',
            data=edificio,
            content_type='application/json'
        )

        assert insertedificio.status_code == 200

        json_data = json.dumps(new_area_umida)
        response = app.test_client().post(
            f"/api/v1/cadastros/area-umida",  
            data=json_data,
            content_type='application/json'
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


def test_update_equipamentos(app, new_area_umida, new_equipamentos):

    json_data = json.dumps(new_area_umida)

    with app.app_context():

        
        app.config.update({'testing': True})

        area_umida = json.dumps(new_area_umida)

        insertareaumida = app.test_client().post(
            'api/v1/cadastros/area-umida',
            data=area_umida,
            content_type='application/json'
        )

        assert insertareaumida.status_code == 200

        json_data = json.dumps(new_equipamentos)
        response = app.test_client().post(
            f"/api/v1/cadastros/equipamentos",  
            data=json_data,
            content_type='application/json'
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


def test_update_usuario(app, new_usuario):

    with app.app_context():

        app.config.update({'testing': True})

        usuario = json.dumps(new_usuario)
        insertusuario = app.test_client().post(
            'api/v1/cadastros/usuario',
            data=usuario,
            content_type='application/json'
        )

        assert insertusuario.status_code == 200
        

        json_data = json.dumps(new_usuario)
        response_dict = json.loads(insertusuario.get_data())
        
        response = app.test_client().put(
            f"/api/v1/editar/usuario/{response_dict['data']['id']}",  
            data=json_data,
            content_type='application/json'
        )

        assert response.status_code == 200

# 
# def test_get_tipo_de_eventos():
#     # Use os dados de teste para inserir um tipo de evento na base de dados de teste
#     with app.app_context():
#         db.session.add(tipo_de_evento_test)
#         db.session.commit()

#     # Realize uma requisição GET à rota com o ID do tipo de evento que você acabou de inserir
#     response = client.get('/tipo-de-evento/1')

#     # Verificações
#     assert response.status_code == 200  # O código de status deve ser 200 (OK)
#     data = json.loads(response.data.decode('utf-8'))  # Decodifica o JSON da resposta
#     assert 'tipo_de_evento' in data  # Verifica se a chave 'tipo_de_evento' está presente nos dados
#     assert data['tipo_de_evento']['nome'] == tipo_de_evento_test.nome  # Verifica se o nome do tipo de evento é igual ao esperado

#     # Limpeza após o teste (opcional)
#     with app.app_context():
#         db.session.delete(tipo_de_evento_test)
#         db.session.commit()