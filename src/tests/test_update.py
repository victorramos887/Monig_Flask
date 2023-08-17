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


# def test_update_edificios(app, new_edificios):

#     json_data = json.dumps(new_edificios)