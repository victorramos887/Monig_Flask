import os
import sys
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


def test_delete_escola(app, new_escolas):
    
    json_escola = jsom.dumps(new_escolas)
    
    with app.app_context():
        
        insertescola = app.test_client().post(
            'api/v1/cadastro/escolas',
            data=json_escola,
            content_type='application/json'
        )
        
        assert insertescola.status_code == 200