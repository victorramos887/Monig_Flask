from flask import Blueprint, jsonify, request
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
from ..models import Escolas, Edificios, db, AreaUmida, Equipamentos, Populacao, Hidrometros
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException
import re
from http import HTTPStatus

editar = Blueprint('editar', __name__, url_prefix='/api/v1/editar')

#EDITAR ESCOLA
@editar.put('/escolas/<id>')
def escolas_editar(id):
    escola = Escolas.query.filter_by(id=id).first()
    edificio = Edificios.query.filter_by(fk_escola=id).first()

    #VERIFICAR O QUE FOI ALTERADO
    body = request.get_json()

    if not escola:
        return jsonify({'mensagem': 'Escola não encontrado', "status": False}), 404

    for k, i in escola.to_json().items():
        print(k, i)

    for k, i in edificio.to_json().items():
        print(k, i)

    try:
        #comparar e incluir na tabela EscolasHistorico
        # if escola != body:
        #     db.session.add(EscolasHistorico(fk_escola=escola.id, cnpj=escola.cnpj, cep=escola.cep, nivel=escola.nivel))

        #atualizar tabela Escola - novas informações
        escola.update(
            nome=body["nome"],
            cnpj=body["cnpj"],
            email=body["email"],
            telefone=body["telefone"],
            nivel=body["nivel"]
        )

        #db.session.commit()

        edificio.update(
            numero_edificio=body["numero"],
            cep_edificio=body["cep"],
            cidade_edificio=body["cidade"],
            estado_edificio=body["estado"],
            cnpj_edificio=body["cnpj"],
            logradouro_edificio=body["logradouro"],
            complemento=body["complemento"]
        )

        db.session.commit()

        return jsonify({"escola": escola.to_json(), "status": True}), HTTP_200_OK 
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

        return jsonify({
            "status":False,"mensagem":"Erro não tratado", "codigo":e
        }), HTTP_500_INTERNAL_SERVER_ERROR


#EDITAR EDIFICIOS
@editar.put('/edificios/<id>')
def edificios_editar(id):
    edificio = Edificios.query.filter_by(id=id).first()
    body = request.get_json()

    if not edificio:
        return jsonify({'mensagem': 'Edificio não encontrado',"status": False}), 404

    try:
        edificio.update(**body)

        db.session.commit()

        return jsonify({"edificio":edificio.to_json(), "status": True}), HTTP_200_OK
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

#EDITAR HIDROMETRO
@editar.put('/hidrometros/<id>')
def hidrometro_editar(id):
    hidrometro = Hidrometros.query.filter_by(id=id).first()
    body = request.get_json()

    if not hidrometro:
        return jsonify({'mensagem': 'Hidrometro não encontrado', "status": False}), 404
    try:
        hidrometro.update(**body)

        db.session.commit()

        return jsonify({"hidrometro":hidrometro.to_json(), "status": True}), HTTP_200_OK
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
   

#EDITAR POPULACAO
@editar.put('/populacao/<id>')
def populacao_editar(id):
    populacao = Populacao.query.filter_by(id=id).first()
    body = request.get_json()

    if not populacao:
        return jsonify({'mensagem': 'Populacao não encontrado', "status": False}), 404
    
    try:

        populacao.update(**body)

        db.session.commit()

        return jsonify({"populacao":populacao.to_json(), "status": True}), HTTP_200_OK
        
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
    

#EDITAR AREA UMIDA
@editar.put('/area-umida/<id>')
def area_umida_editar(id):
    umida = AreaUmida.query.filter_by(id=id).first()
    body = request.get_json()

    if not umida:
        return jsonify({'mensagem': 'Area Umida não encontrado', "status": False}), 404
    try:
        umida.update(**body)
        db.session.commit()
        return jsonify({"areaumida":umida.to_json(), "status": True}), HTTP_200_OK
        
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
    

#EDITAR EQUIPAMENTO
@editar.put('/equipamentos/<id>')
def equipamento_editar(id):
    equipamento = Equipamentos.query.filter_by(id=id).first()
    body = request.get_json()

    if not equipamento:
        return jsonify({'mensagem': 'Equipamento não encontrado', "status": False}), 404
    try:

        equipamento.update(**body)

        db.session.commit()

        return jsonify({"equipamento":equipamento.to_json(), "status": True}), HTTP_200_OK
        
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
    