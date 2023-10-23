import json
from flask import Blueprint, jsonify, request
import re
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException
from ..models import Eventos, Escolas, Edificios, AreaUmida, Reservatorios, Hidrometros, AuxTipoDeEventos, AuxDeLocais, db
from sqlalchemy.exc import ArgumentError
from random import randint


eventos = Blueprint('eventos', __name__, url_prefix='/api/v1/cadastro-evento')

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
    "Ocasional": False,
    "Recorrente": True
}


def obter_local(tipo_de_local, nome):
    consultas = {
        "Escola": Escolas.query.filter_by(nome=nome).first(),
        "Edificação": Edificios.query.filter_by(nome_do_edificio=nome).first(),
        "Área Úmida": AreaUmida.query.filter_by(nome_area_umida=nome).first(),
        "Reservatório": Reservatorios.query.filter_by(nome_do_reservatorio=nome).first(),
        "Hidrômetro": Hidrometros.query.filter_by(hidrometro=nome).first()
    }
    
    return consultas.get(tipo_de_local)


@eventos.post('/tipo-de-evento-ocasional')
def tipoeventoocasional():

    try:
        formulario = request.get_json()
        print(formulario, "Valor")
        #tipo_evento
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400

    try:

        fk_cliente = formulario.get('fk_cliente')
        nome_do_evento = formulario.get('nome_do_evento')
        requerResposta = formulario.get('requerResposta')
        tempo = formulario.get('tolerancia')
        unidade = formulario.get('unidade')

    except Exception as e:
        return jsonify({
            "mensagem": "Verifique os nomes das variaveis do json enviado!!!",
            "status": False
        }), 400

    try:
        #Verificar no models, deixar enviar como None
        
        #color = "%06x" % randint(0, 0xFFFFFF)
        # color = f"{randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)}"
        color = '6ECB04'
        
        
        tipoevento = AuxTipoDeEventos(
            fk_cliente=fk_cliente,
            nome_do_tipo_de_evento=nome_do_evento,
            recorrente=False,
            requer_acao=requerResposta,
            tempo=tempo,
            unidade=unidade,
            color=f"#{color}"
        )

        db.session.add(tipoevento)
        db.session.commit()
        
        return jsonify({
                "status":True,
                "tipo_de_evento":tipoevento.to_json()
            }), 200 #Terminar Retorno

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



@eventos.post('/tipo-evento-recorrente')
def tipoeventorecorrente():

    try:
        formulario = request.get_json()

        print(formulario)

        fk_cliente = formulario.get("fk_cliente")
        nome_do_tipo_de_evento = formulario.get("nome_do_evento")
        # periodicidade = formulario.get('periodicidade') if formulario.get('periodicidade') is not None else False
        dia = formulario.get("dataRecorrente") if formulario.get(
            'dataRecorrente') and formulario.get("dataRecorrente") != "" else None
        mes = meses_dict.get(formulario.get('mesRecorrente')) if formulario.get(
            'mesRecorrente') and formulario.get('mesRecorrente') != "" else None
        requer_acao = formulario.get('requerResposta', None) if formulario.get(
            'requerResposta') is not None else False
        tempo = formulario.get('tolerancia') if formulario.get(
            'tolerancia') else None
        unidade = formulario.get(
            'unidade') if formulario.get('unidade') else None
       
        
        #COR ALEATÓRIA
        #color = "%06x" % randint(0, 0xFFFFFF)
        #color = f"{randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)}"
        color = "0474CB"

        tipo_evento = AuxTipoDeEventos(
            fk_cliente=fk_cliente,
            nome_do_tipo_de_evento=nome_do_tipo_de_evento,
            recorrente=True,
            dia=dia,
            mes=mes,
            requer_acao=requer_acao,
            tempo=tempo,
            unidade=unidade,
            color=f"#{color}"
        )

        db.session.add(tipo_evento)
        db.session.commit()

        return jsonify({'status': True, "mensagem": "Cadastro Realizado", "data": tipo_evento.to_json()}), HTTP_200_OK

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
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            "erro": e
        })


# cadastro de evento
@eventos.post('/eventos')
def eventos_cadastro():

    try:
        formulario = request.get_json()
        print(formulario)
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400
    
    try:
        #Verficando tipo de evento
        try:
            tipo_de_evento = formulario.get("tipo_de_evento", None)
            
            if not tipo_de_evento:
                return jsonify({
                    "mensagem": "Tipo de evento está Nulo!!!",
                    "status": False
                }), 400
                
            tipodeevento = AuxTipoDeEventos.query.filter_by(nome_do_tipo_de_evento=tipo_de_evento).first()
            
            if not tipodeevento:
                return jsonify({
                    "mensagem":f"Não foi encontrado o tipo de evento {tipo_de_evento}",
                    "status": False
                }), 400

        except Exception as e:
            return jsonify({
                "mensagem":"Não foi possível tratar o tipo de evento!",
                "codigo":str(e),
                "status":False
            }), 400


        fk_tipo = formulario.get("tipo_de_evento", None)
        nome = formulario.get("nome_do_evento", None)
        local = formulario.get("local", None)
        tipo_de_local = formulario.get("tipo_de_local", None)
        observacao = formulario.get("observacoes", None)
        encerramento = formulario.get("encerramento", False)
        data_encerramento = formulario.get("dataEncerramento", None)
        
        print(tipodeevento.recorrente)
        if tipodeevento.recorrente:
            datainicio = formulario.get("data_inicio", None)
            datafim = formulario.get("data_fim", None)
            
        else:
            datainicio = formulario.get("data", None)
            datafim = formulario.get("dataEncerramento", None)
            
    
        #Tratamento de tipo_de_local
        
        tipo_de_local_fk = AuxDeLocais.query.filter_by(nome_da_tabela=tipo_de_local).first()
        
        print(tipo_de_local_fk)
        
        if not tipo_de_local_fk:
            return jsonify({
                "mensagem":f"Não foi encontrado a tabela {formulario.get('tipo_de_local')}",
                "status":False
            }), 400
            
        
        local_fk = obter_local(tipo_de_local, local)
        
        if not local_fk:
            return jsonify({
                "mensagem":f"Não foi encontrado o local {local}",
                "status":False
            }), 400
            
            
        tipo_de_evento_fk = AuxTipoDeEventos.query.filter_by(nome_do_tipo_de_evento=fk_tipo).first()
        
        if not tipo_de_evento_fk:
            
            return jsonify({
                "mensagem":f"Não foi encontrado o tipo de evento {fk_tipo}",
                "status":False
            }), 400
            
        
        evento = Eventos(
            fk_tipo=tipo_de_evento_fk.id,
            nome=nome,
            datainicio=datainicio,
            datafim=datafim,
            local=local_fk.id,
            tipo_de_local=tipo_de_local_fk.id,
            observacao=observacao,
            encerramento=encerramento, 
            data_encerramento=data_encerramento
        )

        db.session.add(evento)
        db.session.commit()

        return jsonify({'status': True, "mensagem": "Cadastro Realizado!", "data":evento.to_json()}), HTTP_200_OK

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
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            "erro": e
        })


