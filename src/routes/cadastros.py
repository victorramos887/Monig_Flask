from flask import Blueprint, jsonify, request
import re
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy import exc
from flasgger import swag_from
from werkzeug.exceptions import HTTPException
from ..models import Escolas, Edificios, db, AreaUmida, Equipamentos, Populacao, Hidrometros, Tabela


cadastros = Blueprint('cadastros', __name__, url_prefix = '/api/v1/cadastros')

@cadastros.post('/testando')
def testando():
    formulario = request.get_json()
    tabela = Tabela(**formulario)

    db.session.add(tabela)
    db.session.commit()
    retorno = Tabela.query.filter_by(id=tabela.id).first()

    return jsonify({
        "data":retorno.to_json(),
        "id":retorno.id
    })


#Cadastros das escolas
@cadastros.post('/escolas')
@swag_from('../docs/cadastros/escolas.yaml')
def escolas():
    formulario = request.get_json()

    try:
        escola = Escolas(**formulario)
    
        db.session.add(escola)
        db.session.commit()

        return jsonify({'status':True, 'id': escola.id, "mensagem":"Cadastro Realizado","data":escola.to_json()}), HTTP_200_OK
    
    except exc.DBAPIError as e:   
        if e.orig.pgcode == '23505':
            # extrai o nome do campo da mensagem de erro
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED
       

        if e.orig.pgcode == '01004':
            return jsonify({'status': False, 'mensagem': 'Erro no cabeçalho.', 'codigo': str(e)}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == '500':
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        
        if isinstance(e, HTTPException) and e.code == '400':
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST


#Cadastros dos edifícios.
@cadastros.post('/edificios')
@swag_from('../docs/cadastros/edificios.yaml')
def edificios():

    formulario = request.get_json()
    try:
        edificio = Edificios(**formulario)
        #inserir no banco de dados. Tabela edificios
        db.session.add(edificio)
        db.session.commit()

        return jsonify({'status':True, 'id': edificio.id, "mensagem":"Cadastro Realizado!","data":edificio.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            match = re.search(r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({ 'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT
          

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'mensagem': 'Erro no cabeçalho', 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        if str(e) == '500':
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        
        if str(e) == '400':
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST


@cadastros.post('/hidrometros')
@swag_from('../docs/cadastros/hidrometros.yaml')
def hidrometros():

    formulario = request.get_json()
    hidrometros = Hidrometros(**formulario)

    try:
        #inseri no banco de dados. Tabela hidrometros
        db.session.add(hidrometros)
        db.session.commit()

        return jsonify({'status':True, 'id': hidrometros.id, "mensagem":"Cadastro Realizado com sucesso","data":hidrometros.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        
        if e.orig.pgcode == '23503':
            match = re.search(r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({ 'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT
          
        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED
       
        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'mensagem': 'Erro no cabeçalho', 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        
        if isinstance(e, HTTPException) and e.code == 400:
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST



@cadastros.post('/populacao')
@swag_from('../docs/cadastros/populacao.yaml')
def populacao():

    formulario = request.get_json()
    populacao = Populacao(**formulario)

    try:
        #inseri no banco de dados. Tabela populacao
        db.session.add(populacao)
        db.session.commit()

        return jsonify({'status':True, 'id': populacao.id, "mensagem":"Cadastrado realizado com sucesso","data":populacao.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        
        if e.orig.pgcode == '23503':
            match = re.search(r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({ 'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT
          

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'mensagem': 'Erro no cabeçalho', 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        
        if isinstance(e, HTTPException) and e.code == 400:
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST


#Cadastros das areas umidas
@cadastros.post('/area-umida')
@swag_from('../docs/cadastros/area-umida.yaml')
def area_umida():

    formulario = request.get_json()
    umida = AreaUmida(**formulario)

    try:
        #inseri no banco de dados. Tabela AreaUmida
        db.session.add(umida)
        db.session.commit()

        return jsonify({'status':True, 'id': umida.id, "mensagem":"Cadastrado realizado com sucesso","data":umida.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        
        if e.orig.pgcode == '23503':
            match = re.search(r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({ 'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT
          
        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'mensagem': "Erro no cabeçalho", 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        
        if isinstance(e, HTTPException) and e.code == 400:
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST


@cadastros.post('/equipamentos')
@swag_from('../docs/cadastros/equipamentos.yaml')
def equipamentos():

    formulario = request.get_json()
    equipamento = Equipamentos(**formulario)

    try:
        #inseri no banco de dados. Tabela Equipamentos
        db.session.add(equipamento)
        db.session.commit()

        return jsonify({'status':True, 'id': equipamento.id, "mensagem":"Cadastrado realizado com sucesso","data":equipamento.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
       
        if e.orig.pgcode == '23503':
            match = re.search(r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({ 'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT
          
        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED
        
        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'mensagem': "Erro no cabeçalho", 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        
        if isinstance(e, HTTPException) and e.code == 400:
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST