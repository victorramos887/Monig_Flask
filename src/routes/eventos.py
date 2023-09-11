import json
from flask import Blueprint, jsonify, request
import re
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException
from ..models import Eventos, TipoDeEventos, db
from sqlalchemy.exc import ArgumentError

eventos = Blueprint('eventos', __name__, url_prefix = '/api/v1/cadastro-evento')


@eventos.post('/tipo-evento')
def tipoevento():
    meses_dict = {
        "Janeiro": 1,
        "Fevereiro": 2,
        "Março": 3,
        "Abril": 4,
        "Maio": 5,
        "Junho": 6,
        "Julho": 7,
        "Agosto": 8,
        "Setembro": 9,
        "Outubro": 10,
        "Novembro": 11,
        "Dezembro": 12
    }

    periodicidade = {
            "Ocasional":False, 
            "Recorrente":True
        }
    
    try:
        formulario = request.get_json()

        print(formulario)

        fk_cliente = formulario.get("fk_cliente")
        nome_do_tipo_de_evento = formulario.get("nome_do_evento")
        periodicidade = periodicidade.get(formulario.get('periodicidade')) if formulario.get('periodicidade') is not None else False

        print(periodicidade)

        dia = formulario.get("dataRecorrente") if formulario.get('dataRecorrente') and formulario.get("dataRecorrente") !="" else None
        mes = meses_dict.get(formulario.get('mesRecorrente')) if formulario.get('mesRecorrente') and formulario.get('mesRecorrente') != "" else None
        requer_acao = formulario.get('requerResposta', None) if formulario.get('requerResposta') is not None else False
        tempo = formulario.get('tolerancia') if formulario.get('tolerancia') else None
        unidade = formulario.get('unidade') if formulario.get('unidade') else None
        acao = formulario.get('ehResposta') if formulario.get('ehResposta') is not None else False

        tipo_evento = TipoDeEventos(
            fk_cliente=fk_cliente,
            nome_do_tipo_de_evento=nome_do_tipo_de_evento,
            recorrente=periodicidade,
            dia=dia,
            mes=mes,
            requer_acao=requer_acao,
            tempo=tempo,
            unidade=unidade,
            acao=acao
        )

        db.session.add(tipo_evento)
        db.session.commit()
        
        return jsonify({'status':True, "mensagem":"Cadastro Realizado","data":tipo_evento.to_json()}), HTTP_200_OK

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


#cadastro de evento
@eventos.post('/eventos')
def eventos_cadastro():

    try:

        formulario = request.get_json()

        fk_tipo = formulario.get("fk_tipo", None)
        nome = formulario.get("nome", None)
        datainicio = formulario.get("datainicio", None)
        datafim = formulario.get("datafim", None)
        local = formulario.get("local", None)
        tipo_de_local = formulario.get("tipo_de_local", None)
        observacao = formulario.get("observacao", None)
        color = formulario.get("color", None)
       
        
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