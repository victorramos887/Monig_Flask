from flask import Blueprint, jsonify, request, render_template
from ..constants.http_status_codes import (HTTP_200_OK, HTTP_400_BAD_REQUEST)
from sqlalchemy import exc, func
from ..models import Escolas, Edificios, AreaUmida, Equipamentos, Populacao, AreaUmida, Hidrometros, db
from flasgger import swag_from

send_frontend = Blueprint('send_frontend', __name__, url_prefix = '/api/v1/send_frontend')


#RETORNA TODAS AS ESCOLAS
@send_frontend.get('/escolas')
@swag_from('../docs/send_frontend/escolas.yaml')
def escolas():

    escolas = Escolas.query.all()
    return jsonify({'return':[escola.to_json() for escola in escolas], "status": True}), HTTP_200_OK

#RETORNA APENAS UMA ESCOLA
@send_frontend.get('/escolas/<int:id>')
def get_escolas(id):
    escola = Escolas.query.filter_by(id=id).first()
    return jsonify({'escola':escola.to_json() if escola is not None else escola, "status": True})

#RETORNA TODOS OS ESDIFICOS DA ESCOLA PARA MONTAR A TABELA
@send_frontend.get('/edificios-table/<int:id>')
@swag_from('../docs/send_frontend/edificios.yaml')
def edificios(id):
    edificios = Edificios.query.filter(Edificios.fk_escola == id).all()
    result = []

    for edificio in edificios:
        #População
        soma_colaboradores, soma_alunos = (
            db.session.query(
                func.sum(Populacao.quant_de_funcionarios_usuarios).label('soma_colaboradores'),
                func.sum(Populacao. quant_de_alunos_usuarios).label('soma_alunos')
            )
            .join(Edificios)
            .filter(Populacao.fk_edificios == edificio.id)
            .first()
        )
        soma_total = (soma_colaboradores or 0) + (soma_alunos or 0)

        #Area umida
        contador_area_umida = db.session.query(func.count(AreaUmida.id)).filter(AreaUmida.fk_edificios == edificio.id).scalar()

        result.append({
            'id': edificio.id,
            'nome':edificio.nome_do_edificio,
            'populacao': soma_total or 0,
            'area_umida':contador_area_umida or 0
        })

    return jsonify({'edificios':result})

#RETORNA APENAS O EDIFICIO QUE DESEJA ATUALIZAR
@send_frontend.get('/edificio/<int:id>')
def edificio(id):

    edificio = Edificios.query.filter(Edificios.id == id).first()
    if edificio is None or edificio == '':
        return jsonify({'erro':'Edificio não encontrado',  "status": False}), HTTP_400_BAD_REQUEST

    return jsonify({'edificio':edificio.to_json(), "status": True}), HTTP_200_OK


#TODAS AREA UMIDAS
@send_frontend.get('/area_umidas_table/<int:id>')
@swag_from('../docs/send_frontend/area_umidas.yaml')
def area_umidas(id):
    # fk_edificios = request.args.get('')
    areas_umidas = AreaUmida.query.filter_by(fk_edificios = id, status=True).all()
    result = list()
    for area_umida in areas_umidas:
        #População
        total = (
            db.session.query(
                func.sum(Equipamentos.quant_total).label('total'),
            )
            .join(AreaUmida)
            .filter(Equipamentos.fk_area_umida == area_umida.id)
            .first()
        )

        result.append({
            'id': area_umida.id,
            'tipo_area_umida':area_umida.tipo_area_umida,
            'quant_equipamentos': total.total or 0 if total else 0,
            "status":area_umida.status_area_umida
        })

    return jsonify({'area_umidas':result})

#RETORNA APENAS UMA 
@send_frontend.get('/area_umida/<int:id>')
def get_area_umida(id):
    area_umida = AreaUmida.query.filter_by(id=id).first()
    
    return jsonify({'area_umida':area_umida.to_json() if area_umida is not None else area_umida})


#TODOS OS EQUIPAMENTOS
@send_frontend.get('/equipamentos-table/<int:id>')
@swag_from('../docs/send_frontend/equipamentos.yaml')
def equipamentos(id):

    equipamentos = Equipamentos.query.filter_by(fk_area_umida = id).all()

    return jsonify({
        f'equipamentos':[equipamento.to_json() for equipamento in equipamentos]
    })

#RETORNA APENAS UM
@send_frontend.get('/equipamento/<int:id>')
def get_equipamento(id):
    equipamento = Equipamentos.query.filter_by(id=id).first()
    return jsonify({'equipamento':equipamento.to_json() if equipamento is not None else equipamento})


#TODAS AS POPULAÇÕES   
@send_frontend.get('/populacao-table/<int:id>')
def populacao(id):
    populacoes = Populacao.query.filter_by(fk_edificios = id, status = True).all()
    return jsonify({
        "populacao":[populacao.to_json() for populacao in populacoes]
    })

#RETORNA APENAS UMA 
@send_frontend.get('/populacao/<int:id>')
def get_populacao(id):
    populacao = Populacao.query.filter_by(id=id).first()
    return jsonify({'populacao':populacao.to_json() if populacao is not None else populacao})


#TODOS OS HIDROMETROS
@send_frontend.get('/hidrometros-table/<int:id>')
def hidrometro(id):
    hidrometros = Hidrometros.query.filter_by(fk_edificios = id, status = True).all()
    return jsonify({
        "hidrometro":[hidrometro.to_json() for hidrometro in hidrometros]
    })

#RETORNA APENAS UM
@send_frontend.get('/hidrometro/<int:id>')
def get_hidrometro(id):
    hidrometro = Hidrometros.query.filter_by(id=id).first()
    return jsonify({'hidrometro':hidrometro.to_json() if hidrometro is not None else hidrometro})