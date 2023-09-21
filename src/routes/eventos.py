import json
from flask import Blueprint, jsonify, request
import re
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException
from ..models import Eventos, AuxTipoDeEventos, db
from sqlalchemy.exc import ArgumentError

eventos = Blueprint('eventos', __name__, url_prefix = '/api/v1/cadastro-evento')


#cadastro de evento
@eventos.post('/eventos')
def eventos_cadastro():

    try:

        formulario = request.get_json()
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400
    
    try:

        fk_tipo = formulario.get("fk_tipo", None)
        nome = formulario.get("nome", None)
        datainicio = formulario.get("datainicio", None)
        datafim = formulario.get("datafim", None)
        local = formulario.get("local", None)
        tipo_de_local = formulario.get("tipo_de_local", None)
        observacao = formulario.get("observacao", None)
        color = formulario.get("color", None)
    except Exception as e:
        return jsonify({
            "mensagem": "Verifique os nomes das variaveis do json enviado!!!",
            "status": False
        }), 400
    
    try:   
        
        evento = Eventos(
            fk_tipo=fk_tipo,
            nome=nome,
            datainicio=datainicio,
            datafim=datafim,
            local=local,
            tipo_de_local=tipo_de_local,
            observacao=observacao,
            color=color
        )

        db.session.add(evento)
        db.session.commit()
            
        return jsonify({'status':True, "mensagem":"Cadastro Realizado","data":evento.to_json()}), HTTP_200_OK

    except ArgumentError as e:
        error_message = str(e)
        error_data = {'error': error_message}
        json_error = json.dumps(error_data)
        print(json_error)
        return json_error

    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23505':
            # extrai o nome do campo da mensagem de erro
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            return jsonify({'status': False, 'mensagem': 'Erro no cabeçalho.', 'codigo': str(e)}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        return jsonify({'status': False, 'mensagem': 'Erro postgresql', 'codigo': str(e)}), 500
    
    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == '500':
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        if isinstance(e, HTTPException) and e.code == '400':
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            "erro":e
        })
        
        
        
@eventos.post('/tipo-de-evento-ocasional')
def tipoeventoocasional():
    
    try:
        formulario = request.get_json()
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400
        
    try:
        fk_cliente = formulario.get('fk_cliente')
        ehResposta = formulario.get('ehResposta')
        nome_do_evento = formulario.get('nome_do_evento')
        requerResposta = formulario.get('requerResposta')
        tolerencia = formulario.get('tolerencia')
        unidade = formulario.get('unidade')
        
    except Exception as e:
        return jsonify({
            "mensagem": "Verifique os nomes das variaveis do json enviado!!!",
            "status": False
        }), 400
        
    try:
        
        tipoevento = AuxTipoDeEventos(
            fk_cliente=fk_cliente,
            nome_do_tipo_de_evento=nome_do_evento,
            acao = ehResposta,
            recorrente = False,
            requer_acao=requerResposta,
            tempo=tolerencia,
            unidade=unidade
        )
        
        db.session.add(tipoevento)
        db.session.commit()
        
        return jsonify({'status':True, "mensagem":"Cadastro Realizado","data":tipoevento.to_json()}), HTTP_200_OK
    
    
    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23505':
            # extrai o nome do campo da mensagem de erro
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED
        if e.orig.pgcode == '01004':
            return jsonify({'status': False, 'mensagem': 'Erro no cabeçalho.', 'codigo': str(e)}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        return jsonify({'status': False, 'mensagem': 'Erro postgresql', 'codigo': str(e)}), 500
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível inserir no banco de dados!",
            "status": False,
            "codigo": e
        }), 400



@eventos.post('/tipo-de-evento-recorrente')
def tipoeventorecorrente():
    
    try:
        formulario = request.get_json()
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400
        
    try:
        
        fk_cliente = formulario.get('fk_cliente')
        ehResposta = formulario.get('ehResposta')
        nome_do_evento = formulario.get('nome_do_evento')
        dia = formulario.get('dataRecorrente')
        mes = formulario.get('mesRecorrente')
        requerResposta = formulario.get('requerResposta')
        tolerencia = formulario.get('tolerencia')
        unidade = formulario.get('unidade')
        
    except Exception as e:
        return jsonify({
            "mensagem": "Verifique os nomes das variaveis do json enviado!!!",
            "status": False
        }), 400
        
    try:
        
        tipoevento = AuxTipoDeEventos(
            fk_cliente=fk_cliente,
            nome_do_tipo_de_evento=nome_do_evento,
            acao = ehResposta,
            recorrente = True,
            dia = dia,
            mes = mes,
            requer_acao=requerResposta,
            tempo=tolerencia,
            unidade=unidade
        )
        
        db.session.add(tipoevento)
        db.session.commit()
        
        return jsonify({'status':True, "mensagem":"Cadastro Realizado","data":tipoevento.to_json()}), HTTP_200_OK
    
    
    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23505':
            # extrai o nome do campo da mensagem de erro
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED
        if e.orig.pgcode == '01004':
            return jsonify({'status': False, 'mensagem': 'Erro no cabeçalho.', 'codigo': str(e)}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        return jsonify({'status': False, 'mensagem': 'Erro postgresql', 'codigo': str(e)}), 500
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível inserir no banco de dados!",
            "status": False,
            "codigo": e
        }), 400












