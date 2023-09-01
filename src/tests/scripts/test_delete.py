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


def test_deleta_edificio(app, new_edificios, new_area_umida, new_equipamentos, new_populacao, new_hidrometro):
    """Deletando edificio"""
    with app.app_context():

        # -------------------------------------------------------
        # INSERT
        # -------------------------------------------------------

        # ADICIONAR EDIFICIO
        json_edificio = json.dumps(new_edificios)

        response_post = app.test_client().post(
            'api/v1/cadastros/edificios',
            data=json_edificio,
            content_type='application/json'
        )
        edificio_dict = json.loads(response_post.get_data())

        assert response_post.status_code == 200

        # Adicionar 5 Areas umidas
        for i in range(0, 5):
            new_area_umida['fk_edificios'] = edificio_dict['id']
            json_area_umida = json.dumps(new_area_umida)
            response_area_umida_post = app.test_client().post(
                'api/v1/cadastros/area-umida',
                data=json_area_umida,
                content_type='application/json'
            )
            assert response_area_umida_post.status_code == 200

            for i in range(0, 5):

                json_equipamentos = json.dumps(new_equipamentos)

                response_equipamentos_post = app.test_client().post(
                    'api/v1/cadastros/equipamentos',
                    data=json_equipamentos,
                    content_type='application/json'
                )
                assert response_equipamentos_post.status_code == 200

        # Adicionar 5 populações
        for i in range(0, 5):
            new_populacao['fk_edificios'] = edificio_dict['id']

            json_populacao = json.dumps(new_populacao)
            reponse_populacao = app.test_client().post(
                'api/v1/cadastros/populacao',
                data=json_populacao,
                content_type='application/json'
            )

            assert reponse_populacao.status_code == 200

            response_populacao_get = app.test_client().get(
                f'api/v1/send_frontend/populacao-table/{edificio_dict["id"]}'
            )

        #Adicionar 5 hidrometro
        for i in range(0, 5):

            new_hidrometro['fk_edificios'] = edificio_dict['id']

            json_hidrometro = json.dumps(new_hidrometro)
            response_hidrometro = app.test_client().post(
                'api/v1/cadastros/hidrometros',
                data=json_hidrometro,
                content_type='application/json'
            )
            hidrometro_dict = json.loads(response_hidrometro.get_data())
            assert response_hidrometro.status_code == 200

        # ----------------------------------------------------------
        # ----------------------------------------------------------

        # ----------------------------------------------------------
            # DELETAR
        # ----------------------------------------------------------

        response_delete = app.test_client().delete(
            f'api/v1/remover/edificios/{edificio_dict["id"]}',
        )

        assert response_delete.status_code == 200

        # ----------------------------------------------------------
        # ----------------------------------------------------------

        # ----------------------------------------------------------
        # VERFICANDO RETORNOS
        # ----------------------------------------------------------
        # Retorno edificio

        response_edificio_get = app.test_client().get(
            f'api/v1/send_frontend/edificio/{edificio_dict["id"]}'
        )
       
        dict_ = json.loads(response_edificio_get.get_data())
        
        assert response_edificio_get.status_code == 400
        assert dict_['erro_edificio']['status_do_registro'] == False

        # Retorno Area Umida
        response_area_umida_get = app.test_client().get(
            f'api/v1/send_frontend/area_umida/1'
        )

        assert response_area_umida_get.status_code == 400
        assert json.loads(response_area_umida_get.get_data())[
            'erro_area_umida']['status_do_registro'] == False

        # Retorno equipamentos

        reponse_equipamentos_get = app.test_client().get(
            f'api/v1/send_frontend/equipamento/2'
        )

        assert reponse_equipamentos_get.status_code == 400
        assert json.loads(reponse_equipamentos_get.get_data())[
            'erro_equipamento']['status_do_registro'] == False

        # Retorno de apenas uma Populacao -- Verificar se é possivel análisar todas

        response_populacao_get = app.test_client().get(
            f'api/v1/send_frontend/populacao/2'
        )
        print("populacao", json.loads(response_populacao_get.get_data()))
        assert response_populacao_get.status_code == 400
        assert json.loads(response_populacao_get.get_data())['erro_populacao']['status_do_registro'] == False


        #Retorno apenas um hidrometro
        response_hidrometro_get = app.test_client().get(
            f'api/v1/send_frontend/hidrometro/2'
        )

        assert response_hidrometro_get.status_code == 400
        assert json.loads(response_hidrometro_get.get_data())['erro_hidrometro']['status_do_registro'] == False
        # ----------------------------------------------------------
        # # ----------------------------------------------------------
