import os
import sys
from time import sleep
import json
from dotenv import load_dotenv


# Define o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))
print(sys.path)
# Caminho para o arquivo .env
ENV_PATH = os.path.join(sys.path[0], '.env')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(ENV_PATH)


def test_deleta_escola(app, new_escolas):
    
    """ Deletando apenas a escola"""
    
    with app.app_context():
        
        # -------------------------------------------------------
                                # INSERT ESCOLA
        # -------------------------------------------------------
        
        json_escola = json.dumps(new_escolas)
        
        response_escola = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escola,
            content_type='application/json'
        )
        
        
        dict_escola_insert = json.loads(response_escola.get_data())
        assert response_escola.status_code == 200
        
        # -------------------------------------------------------
        
        
        # -------------------------------------------------------
                            #VERIFICANDO ESCOLA
        # -------------------------------------------------------
        
        send_escola = app.test_client().get(
            f"api/v1/send_frontend/escolas/{dict_escola_insert['id']}",
        )
               
        assert send_escola.status_code == 200
        
        
        #--------------------------------------------------------
                            #DELETAR ESCOLA
        #--------------------------------------------------------
        deletar_escola = app.test_client().put(
            f'api/v1/remover/escolas/{dict_escola_insert["id"]}'
        )
        
        assert deletar_escola.status_code == 200
        
        # verificando tabela histórico
        version_delete = app.test_client().get(
            f'api/v1/version/escola-deletada/{dict_escola_insert["id"]}'
        )
        
        print(dict_escola_insert["id"])
        print(json.loads(version_delete.get_data()))
        
        assert version_delete.status_code == 200
        

def test_deleta_escola_completo(app, new_escolas, new_edificios, new_area_umida, new_equipamentos, new_populacao, new_hidrometro):
    
    """Deletar escola completo. Adicionar escola, edificio, area umida, equipamentos, populacao, hidrometros."""
    
    
    with app.app_context():
               
        # -----------------------------------------------------------
                                    #INSERT
        # -----------------------------------------------------------
        
        #ESCOLA
        json_escolas = json.dumps(new_escolas)
        
        response_escolas_insert = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escolas,
            content_type='application/json'
        )
        
        escolas_dict = json.loads(response_escolas_insert.get_data())
        
        assert response_escolas_insert.status_code == 200
        
        
        
        #EDIFICIOS
        
        json_edificios = json.dumps(new_edificios)
        
        response_edificios_insert = app.test_client().post(
            'api/v1/cadastros/edificios',
            data=json_edificios,
            content_type='application/json'
        )
        
        edificios_dict = json.loads(response_edificios_insert.get_data())
        print('id', edificios_dict['id'])
        
        assert response_edificios_insert.status_code == 200
        
        #AREA UMIDA
        
        json_area_umida = json.dumps(new_area_umida)
        
        response_area_umida_insert = app.test_client().post(
            'api/v1/cadastros/area-umida',
            data=json_area_umida,
            content_type='application/json'
        )
        
        area_umida_dict = json.loads(response_area_umida_insert.get_data())
       
        assert response_area_umida_insert.status_code == 200
        
        #EQUIPAMENTOS
        for i in range(0,5):
            
            json_equipamentos = json.dumps(new_equipamentos)
            
            response_equipamentos = app.test_client().post(
                'api/v1/cadastros/equipamentos',
                data=json_equipamentos,
                content_type='application/json'
            )
            
            assert response_equipamentos.status_code == 200
        
        
        # POPULAÇÃO
        for i in range(0, 5):
            
            json_populacao = json.dumps(new_populacao)
            
            response_populacao_insert = app.test_client().post(
                'api/v1/cadastros/populacao',
                data=json_populacao,
                content_type='application/json'
            )
            
            assert response_populacao_insert.status_code == 200
        
        # HIDROMETRO
        
        for i in range(0, 5):
            
            json_hidrometro = json.dumps(new_hidrometro)
            
            response_hidrometro_insert = app.test_client().post(
                'api/v1/cadastros/hidrometros',
                data=json_hidrometro,
                content_type='application/json'
            )
            
            assert response_hidrometro_insert.status_code == 200
            
        #-----------------------------------------------------------
    
        # -----------------------------------------------------------
                                #DELETANDO
        # -----------------------------------------------------------
        #ESCOLA
        response_escola_remove = app.test_client().put(
            'api/v1/remover/escolas/1'
        )
        
        assert response_escola_remove.status_code == 200
        #-----------------------------------------------------------
        
        # -----------------------------------------------------------
                                #VERSION
        # -----------------------------------------------------------
        
        #ESCOLA
        response_escola_version = app.test_client().get(
            'api/v1/version/escola-deletada/1'
        )
        
        assert response_escola_version.status_code == 200
        
        #EDIFICIOS
        
        response_edificio_version = app.test_client().get(
            f'api/v1/version/edificio-deletado/1'
        )
        print(response_edificio_version)
        
        assert response_edificio_version.status_code == 200
        
        response_edificio_version2 = app.test_client().get(
            'api/v1/version/edificio-deletado/2'
        )
        
        assert response_edificio_version2.status_code == 200
        
        #AREA UMIDA
        
        response_area_umida_version = app.test_client().get(
            f"api/v1/version/area-umida-deletada/{area_umida_dict['id']}"
        )
        
        assert response_area_umida_version.status_code == 200
        
        
        for i in range(0, 5):
            
            response_equipamentos_version = app.test_client().get(
                f'api/v1/version/equipamento-deletado/{i+1}'
            )
            
            assert response_equipamentos_version.status_code == 200
            
        for i in range(0, 5):
            
            response_populacao_version = app.test_client().get(
                f'api/v1/version/populacao-deletada/{i+1}'
            )
            
            assert response_populacao_version.status_code == 200
            
        for i in range(0, 5):
            
            response_hidrometro_version = app.test_client().get(
                f'api/v1/version/hidrometro-deletada/{i+1}'
            )
            
            assert response_hidrometro_version.status_code == 200
        # -----------------------------------------------------------
    #------------------------------------------------------------


def test_deleta_edificio(app, new_escolas, new_edificios, new_area_umida, new_equipamentos, new_populacao, new_hidrometro):
    """Deletando edificio"""
    with app.app_context():

        # -----------------------------------------------------------
                                    #INSERT
        # -----------------------------------------------------------
        
        #ESCOLA
        json_escolas = json.dumps(new_escolas)
        
        response_escolas_insert = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escolas,
            content_type='application/json'
        )
        
        escolas_dict = json.loads(response_escolas_insert.get_data())
        
        assert response_escolas_insert.status_code == 200
        
        
        
        #EDIFICIOS
        
        json_edificios = json.dumps(new_edificios)
        
        response_edificios_insert = app.test_client().post(
            'api/v1/cadastros/edificios',
            data=json_edificios,
            content_type='application/json'
        )
        
        edificios_dict = json.loads(response_edificios_insert.get_data())
        print('id', edificios_dict['id'])
        
        assert response_edificios_insert.status_code == 200
        
        #AREA UMIDA
        
        json_area_umida = json.dumps(new_area_umida)
        
        response_area_umida_insert = app.test_client().post(
            'api/v1/cadastros/area-umida',
            data=json_area_umida,
            content_type='application/json'
        )
        
        area_umida_dict = json.loads(response_area_umida_insert.get_data())
       
        assert response_area_umida_insert.status_code == 200
        
        #EQUIPAMENTOS
        for i in range(0,5):
            
            json_equipamentos = json.dumps(new_equipamentos)
            
            response_equipamentos = app.test_client().post(
                'api/v1/cadastros/equipamentos',
                data=json_equipamentos,
                content_type='application/json'
            )
            
            assert response_equipamentos.status_code == 200
        
        
        # POPULAÇÃO
        for i in range(0, 5):
            
            json_populacao = json.dumps(new_populacao)
            
            response_populacao_insert = app.test_client().post(
                'api/v1/cadastros/populacao',
                data=json_populacao,
                content_type='application/json'
            )
            
            assert response_populacao_insert.status_code == 200
        
        # HIDROMETRO
        
        for i in range(0, 5):
            
            json_hidrometro = json.dumps(new_hidrometro)
            
            response_hidrometro_insert = app.test_client().post(
                'api/v1/cadastros/hidrometros',
                data=json_hidrometro,
                content_type='application/json'
            )
            
            assert response_hidrometro_insert.status_code == 200
            
        #-----------------------------------------------------------
    
        # -----------------------------------------------------------
                                #DELETANDO
        # -----------------------------------------------------------
        #ESCOLA
        response_deletar_edificio = app.test_client().put(
            'api/v1/remover/edificios/1'
        )
        
        assert response_deletar_edificio.status_code == 200
        #-----------------------------------------------------------
        
        # -----------------------------------------------------------
                                #VERSION
        # -----------------------------------------------------------        
       
        #EDIFICIOS
        
        response_edificio_version = app.test_client().get(
            f'api/v1/version/edificio-deletado/1'
        )
        print(response_edificio_version)
        
        assert response_edificio_version.status_code == 200
        
        response_edificio_version2 = app.test_client().get(
            'api/v1/version/edificio-deletado/2'
        )
        
        assert response_edificio_version2.status_code == 400
        
        #AREA UMIDA
        
        response_area_umida_version = app.test_client().get(
            f"api/v1/version/area-umida-deletada/{area_umida_dict['id']}"
        )
        
        assert response_area_umida_version.status_code == 200
        
        
        for i in range(0, 5):
            
            response_equipamentos_version = app.test_client().get(
                f'api/v1/version/equipamento-deletado/{i+1}'
            )
            
            assert response_equipamentos_version.status_code == 200
            
        for i in range(0, 5):
            
            response_populacao_version = app.test_client().get(
                f'api/v1/version/populacao-deletada/{i+1}'
            )
            
            assert response_populacao_version.status_code == 200
            
        for i in range(0, 5):
            
            response_hidrometro_version = app.test_client().get(
                f'api/v1/version/hidrometro-deletada/{i+1}'
            )
            
            assert response_hidrometro_version.status_code == 200
        # -----------------------------------------------------------
    #------------------------------------------------------------
    

def test_deletar_hidrometro(app, new_escolas, new_hidrometro):
    
    with app.app_context():
        
        
        json_escolas = json.dumps(new_escolas)
        
        response_escolas_insert = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escolas,
            content_type='application/json'
        )
        
        escolas_dict = json.loads(response_escolas_insert.get_data())
        
        assert response_escolas_insert.status_code == 200
        
        
        #RECUPERAR EDIFICIO
        response_send_edificio = app.test_client().get(
            f'api/v1/send_frontend/edificio/1'
        )
        
        assert response_send_edificio.status_code == 200
        
        
        json_hidrometro = json.dumps(new_hidrometro)
        
        response_hidrometro = app.test_client().post(
            'api/v1/cadastros/hidrometros',
            data=json_hidrometro,
            content_type='application/json'
        )
        
        assert response_hidrometro.status_code == 200
        
        
        #DELETAR HIDROMETRO
        
        response_deletar_hidrometro = app.test_client().put(
            'api/v1/remover/hidrometros/1'
        )
        
        assert response_deletar_hidrometro.status_code == 200
        


def test_deletar_populacao(app, new_escolas, new_populacao):
    
    with app.app_context():
        
        
        json_escolas = json.dumps(new_escolas)
        
        response_escolas_insert = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escolas,
            content_type='application/json'
        )
        
        escolas_dict = json.loads(response_escolas_insert.get_data())
        
        assert response_escolas_insert.status_code == 200
        
        
        #RECUPERAR EDIFICIO
        response_send_edificio = app.test_client().get(
            f'api/v1/send_frontend/edificio/1'
        )
        
        assert response_send_edificio.status_code == 200
        
        
        json_populacao = json.dumps(new_populacao)
        
        response_populacao = app.test_client().post(
            'api/v1/cadastros/populacao',
            data=json_populacao,
            content_type='application/json'
        )
        
        assert response_populacao.status_code == 200
        
        
        #DELETAR HIDROMETRO
        
        response_deletar_populacao = app.test_client().put(
            'api/v1/remover/populacao/1'
        )
        
        assert response_deletar_populacao.status_code == 200
        
def test_deletar_area_umida(app, new_escolas, new_area_umida, new_equipamentos):
    
    with app.app_context():
        
        
        json_escolas = json.dumps(new_escolas)
        
        response_escolas_insert = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escolas,
            content_type='application/json'
        )
        
        escolas_dict = json.loads(response_escolas_insert.get_data())
        
        assert response_escolas_insert.status_code == 200
        
        
        #RECUPERAR EDIFICIO
        response_send_edificio = app.test_client().get(
            f'api/v1/send_frontend/edificio/1'
        )
        
        assert response_send_edificio.status_code == 200
        
        
        json_area_umida = json.dumps(new_area_umida)
        
        response_area_umida = app.test_client().post(
            'api/v1/cadastros/area-umida',
            data=json_area_umida,
            content_type='application/json'
        )

        assert response_area_umida.status_code == 200
        
        for i in range(0, 5):
            
            json_equipamento = json.dumps(new_equipamentos)
            
            response_equipamento_insert = app.test_client().post(
                'api/v1/cadastros/equipamentos',
                data=json_equipamento,
                content_type='application/json'
            )
            
            assert response_equipamento_insert.status_code == 200
        
        #DELETAR AREA UMIDA
        
        response_deletar_populacao = app.test_client().put(
            'api/v1/remover/area-umida/1'
        )
        
        assert response_deletar_populacao.status_code == 200
        
        #VERSÃO
        
        response_area_umida_version = app.test_client().get(
            f"api/v1/version/area-umida-deletada/1"
        )
        
        assert response_area_umida_version.status_code == 200
        
        for i in range(0, 5):
            response_equipamentos_version = app.test_client().get(
                f"api/v1/version/equipamento-deletado/{i+1}"
            )
        
            assert response_equipamentos_version.status_code == 200



def test_deletar_equipamentos(app, new_escolas, new_area_umida, new_equipamentos):
    
    with app.app_context():
        
        
        json_escolas = json.dumps(new_escolas)
        
        response_escolas_insert = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escolas,
            content_type='application/json'
        )
        
        escolas_dict = json.loads(response_escolas_insert.get_data())
        
        assert response_escolas_insert.status_code == 200
        
        
        #RECUPERAR EDIFICIO
        response_send_edificio = app.test_client().get(
            f'api/v1/send_frontend/edificio/1'
        )
        
        assert response_send_edificio.status_code == 200
        
        
        json_area_umida = json.dumps(new_area_umida)
        
        response_area_umida = app.test_client().post(
            'api/v1/cadastros/area-umida',
            data=json_area_umida,
            content_type='application/json'
        )

        assert response_area_umida.status_code == 200
        
            
        json_equipamento = json.dumps(new_equipamentos)
        
        response_equipamento_insert = app.test_client().post(
            'api/v1/cadastros/equipamentos',
            data=json_equipamento,
            content_type='application/json'
        )
        
        assert response_equipamento_insert.status_code == 200
        
        #DELETAR EQUIPAMENTO
        
        response_deletar_equipamento = app.test_client().put(
            'api/v1/remover/equipamentos/1'
        )
        
        assert response_deletar_equipamento.status_code == 200
        
        #VERSÃO
        
        response_equipamentos_version = app.test_client().get(
            f"api/v1/version/equipamento-deletado/1"
        )
    
        assert response_equipamentos_version.status_code == 200
    


def test_deletar_reservatorio(app, new_escolas, new_reservatorio):
    
    with app.app_context():
        
        
        json_escolas = json.dumps(new_escolas)
        
        response_escolas_insert = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escolas,
            content_type='application/json'
        )
        
        escolas_dict = json.loads(response_escolas_insert.get_data())
        
        assert response_escolas_insert.status_code == 200
        
        json_reservatorio = json.dumps(new_reservatorio)
        
        response_reservatorio_insert = app.test_client().post(
            'api/v1/cadastros/reservatorios',
            data=json_reservatorio,
            content_type='application/json'
        )
        
        assert response_reservatorio_insert.status_code == 200
        
        #DELETAR RESERVATÓRIO
        
        response_deletar_reservaotorio = app.test_client().put(
            'api/v1/remover/reservatorios/1'
        )
        
        assert response_deletar_reservaotorio.status_code == 200


def test_deletar_monitoramento(app, new_escolas, new_hidrometro):

    with app.app_context():
        json_escolas = json.dumps(new_escolas)
        
        response_escolas_insert = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escolas,
            content_type='application/json'
        )
        
        escolas_dict = json.loads(response_escolas_insert.get_data())
        
        assert response_escolas_insert.status_code == 200

        #RECUPERAR EDIFICIO
        response_send_edificio = app.test_client().get(
            f'api/v1/send_frontend/edificio/1'
        )
        
        assert response_send_edificio.status_code == 200


        json_hidrometro = json.dumps(new_hidrometro)
        
        response_hidrometro = app.test_client().post(
            'api/v1/cadastros/hidrometros',
            data=json_hidrometro,
            content_type='application/json'
        )
        
        hidrometro = json.loads(response_hidrometro.get_data())

        print(f"\033[32m{hidrometro['data']['hidrometro']}\033[0m")
        print(f"Escola: \033[32m{escolas_dict['data']['nome']}\033[0m")

        assert response_hidrometro.status_code == 200


        json_monitoramento = json.dumps({
                "hidrometro": hidrometro['data']['hidrometro'],
                "leitura": "250000",
                "nome": escolas_dict['data']['nome'],
                "fk_escola":1,
                "data":"11/02/2023",
                "hora":"11:20"
            })
        response_monitoramento = app.test_client().post(
            '/api/v1/monitoramento/cadastrarleitura',
            data=json_monitoramento,
            content_type='application/json'
        )

        monitoramento_dict = json.loads(response_monitoramento.get_data())

        assert response_monitoramento.status_code == 200

        response_monitoramento = app.test_client().delete(

            f'api/v1/monitoramento/deletar-leitura/1'
        )

def test_deletar_monitoramento_duas_escolas(app, new_escolas, new_hidrometro, segunda_escola):
    
    with app.app_context():
        json_escolas = json.dumps(new_escolas)
        
        response_escolas_insert = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escolas,
            content_type='application/json'
        )
        
        escolas_dict = json.loads(response_escolas_insert.get_data())
        
        assert response_escolas_insert.status_code == 200

        #RECUPERAR EDIFICIO
        response_send_edificio = app.test_client().get(
            f'api/v1/send_frontend/edificio/1'
        )
        
        assert response_send_edificio.status_code == 200

        #Segunda Escola

        json_escolas_2 = json.dumps(segunda_escola)
        
        response_escolas_insert_2 = app.test_client().post(
            'api/v1/cadastros/escolas',
            data=json_escolas_2,
            content_type='application/json'
        )
        
        escolas_dict = json.loads(response_escolas_insert_2.get_data())
        
        assert response_escolas_insert_2.status_code == 200

        #RECUPERAR EDIFICIO
        response_send_edificio_2 = app.test_client().get(
            f'api/v1/send_frontend/edificio/2'
        )
        
        assert response_send_edificio_2.status_code == 200


    #     hidrometro = {
    #     "fk_edificios":1,
    #     "hidrometro":"HIDROMETRO1"
    # }

        json_hidrometro = json.dumps(new_hidrometro)
        
        response_hidrometro = app.test_client().post(
            'api/v1/cadastros/hidrometros',
            data=json_hidrometro,
            content_type='application/json'
        )
        
        hidrometro = json.loads(response_hidrometro.get_data())

        print(f"\033[32m{hidrometro['data']['hidrometro']}\033[0m")
        print(f"Escola: \033[32m{escolas_dict['data']['nome']}\033[0m")

        assert response_hidrometro.status_code == 200


        json_monitoramento_1 = json.dumps({
                "hidrometro": hidrometro['data']['hidrometro'],
                "leitura": "250000",
                "nome": escolas_dict['data']['nome'],
                "fk_escola":1,
                "data":"11/02/2023",
                "hora":"11:20"
            })
        response_monitoramento_1 = app.test_client().post(
            '/api/v1/monitoramento/cadastrarleitura',
            data=json_monitoramento_1,
            content_type='application/json'
        )

        monitoramento_dict = json.loads(response_monitoramento_1.get_data())

        assert response_monitoramento_1.status_code == 200

       
        response_monitoramento_1 = app.test_client().delete(

            f'api/v1/monitoramento/deletar-leitura/1'
        )