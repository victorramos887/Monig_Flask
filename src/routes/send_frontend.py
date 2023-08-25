from flask import Blueprint, json, jsonify, request, render_template, current_app
from ..constants.http_status_codes import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)
from sqlalchemy import func, select, desc
from ..models import db, Escolas, Edificios, Reservatorios, AreaUmida, TipoDeEventos, EscolaNiveis, Equipamentos, Populacao, AreaUmida, Hidrometros, OpNiveis, Historico

send_frontend = Blueprint('send_frontend', __name__,
                          url_prefix='/api/v1/send_frontend')


# Verificar Historico de Deleção
@send_frontend.get('/historico')
def historico():

    historico = Historico.query.all()
    return jsonify([json.dumps(h.to_json()) for h in historico])
   


# RETORNA TODAS AS ESCOLAS
@send_frontend.get('/escolas')
def escolas():
    # token = validacao_token(request.headers.get('Authorization'))

    escolas = Escolas.query.filter_by(status_do_registro=True).all()
    return jsonify({
        'return': [escola.to_json() for escola in escolas],
        'status': True,
        'mensagem': 'Escolas retornadas com sucesso'
    }), 200


# RETORNA APENAS UMA ESCOLA
@send_frontend.get('/escolas/<int:id>')
def get_escolas(id):
    escola = Escolas.query.filter_by(id=id).first()

    if not escola:
        return jsonify({
            "status": False,
            "mensagem": "Escola não encontrada."
        }), 404

    escola_json = escola.to_json() if escola is not None else ''

    edificio = Edificios.query.filter_by(fk_escola=id).first()
    edificio_json = edificio.to_json() if edificio is not None else None

    result = db.session.query(EscolaNiveis.escola_id, OpNiveis.nivel) \
        .join(OpNiveis, OpNiveis.id == EscolaNiveis.nivel_ensino_id) \
        .filter(EscolaNiveis.escola_id == escola.id) \
        .all()

    nivelRetorno = [nivel for escola_id, nivel in result]

    if edificio is not None and escola is not None:
        enviar = {
            "cnpj": edificio_json["cnpj_edificio"],
            "email": escola_json["email"],
            "id": escola_json["id"],
            "nivel": nivelRetorno,
            "nome": escola_json["nome"],
            "status_do_registro": escola_json["status_do_registro"],
            "telefone": escola_json["telefone"],
            "logradouro": edificio_json["logradouro_edificio"],
            "bairro": edificio_json["bairro_edificio"],
            "numero": edificio_json["numero_edificio"],
            "complemento": edificio_json["complemento_edificio"],
            "estado": edificio_json["estado_edificio"],
            "cep": edificio_json["cep_edificio"],
            "cidade": edificio_json["cidade_edificio"]
        }
        return jsonify({
            "status": True,
            "escola": enviar,
            'mensagem': 'Escola retornada com sucesso!'
        }), 200

    # Adicione esta declaração de retorno caso a condição anterior não seja satisfeita
    return jsonify({
        "status": False,
        "mensagem": "Escola não encontrada."
    }), 404


# RETORNA TODOS OS EDIFICIOS DA ESCOLA PARA MONTAR A TABELA
@send_frontend.get('/edificios-table/<int:id>')
def edificios(id):

    edificios = Edificios.query.filter_by(
        fk_escola=id, status_do_registro=True).order_by(desc(Edificios.principal)).all()
    result = []

    for edificio in edificios:
        # População
        soma_colaboradores, soma_alunos = (
            db.session.query(
                func.sum(Populacao.funcionarios).label('soma_colaboradores'),
                func.sum(Populacao.alunos).label('soma_alunos')
            )
            .join(Edificios)
            .filter(Populacao.fk_edificios == edificio.id)
            .first()
        )
        soma_total = (soma_colaboradores or 0) + (soma_alunos or 0)

        # Area umida
        contador_area_umida = db.session.query(func.count(AreaUmida.id)).filter(
            AreaUmida.fk_edificios == edificio.id).scalar()

        # Reservatorios
        reservatorios = Reservatorios.query.filter(
            Reservatorios.fk_escola == id, Reservatorios.status_do_registro == True).all()
        info_reservatorios = [reservatorio.to_json()
                              for reservatorio in reservatorios]

        result.append({
            'id': edificio.id,
            'nome': edificio.nome_do_edificio,
            'populacao': soma_total or 0,
            'area_umida': contador_area_umida or 0,
            'principal': edificio.principal,
            'reservatorios': info_reservatorios
        })

    return jsonify({
        'edificios': result,
        'status': True,
        'mensagem': 'Edificio retornado com sucesso!'
    })


# RETORNA APENAS O EDIFICIO QUE DESEJA ATUALIZAR
@send_frontend.get('/edificio/<int:id>')
def edificio(id):

    edificio = Edificios.query.filter_by(
        id=id, status_do_registro=True).first()
    reservatorios = Reservatorios.query.filter(
        Reservatorios.fk_escola == id, Reservatorios.status_do_registro == True).all()

    if edificio is None:
        return jsonify({'erro': 'Edificio não encontrado',  "status": False}), HTTP_400_BAD_REQUEST

    return jsonify({
        "edificio": edificio.to_json(), "status": True
    }), HTTP_200_OK


# TODAS AREA UMIDAS
@send_frontend.get('/area_umidas_table/<int:id>')
def area_umidas(id):
    # fk_edificios = request.args.get('')
    areas_umidas = AreaUmida.query.filter_by(
        fk_edificios=id, status_do_registro=True).all()
    result = list()
    for area_umida in areas_umidas:
        # População
        total = (
            db.session.query(
                func.sum(Equipamentos.quantTotal).label('total'),
            )
            .join(AreaUmida)
            .filter(Equipamentos.fk_area_umida == area_umida.id)
            .first()
        )

        result.append({
            'id': area_umida.id,
            'tipo_area_umida': area_umida.tipo_area_umida_rel.tipo,
            'quant_equipamentos': total.total or 0 if total else 0,
            "status": "Aberto" if area_umida.status_area_umida else "Fechado"
        })

    return jsonify({'area_umidas': result, "status": True})

# RETORNA APENAS UMA


@send_frontend.get('/area_umida/<int:id>')
def get_area_umida(id):
    area_umida = AreaUmida.query.filter_by(id=id).first()
    return jsonify({'area_umida': area_umida.to_json() if area_umida is not None else area_umida, "status": True})

# TODOS OS EQUIPAMENTOS


@send_frontend.get('/equipamentos-table/<int:id>')
def equipamentos(id):

    equipamentos = Equipamentos.query.filter_by(
        fk_area_umida=id, status_do_registro=True).all()

    return jsonify({
        f'equipamentos': [equipamento.to_json() for equipamento in equipamentos], "status": True
    })

# RETORNA APENAS UM


@send_frontend.get('/equipamento/<int:id>')
def get_equipamento(id):
    equipamento = Equipamentos.query.filter_by(id=id).first()
    return jsonify({'equipamento': equipamento.to_json() if equipamento is not None else equipamento, "status": True})


# TODAS AS POPULAÇÕES
@send_frontend.get('/populacao-table/<int:id>')
def populacao(id):
    populacoes = Populacao.query.filter_by(
        fk_edificios=id, status_do_registro=True).all()
    return jsonify({
        "populacao": [populacao.to_json() for populacao in populacoes],
        "status": True
    })

# RETORNA APENAS UMA


@send_frontend.get('/populacao/<int:id>')
def get_populacao(id):
    populacao = Populacao.query.filter_by(id=id).first()
    return jsonify({'populacao': populacao.to_json() if populacao is not None else populacao, "status": True})


# TODOS OS HIDROMETROS
@send_frontend.get('/hidrometros-table/<int:id>')
def hidrometro(id):
    hidrometros = Hidrometros.query.filter_by(
        fk_edificios=id, status_do_registro=True).all()
    return jsonify({
        "hidrometro": [hidrometro.to_json() for hidrometro in hidrometros], "status": True
    })

# RETORNA APENAS UM


@send_frontend.get('/hidrometro/<int:id>')
def get_hidrometro(id):
    hidrometro = Hidrometros.query.filter_by(id=id).first()
    return jsonify({'hidrometro': hidrometro.to_json() if hidrometro is not None else hidrometro, "status": True})


@send_frontend.get('/reservatorio/<int:id>')
def get_reservatorio(id):

    reservatorio = Reservatorios.query.filter_by(
        id=id, status_do_registro=True
    ).first()

    return jsonify({
        'reservatorio': reservatorio.to_json() if reservatorio is not None else reservatorio, "status": True
    })

# TODOS OS RESERVATÓRIOS


@send_frontend.get('/reservatorios-table/<int:id>')
def reservatorios(id):
    reservatorios = Reservatorios.query.filter_by(
        fk_escola=id, status_do_registro=True).all()
    return jsonify({
        "reservatorios": [reservatorio.to_json() for reservatorio in reservatorios], "status": True
    })


@send_frontend.get('/tipo-de-eventos/<int:id>')
def tipo_de_eventos(id):

    tipo_de_eventos = TipoDeEventos.query.filter_by(
        fk_cliente = id
    ).all()

    return jsonify({
        "tipo_de_eventos":[
            tipo_de_evento.to_json() for tipo_de_evento in tipo_de_eventos
        ],
        "status":True
    }), 200


@send_frontend.get('/testando')
def testandoretorno():

    print(request.get_json())

    return "Retorno"